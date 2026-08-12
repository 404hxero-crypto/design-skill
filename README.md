[README.md](https://github.com/user-attachments/files/30967653/README.md)
# wujie-creative · 无界创意 全域物料延展落地 Skill

> 以上传主视觉为唯一源头，按不同尺寸专属构图逻辑（窄长去左右 / 宽屏展开氛围 / 展板放大品牌符号 / 手机端聚焦主体），只裁切 + 重组 + 重排层级，禁止拉伸变形改色，一键适配线上小红书 / 抖音 / B站 / H5 / Banner + 线下海报 / 易拉宝 / 展板全套物料。

---

## 核心理念

### 三禁止（绝对不可打破）

| 原则 | 说明 |
|------|------|
| 禁止拉伸 | 不把横图压扁成竖图、不把竖图拉成宽屏 |
| 禁止变形 | 人物、道具、建筑的比例永远与主视觉一致 |
| 禁止改色 | 色彩体系、材质、色调，所有物料完全一致 |

### 三允许（所有延展仅能使用）

| 操作 | 说明 |
|------|------|
| 等比例裁切 | 按目标尺寸比例从核心画面取景 |
| 重组层级 | 元素在画面中可重新排布（但不可改比例） |
| 重排层级 | 前景 / 主体 / 背景可切换视觉层次（但不可改色） |

---

## 6 种构图逻辑

每个物料类型按其物理形态匹配专属构图引导，不能用"同一个提示词改比例"。

| 构图类型 | 适用物料 | 构图策略 |
|---------|---------|---------|
| 窄长竖版 | 抖音、H5、易拉宝、竖版海报 | 去掉左右装饰，聚焦中心主体，上下延伸氛围 |
| 中竖版 | 小红书竖图、海报 | 裁去两侧飞船建筑，主角占画面 60% |
| 方图 | 小红书方图 | 正方形居中构图，四周均匀分布元素 |
| 宽屏横版 | 公众号、B站、Banner | 横向展开左右氛围，电影级宽幅叙事感 |
| 大屏展板 | 展板 | 放大品牌符号，左右展开宏大场景 |
| 手机端 | 小红书x2、H5、抖音 | 主体占 40~60%，边缘 10% 安全区 |

---

## 11 种物料规格速览

### 线上 / 社交媒体

| 物料 | 尺寸 (px) | 比例 | image_size | 代码 | 构图类型 |
|------|----------|------|------------|------|---------|
| 公众号封面 | 900x383 | 2.35:1 | landscape_4_3 | `wechat_cover` | 宽屏横版 |
| 小红书竖图 | 1080x1440 | 3:4 | portrait_4_3 | `xhs` | 中竖版 + 手机端 |
| 小红书方图 | 1080x1080 | 1:1 | square | `xhs_square` | 方图 + 手机端 |
| 抖音封面 | 1080x1920 | 9:16 | portrait_16_9 | `douyin` | 窄长竖版 + 手机端 |
| B站封面 | 1146x717 | 16:10 | landscape_16_9 | `bilibili` | 宽屏横版 |
| H5 页面 | 750x1334 | 9:16 | portrait_16_9 | `h5` | 窄长竖版 + 手机端 |
| Banner | 1920x600 | 16:5 | landscape_16_9 | `banner` | 宽屏横版 |

### 线下 / 实体

| 物料 | 常见尺寸 | 比例 | image_size | 代码 | 构图类型 |
|------|---------|------|------------|------|---------|
| 海报 A3/A2/A1 | 297x420mm | 1:1.41 | portrait_4_3 | `poster` | 中竖版 |
| 竖版海报 | 600x900mm | 2:3 | portrait_16_9 | `poster_v` | 窄长竖版 |
| 易拉宝 | 80x200cm | 2:5 | portrait_16_9 | `rollup` | 窄长竖版 |
| 展板 | 80x120cm | 2:3 | landscape_4_3 | `board` | 大屏展板 |

---

## 安装

### 方式一：通过 Trae Skills 安装

```bash
npx skills add https://github.com/404hxero-crypto/design-skill
```

### 方式二：手动安装

将整个仓库复制到你的项目目录：

```bash
cp -r design-skill <your-project>/.TRAE/Skills/wujie-creative
```

---

## 使用

### 1. 放置主视觉母版

将你的主视觉源头图放入 `assets/` 目录。脚本会自动检测文件名含 `source / KV / 主视觉 / 节点 / Key / Visual` 等关键词的图片作为源头。

### 2. 标注人物安全框（可选但推荐）

编辑 `assets/subject_bbox.txt`，标注人物核心区域坐标：

```
safe_x0=200
safe_y0=0
safe_x1=750
safe_y1=950
```

裁切脚本会保证该区域 100% 完整，不切脸 / 帽 / 杖 / 球 / 靴 / 袍。

### 3. 一键裁切 11 种物料（兜底方案）

从已有主视觉母版按 11 种比例居中裁切，像素全部来自原图，无 AI 生成、无滤镜、无改色：

```bash
cd scripts/
python3 crop_from_source.py
```

输出 11 张 `kv_*.png` 到 `assets/` 目录。

### 4. AI 生图（按物料类型）

按物料代码生成，自动匹配比例并注入对应构图引导词：

```bash
cd scripts/
bash generate_by_material.sh "xhs" "wizard character holding magic staff with crystal ball" "output_xhs.png"
```

支持的物料代码：`wechat_cover` / `xhs` / `xhs_square` / `douyin` / `bilibili` / `h5` / `banner` / `poster` / `poster_v` / `rollup` / `board`

> 认证提示：`text_to_image` API 需要 Trae IDE 前端注入认证凭据。建议在 IDE 内使用 `<img>` 渲染方式生成，或在 IDE 终端配合 `TRAE_IDE_TOKEN` 环境变量执行脚本。

---

## 目录结构

```
design-skill/
├── .gitignore                          # 忽略 macOS/Python 缓存
├── README.md                           # 本文件
├── SKILL.MD                            # Trae Skill 定义文件（含 frontmatter）
├── assets/
│   ├── README.md                       # 物料预览索引（含 AI 生图提示词）
│   ├── source_image.jpg                # 示例主视觉母版
│   └── subject_bbox.txt                # 人物安全框坐标
├── references/
│   ├── social-media/SPEC.md            # 线上物料详细规格
│   └── physical/SPEC.md                # 线下物料详细规格
└── scripts/
    ├── crop_from_source.py             # 核心裁切脚本（人物完整约束）
    ├── generate_image.sh               # 指定比例生图脚本
    ├── generate_by_material.sh         # 按物料代码生图脚本
    └── _batch_gen.html                 # 批量生成页面
```

---

## 生图工作流

```
主视觉母版 → 分析风格 → 抽取基础提示词
                                ↓
                    匹配物料代码 → 取专属构图引导词
                                ↓
                    拼接完整提示词 = 基础风格 + 构图引导
                                ↓
                    确定 image_size → 调用生图 API
                                ↓
                    输出 11 张延展物料
```

**提示词构建公式：**

```
完整 prompt = 基础风格提示词(主体+场景+色彩+风格+光影) + ", " + 专属构图引导词
```

---

## 环境要求

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 裁切脚本 |
| Pillow | latest | 图像处理 (`pip install Pillow`) |
| Bash | any | 生图脚本 |
| Trae IDE | latest | AI 生图 API 认证 |

---

## 设计哲学

> 窄长 = 去掉左右装饰
> 宽屏 = 展开左右氛围
> 大屏展板 = 放大品牌符号
> 手机端 = 聚焦中心主体

所有衍生物料保持原图**风格、色彩、元素、比例**不变，只通过裁切 + 重组 + 重排层级适配不同尺寸。

---

## License

MIT
