# wujie-creative · 无界创意 全域物料延展落地 Skill

> 以上传主视觉为唯一源头，按不同尺寸专属构图逻辑，只裁切+重组+重排层级，禁止拉伸变形改色，一键适配线上线下全套物料。

## ✨ 特性

- **三禁止原则**：禁止拉伸 · 禁止变形 · 禁止改色
- **三允许操作**：等比例裁切 · 重组层级 · 重排层级
- **11 种物料一键适配**：
  - 线上：公众号封面、小红书竖图/方图、抖音封面、B站封面、H5、Banner
  - 线下：海报、竖版海报、易拉宝、展板
- **6 种构图逻辑**：窄长去左右 / 宽屏展开氛围 / 方图平衡居中 / 中竖适度聚焦 / 大屏放大品牌符号 / 手机端聚焦主体
- **人物完整性硬约束**：裁切保证核心人物安全框 100% 完整

## 📦 安装

### 方式一：通过 Trae Skills 安装

```bash
npx skills add https://github.com/<your-username>/wujie-creative-skill
```

### 方式二：手动安装

将整个仓库复制到你的项目目录：

```
<your-project>/.TRAE/Skills/wujie-creative/
```

## 🚀 使用

### 快速裁切（兜底方案）

从已有的主视觉母版图按 11 种比例一键裁切：

```bash
cd scripts/
python3 crop_from_source.py
```

主视觉源图放入 `assets/` 目录，文件名含 `KV/主视觉/节点/Key/Visual` 等关键词会被自动选为源头。

### 人物安全框标注

在 `assets/subject_bbox.txt` 中手动标注人物核心区域：

```
safe_x0=200
safe_y0=0
safe_x1=750
safe_y1=950
```

### 生成全新物料（AI 生图）

按物料类型生成（自动匹配比例 + 注入构图引导词）：

```bash
cd scripts/
bash generate_by_material.sh "xhs" "wizard character holding magic staff with crystal ball" "output_xhs.png"
```

支持的物料代码：`wechat_cover` / `xhs` / `xhs_square` / `douyin` / `bilibili` / `h5` / `banner` / `poster` / `poster_v` / `rollup` / `board`

## 📁 目录结构

```
wujie-creative/
├── SKILL.md                          # Trae Skill 定义文件（含 frontmatter）
├── README.md                         # GitHub 说明文档
├── assets/                           # 主视觉源图 + 裁切输出
│   ├── source_image.jpg            # 示例主视觉母版（已压缩）
│   ├── subject_bbox.txt              # 人物安全框坐标
│   └── kv_*.png                      # 11 种裁切输出示例
├── references/
│   ├── social-media/SPEC.md          # 线上/社交媒体物料规格
│   └── physical/SPEC.md              # 线下/实体物料规格
└── scripts/
    ├── crop_from_source.py           # 核心裁切脚本（人物完整约束）
    ├── generate_image.sh             # 指定比例生图脚本
    └── generate_by_material.sh       # 按物料代码生图脚本
```

## 📐 物料规格速览

| 物料 | 尺寸 (px) | 比例 | 构图类型 |
|------|----------|------|---------|
| 公众号封面 | 900×383 | 2.35:1 | 宽屏横版 |
| 小红书竖图 | 1080×1440 | 3:4 | 中竖版 + 手机端 |
| 小红书方图 | 1080×1080 | 1:1 | 方图 + 手机端 |
| 抖音封面 | 1080×1920 | 9:16 | 窄长竖版 + 手机端 |
| B站封面 | 1146×717 | 16:10 | 宽屏横版 |
| H5 页面 | 750×1334 | 9:16 | 窄长竖版 + 手机端 |
| Banner | 1920×600 | 16:5 | 宽屏横版 |
| 海报 A3/A2/A1 | 297×420mm | 1:1.41 | 中竖版 |
| 竖版海报 | 600×900mm | 2:3 | 窄长竖版 |
| 易拉宝 | 80×200cm | 2:5 | 窄长竖版 |
| 展板 | 80×120cm | 2:3 | 大屏展板 |

## 🔧 环境要求

- Python 3.8+（裁切脚本）
  - Pillow：`python3 -m pip install Pillow`
- Bash（生图脚本）
- Trae IDE（生图 API 需要 IDE 前端注入认证凭据）

## 📜 License

MIT
