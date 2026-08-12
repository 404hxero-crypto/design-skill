#!/usr/bin/env python3
# ============================================================
# 全域物料延展 · 从主视觉母版按 11 种比例裁切（人物完整性硬约束版）
# ------------------------------------------------------------
# 核心约束（「4 必须 · 3 禁止」）：
#   · MUST 1: 人物核心安全框 100% 完整包含于裁切结果（不可切靴/袍/脸/帽/杖/球）
#   · MUST 2: 宽高比严格等于目标物料比例（不拉伸不变形）
#   · MUST 3: 裁切结果像素全部来自原图（直接 copy，无滤镜无改色）
#   · MUST 4: 构图逻辑对齐 Skill 表
#                窄长 → 优先让人物居中且占画面较大比例
#                宽屏 → 在包含人物前提下，尽可能展开左右两侧氛围场景
#                方图 → 人物居中
#                展板 → 放大水晶球（品牌符号）视野
#   · PROHIBIT: 禁止拉伸 / 禁止变形 / 禁止改色
# ============================================================
import os, sys
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR  = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(SKILL_DIR, "assets")

# --------------- 11 种物料定义 ---------------
# 顺序：线上7 + 线下4
MATERIALS = [
    # (编号, 物料代码, 显示名, 比例 w/h, image_size, 输出文件名, 构图逻辑)
    ("①", "wechat_cover", "公众号封面",      4/3,  "landscape_4_3", "kv_wechat_cover.png", "wide"),      # 宽屏：展开左右氛围
    ("②", "xhs",          "小红书竖图",      3/4,  "portrait_4_3",  "kv_xhs_portrait.png", "mid_portrait+mobile"),  # 中竖+手机
    ("③", "xhs_square",   "小红书方图",      1.0,  "square",        "kv_xhs_square.png",   "square+mobile"),       # 方图+手机
    ("④", "douyin",       "抖音封面",        9/16, "portrait_16_9", "kv_douyin.png",       "narrow+mobile"),       # 窄长+手机
    ("⑤", "bilibili",     "B站封面",         16/9, "landscape_16_9","kv_bilibili.png",     "wide"),                # 宽屏
    ("⑥", "h5",           "H5 页面",         9/16, "portrait_16_9", "kv_h5.png",           "narrow+mobile"),       # 窄长+手机
    ("⑦", "banner",       "Banner 横幅",     16/9, "landscape_16_9","kv_banner.png",       "wide"),                # 宽屏
    ("⑧", "poster",       "海报 A3/A2/A1",   3/4,  "portrait_4_3",  "kv_poster.png",      "mid_portrait"),        # 中竖
    ("⑨", "poster_v",     "竖版海报",        9/16, "portrait_16_9", "kv_poster_v.png",     "narrow"),              # 窄长
    ("⑩", "rollup",       "易拉宝",          9/16, "portrait_16_9", "kv_rollup.png",       "narrow"),              # 窄长
    ("⑪", "board",        "展板",            4/3,  "landscape_4_3", "kv_board.png",        "board"),               # 展板（放大品牌符号）
]


def load_subject_bbox(img_W, img_H):
    """加载人物安全框（手动标注 + 坐标文件持久化）。若坐标文件不存在则返回默认人物中心偏左框。"""
    bbox_file = os.path.join(ASSETS_DIR, "subject_bbox.txt")
    sx0, sy0, sx1, sy1 = None, None, None, None
    if os.path.isfile(bbox_file):
        kv = {}
        with open(bbox_file) as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    k, v = line.split("=", 1)
                    kv[k.strip()] = v.strip()
        try:
            sx0 = int(kv["safe_x0"]); sy0 = int(kv["safe_y0"])
            sx1 = int(kv["safe_x1"]); sy1 = int(kv["safe_y1"])
        except Exception:
            sx0 = sy0 = sx1 = sy1 = None
    if sx0 is None:
        # 回退：按 Wizard 默认人物框（覆盖母版常见人物区域），预留 10%
        sx0 = int(img_W * 0.20)
        sy0 = int(img_H * 0.00)
        sx1 = int(img_W * 0.75)
        sy1 = int(img_H * 0.95)
    return sx0, sy0, sx1, sy1


