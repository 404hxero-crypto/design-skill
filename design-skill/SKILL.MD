---
name: "wujie-creative"
description: "全域物料延展落地能力：以上传主视觉为唯一源头，按不同尺寸专属构图逻辑（窄长去左右/宽屏展开氛围/展板放大品牌符号/手机端聚焦主体），只裁切+重组+重排层级，禁止拉伸变形改色，一键适配线上小红书/抖音/B站/H5/Banner+线下海报/易拉宝/展板全套物料。Invoke when user needs to extend a key visual into multi-channel materials."
---

# 无界创意 · 全域物料延展落地

## 核心理念（三禁止 + 三允许）

**以用户上传的「1 张统一风格的主视觉母版图（源头底图）」为唯一源头**，所有衍生物料保持原图**风格、色彩、元素、比例**不变。

### 🚫 三禁止原则（绝对不可打破）
- 禁止拉伸：不把横图压扁成竖图、不把竖图拉成宽屏
- 禁止变形：人物、道具、建筑的比例永远与主视觉一致
- 禁止改色：深蓝/紫/金的色彩体系、水晶材质、星空色调，所有物料完全一致

### ✅ 三允许操作（所有延展仅能使用）
- 等比例裁切：按目标尺寸比例从核心画面取景
- 重组层级：元素在画面中可重新排布（但不可改比例）
- 重排层级：前景/主体/背景可切换视觉层次（但不可改色）

---

## ⭐ 不同尺寸 · 不同构图逻辑（Skill 核心设计规则）

每个物料类型必须按其物理形态匹配专属的构图引导，不能用"同一个提示词改比例"。

| 构图类型 | 适用物料 | 构图策略 | 提示词中必须加入的构图引导词（英文） |
|---------|---------|---------|----------------------------------|
| **窄长竖版**（去掉左右装饰） | 抖音封面、H5、易拉宝、竖版海报 | 去掉左右装饰建筑/飞船，聚焦中心巫师主体 + 权杖拖尾 + 水晶球，上下延伸星空氛围填满纵向空间 | `vertical portrait composition, tight crop, focus tightly on the central wizard character, remove excessive side decorations, emphasize vertical flow of starry nebula, subject-to-frame ratio large` |
| **中竖版**（3:4 适度聚焦） | 小红书竖图、海报(A3/A2/A1) | 裁去两侧飞船建筑，主角+权杖+水晶球占画面 60%，上下留星空与水晶柱点缀 | `portrait 3:4 composition, moderately tight crop, wizard character as dominant subject, remove side spaceships, keep crystal pillars top and bottom` |
| **方图**（1:1 平衡居中） | 小红书方图 | 正方形居中构图，巫师+权杖+水晶球在中央，四周均匀分布水晶建筑、星空、飞船，四方视觉平衡 | `square centered composition, balanced framing, wizard character in absolute center, crystal architecture and spaceships evenly on four sides` |
| **宽屏横版**（展开左右氛围） | 公众号封面、B站封面、Banner | 横向展开左右宇宙氛围，左右两侧增加水晶浮空城/飞船群，巫师在中央偏左（权杖挥出轨迹引导视线右移），整体电影级宽幅叙事感 | `wide panoramic landscape composition, expand left and right cosmic atmosphere with floating crystal architecture and spaceship fleets, cinematic wide framing, wizard positioned center-left with magic trail guiding eye movement` |
| **大屏展板**（放大品牌符号） | 展板（80×120cm级） | 放大水晶球（品牌符号），左右展开宏大场景，细节更丰富，飞船、水晶柱、星辰更密集，适合远距离观看仍具冲击力 | `exhibition board layout, wide horizontal, enlarged crystal ball as brand symbol, extra detailed cosmic elements, dense crystal architecture and spaceships, grand and impactful for distant viewing` |
| **手机端**（聚焦中心主体） | 小红书×2、H5、抖音 | 主体占比大（巫师占画面 40~60%），避免小装饰干扰，边缘 10% 为安全区，关键内容绝对不碰边角 | `mobile-friendly centered composition, wizard subject prominent with 40-60 percent screen area, minimal decorative distractions, 10 percent safe margin on all sides, key content away from edges` |