def subject_preserving_crop(img, target_ratio, layout, sx0, sy0, sx1, sy1):
    """
    按目标比例裁切，且必须 100% 包含人物安全框 [sx0,sy0]-[sx1,sy1]。
    layout: wide / narrow / mid_portrait / square+mobile / mid_portrait+mobile / narrow+mobile / board
    返回 Image 与 (cx0, cy0, cx1, cy1)。
    """
    W, H = img.size
    SW, SH = sx1 - sx0, sy1 - sy0

    # 目标比例 r = cw/ch
    r = target_ratio

    # ---- 求解最小满足「人物完整」的裁切框尺寸 cw, ch ----
    # 约束: cw >= SW 且 ch >= SH 且 cw/ch = r
    # 解得:
    #   若 SW/SH >= r  → 人物比目标更"宽"。固定 cw = SW，则 ch_min = SW/r；若 ch_min < SH 则 ch 必须 = SH，此时 cw 被迫 = SH*r，这会 < SW，人物会被横向裁切！
    #     此时优先保人物：若人物必须完整，则 cw=max(SW, SH*r)，ch=max(SH, SW/r)
    #   推导公式：令 ch_min_candidate1 = SW / r   (由宽决定高,  cw=SW 完整包住横向)
    #            令 cw_min_candidate2 = SH * r   (由高决定宽,  ch=SH 完整包住纵向)
    #   实际取 cw = max(SW, ceil(SH * r))   ch = max(SH, ceil(SW / r))
    import math
    ch_by_cw = SW / r
    cw_by_ch = SH * r
    cw = int(math.ceil(max(SW, cw_by_ch)))
    ch = int(math.ceil(max(SH, ch_by_cw)))

    # 如果 cw > W 或 ch > H，说明原图太小不足以同时容纳该比例和人物框——此时按边界 clamp 到原图，人物可能略被切但尽量少
    if cw > W: cw = W
    if ch > H: ch = H

    # ---- 在原图内定位裁切框 cx0, cy0 ----
    # 原则:
    #  1) 尽量使人物安全框在裁切框的"期望位置"（对齐构图逻辑）
    #     wide: 人物在水平方向偏左 40%（权杖挥向右，权杖拖尾在人物左上方形成平衡，但宽屏版右边展开宇宙氛围）
    #     narrow+mobile: 人物在垂直方向略偏上（给标题留下方空间）+ 水平严格居中
    #     board: 尽量向左右两边展开更多背景（宽屏且宏大）
    #     square/mid_portrait: 人物大致居中
    #  2) 硬约束: cx0 <= sx0 且 cy0 <= sy0 且 cx0+cw >= sx1 且 cy0+ch >= sy1

    # 先给默认值：严格保证人物完整，人物在裁切框中的位置是保守居中安全版
    # 在满足 cx0 <= sx0 的前提下，cx0 尽量大（左边不要空太多）
    # 同样 cx0 + cw >= sx1 → cx0 >= sx1 - cw
    # 所以 cx0 的可行区间：[sx1 - cw, sx0]
    cx_min = sx1 - cw   # 再小 sx1 就露不进去了（右边不够）
    cx_max = sx0        # 再大 sx0 就被切了（左边不够）
    cy_min = sy1 - ch
    cy_max = sy0
    # clamp 到 [0, W-cw] / [0, H-ch]
    cx_min = max(0, min(cx_min, W - cw))
    cx_max = max(0, min(cx_max, W - cw))
    cy_min = max(0, min(cy_min, H - ch))
    cy_max = max(0, min(cy_max, H - ch))
    if cx_max < cx_min: cx_min = cx_max = (cx_min + cx_max)//2
    if cy_max < cy_min: cy_min = cy_max = (cy_min + cy_max)//2

    # 现在根据构图逻辑取 cx 在 [cx_min,cx_max] 区间中的位置
    # 人物框人物水平中心 sxc = (sx0+sx1)/2；裁切框中心 cxc = cx0 + cw/2
    # "期望 cxc 相对位置"：
    #   wide / board: 期望人物在裁切框水平偏左（40% 处左右），即 cxc ≈ cx0 + cw*0.45
    #                 → 推出 cx0 ≈ sxc - cw * 0.45
    #                 在可行区间 [cx_min, cx_max] 内夹取
    #   narrow / mid_portrait: 期望人物水平居中，即 cxc = sxc
    #                 → 推出 cx0 ≈ sxc - cw * 0.5，夹取
    #   垂直方向：
    #   narrow+mobile / mid_portrait+mobile / square+mobile: 人物在裁切框垂直 40% 处（偏上留标题位）
    #                 → cy0 ≈ syc - ch * 0.42
    #   wide / board / 非手机端 portrait: 人物垂直居中
    #                 → cy0 ≈ syc - ch * 0.50
    sxc = (sx0 + sx1) / 2.0
    syc = (sy0 + sy1) / 2.0

    # ---- 水平偏移策略 ----
    if layout in ("wide", "board"):
        ideal_cx = sxc - cw * 0.44  # 人物偏左 44% 处，权杖光迹向右引导视觉
    elif "mobile" in layout:
        ideal_cx = sxc - cw * 0.50  # 手机端水平居中以保证边缘安全区
    else:
        ideal_cx = sxc - cw * 0.50  # 其它严格居中

    # ---- 垂直偏移策略 ----
    if "mobile" in layout:
        ideal_cy = syc - ch * 0.42  # 手机端人物偏上，预留文案区
    elif layout in ("narrow",):
        ideal_cy = syc - ch * 0.47  # 竖版线下物料人物稍偏上
    elif layout in ("wide", "board"):
        ideal_cy = syc - ch * 0.50  # 横版宽屏垂直居中
    else:
        ideal_cy = syc - ch * 0.48  # square / mid_portrait 略偏上

    cx0 = int(round(ideal_cx))
    cy0 = int(round(ideal_cy))

    # ---- 夹到安全可行区间（最重要的硬约束） ----
    cx0 = max(cx_min, min(cx_max, cx0))
    cy0 = max(cy_min, min(cy_max, cy0))

    cx1 = cx0 + cw
    cy1 = cy0 + ch

    # ---- 边界 clamp ----
    if cx1 > W: cx0 = W - cw; cx1 = W
    if cy1 > H: cy0 = H - ch; cy1 = H
    cx0 = max(0, cx0); cy0 = max(0, cy0)

    # 最后断言人物框完整
    assert cx0 <= sx0, f"人物左侧越界 cx0={cx0} > sx0={sx0}"
    assert cy0 <= sy0, f"人物顶部越界 cy0={cy0} > sy0={sy0}"
    assert cx1 >= sx1, f"人物右侧越界 cx1={cx1} < sx1={sx1}"
    assert cy1 >= sy1, f"人物底部越界 cy1={cy1} < sy1={sy1}"

    cropped = img.crop((cx0, cy0, cx1, cy1))
    return cropped, (cx0, cy0, cx1, cy1)