> **设计哲学**：窄长 = 去掉左右装饰，宽屏 = 展开左右氛围，大屏展板 = 放大品牌符号，手机端 = 聚焦中心主体。

---

## 目录结构

```
wujie-creative/
├── SKILL.MD                          ← 本文件，总指令与构图规则
├── assets/                           ← 主视觉源文件存放处（用户上传）
├── references/
│   ├── social-media/SPEC.md          ← 线上/社交媒体物料规格
│   └── physical/SPEC.md              ← 线下/实体物料规格
└── scripts/
    ├── generate_image.sh             ← 生图主脚本（指定比例）
    ├── generate_by_material.sh       ← 按物料类型生图（自动匹配比例+注入对应构图引导词）
    └── crop_from_source.py           ← 从已有主视觉原图按11种比例居中裁切（兜底方案）
```

### assets 文件夹

`assets/` 是主视觉源文件的存放位置。**1 张统一风格的主视觉母版图（源头底图）**放置于此，所有衍生物料以此为设计基准：色彩、元素、角色比例、艺术风格。

---

## 物料适配清单（11 种 × 对应构图类型）

### 线上 / 社交媒体物料

| 物料 | 尺寸 (px) | 比例 | 生图 image_size | 物料代码 | 构图类型 |
|------|----------|------|-----------------|---------|---------|
| 公众号封面 | 900×383 | 2.35:1 | landscape_4_3 | wechat_cover | 宽屏横版（展开左右氛围） |
| 小红书竖图 | 1080×1440 | 3:4 | portrait_4_3 | xhs | 中竖版 + 手机端（适度聚焦+主体突出） |
| 小红书方图 | 1080×1080 | 1:1 | square | xhs_square | 方图（平衡居中） + 手机端 |
| 抖音/视频封面 | 1080×1920 | 9:16 | portrait_16_9 | douyin | 窄长竖版（去左右装饰） + 手机端 |
| B站封面 | 1146×717 | 16:10 | landscape_16_9 | bilibili | 宽屏横版（展开左右氛围） |
| H5 页面 | 750×1334 | 9:16 | portrait_16_9 | h5 | 窄长竖版（去左右装饰） + 手机端 |
| Banner 横幅 | 1920×600 | 16:5 | landscape_16_9 | banner | 宽屏横版（展开左右氛围） |

### 线下 / 实体物料

| 物料 | 常见尺寸 | 比例 | 生图 image_size | 物料代码 | 构图类型 |
|------|---------|------|-----------------|---------|---------|
| 海报 (A3/A2/A1) | 297×420mm 起 | 1:1.41 | portrait_4_3 | poster | 中竖版（3:4 适度聚焦） |
| 竖版海报 | 600×900mm | 2:3 | portrait_16_9 | poster_v | 窄长竖版（去左右装饰） |
| 易拉宝 | 80×200cm | 2:5 | portrait_16_9 | rollup | 窄长竖版（去左右装饰） |
| 展板（横版） | 80×120cm | 2:3 | landscape_4_3 | board | 大屏展板（放大品牌符号+左右宏大场景） |

> 详细规格见 `references/social-media/SPEC.md` 与 `references/physical/SPEC.md`

---

## 延展设计规则

### 1. 按「构图类型表」注入专属构图引导词
生成每种物料时，必须从上方「不同尺寸·不同构图逻辑」表中取出对应的英文构图引导词，拼接到基础风格提示词之后。

### 2. 版式自适应（重组/重排层级）
文字、Logo、装饰元素可重新排布，但必须：
- 使用主视觉同一色板（深蓝 #0A1128 / 紫 #7B2CBF / 金 #FFD700）
- 使用主视觉同一字体风格与字重层级
- 保持视觉层次：前景（装饰水晶）> 中景（巫师+道具）> 背景（星空+建筑），与主视觉一致