def pick_source_image():
    """从 assets/ 自动选主视觉母版图（源头底图）作为裁切源。
    优先匹配用户上传的常见命名（含「节点/KV/主视觉/key/visual」等关键词），排除输出类文件（kv_*、_debug*、*总览*、*预览*、*Overview*）。
    """
    # 黑名单（裁切脚本本身的输出物）
    BLACKLIST_PREFIX = ("kv_", "_debug")
    BLACKLIST_SUBSTR = ("总览", "预览", "Overview", "物料索引", "物料清单")
    cands = []
    for fn in os.listdir(ASSETS_DIR):
        if not fn.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue
        low = fn
        skip = False
        for p in BLACKLIST_PREFIX:
            if fn.startswith(p):
                skip = True; break
        if not skip:
            for s in BLACKLIST_SUBSTR:
                if s in low:
                    skip = True; break
        if skip:
            continue
        p = os.path.join(ASSETS_DIR, fn)
        try:
            sz = os.path.getsize(p)
        except OSError:
            continue
        # 加分项：文件名中含 KV/主视觉/节点/Key/Visual 等关键词，作为母版可能性更高
        score = sz
        keywords = ("节点", "kv", "key", "visual", "主视觉", "母版", "源头", "original", "source")
        for kw in keywords:
            if kw.lower() in fn.lower():
                score += 50 * 1024 * 1024  # 加 50MB 虚分，强制选为源
        cands.append((score, p))
    if not cands:
        print("❌ assets/ 目录中未找到主视觉源图，请先放入 KV 文件")
        sys.exit(1)
    cands.sort(reverse=True)
    return cands[0][1]


def main():
    src_path = pick_source_image()
    print(f"📷 主视觉母版: {os.path.basename(src_path)}")
    img = Image.open(src_path).convert("RGB")
    W, H = img.size
    print(f"   尺寸: {W}×{H}   比例: {W/H:.4f}")

    sx0, sy0, sx1, sy1 = load_subject_bbox(W, H)
    SW, SH = sx1-sx0, sy1-sy0
    print(f"🔒 人物安全框: [{sx0},{sy0}]~[{sx1},{sy1}]   {SW}×{SH}   占比 {SW/W:.1%}×{SH/H:.1%}")

    ok = 0
    for num, code, name, ratio, isz, out_fn, layout in MATERIALS:
        out_path = os.path.join(ASSETS_DIR, out_fn)
        try:
            cropped, (cx0, cy0, cx1, cy1) = subject_preserving_crop(img, ratio, layout, sx0, sy0, sx1, sy1)
        except AssertionError as e:
            print(f"❌ {num} {name:<14}: 裁切约束失败 - {e}")
            continue
        cw, ch = cropped.size
        # 校验实际比例
        actual_r = cw / ch
        ratio_err = abs(actual_r - ratio) / ratio
        # 校验人物完整
        assert cx0 <= sx0 and cy0 <= sy0 and cx1 >= sx1 and cy1 >= sy1, f"{name} 裁切后人物框不完整!"
        cropped.save(out_path, "PNG", optimize=True)
        print(f"✅ {num} {name:<14} ratio={ratio:.4f} (err {ratio_err:.3%})  {cw}×{ch}  取景 [{cx0},{cy0}]~[{cx1},{cy1}]  layout={layout}")
        ok += 1

    print(f"\n🎉 {ok}/{len(MATERIALS)} 张物料保存完成 → {ASSETS_DIR}")


if __name__ == "__main__":
    main()