### 3. 安全区
所有物料预留 10% 边距作为安全区，关键人物主体/Logo/标题不越界。

### 4. 色彩锁定
- 所有衍生物料使用主视觉同一色板
- 线上物料：RGB 色彩模式
- 线下物料：CMYK 色彩模式，色值与主视觉绝对一致（不可因 CMYK 转印而擅自提亮/压暗）

---

## 提示词构建模板（核心：基础风格 + 专属构图引导词）

所有 11 种物料的提示词 = **基础风格提示词（固定不变，来自主视觉分析）** + **该物料专属构图引导词（从上表取，每类不同）**。

基础风格提示词通过分析 `assets/` 中的主视觉母版自动抽取，包含：
1. 主体描述（人物、服装、道具、姿态）
2. 场景描述（背景、环境、装饰元素）
3. 色彩体系（主色板 hex + 色值比例）
4. 艺术风格（C4D / 3D 渲染 / Octane / 低多边形 / 水彩 等）
5. 光影关键词（cinematic lighting / soft studio / neon glow 等）

---

## 生图工作流

### 步骤一：分析主视觉 → 抽取「基础风格提示词」

读取 `assets/` 中的主视觉母版图（用户上传），按以下维度抽取英文基础风格提示词：
```
主体描述（subject） + 场景描述（scene） + 色彩体系（colors） + 艺术风格（style） + 光影关键词（lighting）
```

### 步骤二：匹配物料代码 → 取「专属构图引导词」

根据用户需要的物料类型，从「不同尺寸·不同构图逻辑」表中取出对应英文构图引导词。

### 步骤三：拼接完整提示词

```
完整 prompt = 基础风格提示词（空格分隔） + ", " + 专属构图引导词（逗号分隔）
```

### 步骤四：确定 image_size 并生成
- 从「物料适配清单」中取对应 `image_size`
- 两种生成方式任选其一：

#### 🔹 方式 0 — 聊天 `<img>` 渲染（IDE 内推荐，自动注入认证）

```markdown
<img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={URL编码后的完整prompt}&image_size={image_size}" alt="物料名称" style="max-width:100%;">
```

生成后用户右键图片 → 存储图像 → 保存到 `assets/` 目录。

#### 🔹 方式 1 — 执行脚本

```bash
# 按物料代码生图（自动匹配 image_size + 已内置构图引导词）
bash scripts/generate_by_material.sh "<物料代码>" "<基础风格提示词>" "<输出文件名>"

# 或直接指定比例（需手动拼接构图引导词进 prompt）
bash scripts/generate_image.sh "<完整prompt>" "<image_size>" "<输出文件名>"
```

> **⚠️ 认证提示：** `text_to_image` API 需要 TRAE IDE 前端注入的认证凭据。沙箱/SSH 终端执行脚本会返回 `Authentication failed (code 1001)`，此时请使用「方式 0 聊天 `<img>` 渲染」或在 IDE 终端配合 `TRAE_IDE_TOKEN` 环境变量执行。

### 生成结果

- 脚本方式：自动保存至 `assets/`，PNG 格式
- 聊天 `<img>` 方式：IDE 窗口真实渲染，用户右键 → 存储图像 → 存到 `assets/`

> **API 端点：** `https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={prompt}&image_size={image_size}`

---

## 执行流程总结

1. **读取主视觉母版** → 从 `assets/` 获取用户上传的 1 张源头底图
2. **分析风格抽取基础提示词** → 主体/场景/色彩/艺术风格/光影
3. **确定目标物料集合** → 11 种或用户指定子集
4. **每种物料拼接：基础风格 + 专属构图引导词** → 按构图类型表注入
5. **调用生图（聊天 `<img>` 或脚本）** → image_size 对应物料比例
6. **输出 11 张延展物料** → 不变形、统一风格、完全贴合尺寸构图逻辑
