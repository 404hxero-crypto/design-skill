#!/bin/bash
# ============================================================
# 全域物料延展 - 生图脚本
# 调用 text_to_image API 生成图片，结果保存到 assets 目录
# ============================================================
#
# ⚠️  认证说明：
#   text_to_image API 需要 IDE 前端注入的认证凭据。
#   若在无认证的终端（沙箱/SSH）执行会收到：{"code":1001,"Authentication failed"}
#   两种解决方式：
#   1. 携带 Token：执行前设置环境变量 TRAE_IDE_TOKEN 或 IDE_AUTH
#      export TRAE_IDE_TOKEN="你的 Bearer Token"
#   2. 优先使用 SKILL 内置机制：在 TRAE IDE 聊天中直接用 markdown <img> 标签引用
#      https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=...&image_size=...
#      IDE 会自动注入认证，图片真实渲染后，右键 → 存储图像到 assets/ 即可。
#
# 用法:
#   ./generate_image.sh "<生图提示词>" "<image_size>" "<输出文件名>"
#
# 参数:
#   $1 - prompt:    生图提示词（中文/英文均可，建议英文以获得更稳定效果）
#   $2 - image_size: 图片比例，可选值:
#                     square_hd | square | portrait_4_3 | portrait_16_9
#                     | landscape_4_3 | landscape_16_9
#   $3 - output:    输出文件名（不含扩展名，默认 generated_image）
#
# 示例:
#   ./generate_image.sh "brand poster, minimalist, blue tone, product center" "portrait_16_9" "poster_a1"
#   ./generate_image.sh "小红书封面，清新风格，花卉元素" "portrait_4_3" "xhs_cover"
#
# 带认证执行:
#   TRAE_IDE_TOKEN="Bearer xxxxxx" ./generate_image.sh "..." "square" "..."
# ============================================================

set -e

# ---------- 参数校验 ----------
PROMPT="${1:?❌ 缺少参数: 生图提示词 (prompt)}"
IMAGE_SIZE="${2:?❌ 缺少参数: image_size (square_hd|square|portrait_4_3|portrait_16_9|landscape_4_3|landscape_16_9)}"
OUTPUT_NAME="${3:-generated_image}"

# ---------- 路径配置 ----------
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="${SKILL_DIR}/assets"
mkdir -p "$ASSETS_DIR"

# 校验 image_size 合法性
VALID_SIZES="square_hd square portrait_4_3 portrait_16_9 landscape_4_3 landscape_16_9"
if ! echo "$VALID_SIZES" | grep -qw "$IMAGE_SIZE"; then
  echo "❌ 无效的 image_size: $IMAGE_SIZE"
  echo "   可选值: $VALID_SIZES"
  exit 1
fi

# ---------- URL 编码 prompt ----------
ENCODED_PROMPT=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$PROMPT")

# ---------- 构造请求 URL ----------
API_BASE="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"
REQUEST_URL="${API_BASE}?prompt=${ENCODED_PROMPT}&image_size=${IMAGE_SIZE}"

echo "📤 正在调用生图 API..."
echo "   image_size : $IMAGE_SIZE"
echo "   prompt     : $PROMPT"
echo "   请求 URL   : $REQUEST_URL"

# ---------- 构建 curl 认证头 ----------
AUTH_HEADER=()
if [ -n "$TRAE_IDE_TOKEN" ]; then
  AUTH_HEADER=(-H "Authorization: ${TRAE_IDE_TOKEN}")
  echo "🔐 使用 TRAE_IDE_TOKEN 认证"
elif [ -n "$IDE_AUTH" ]; then
  AUTH_HEADER=(-H "Authorization: ${IDE_AUTH}")
  echo "🔐 使用 IDE_AUTH 认证"
else
  echo "ℹ️  未设置 TRAE_IDE_TOKEN / IDE_AUTH 环境变量，若无 IDE 注入的认证，可能会返回 Authentication failed (code 1001)"
  echo "   解决方式见脚本顶部说明，或直接在 TRAE IDE 聊天中以 <img> 标签方式渲染后右键存图。"
fi

# ---------- 发送请求 ----------
OUTPUT_FILE="${ASSETS_DIR}/${OUTPUT_NAME}.png"
# -L 跟随 302 重定向；--compressed 启用压缩；--max-time 超时控制
HTTP_CODE=$(curl -sSL --compressed --max-time 120 "${AUTH_HEADER[@]}" \
  -o "$OUTPUT_FILE" -w "%{http_code}" "$REQUEST_URL" 2>&1 || true)
# 兼容旧版 curl：再次捕获真实 http_code
if [ -z "$HTTP_CODE" ] || ! [[ "$HTTP_CODE" =~ ^[0-9]+$ ]]; then
  HTTP_CODE=$(curl -sSL --compressed --max-time 120 "${AUTH_HEADER[@]}" \
    -o "$OUTPUT_FILE" -w "%{http_code}" "$REQUEST_URL")
fi

# ---------- 结果处理 ----------
if [ "$HTTP_CODE" = "200" ]; then
  # 检查返回的是图片还是 JSON（错误信息）
  FILE_TYPE=$(file -b --mime-type "$OUTPUT_FILE")
  if echo "$FILE_TYPE" | grep -q "image"; then
    echo "✅ 生图成功！"
    echo "   📁 文件路径: $OUTPUT_FILE"
    echo "   📐 MIME 类型: $FILE_TYPE"
  else
    # 可能是 JSON 响应（含图片 URL 或错误）
    echo "⚠️  返回内容非图片，可能是 JSON 响应，内容如下："
    cat "$OUTPUT_FILE"
    echo ""
    # 尝试提取 JSON 中的 url 字段并下载
    IMG_URL=$(python3 -c "
import json, sys
try:
    data = json.load(open('$OUTPUT_FILE'))
    if isinstance(data, dict):
        print(data.get('url') or data.get('image_url') or data.get('data', {}).get('url', ''))
except: pass
" 2>/dev/null)
    if [ -n "$IMG_URL" ]; then
      echo "🔗 检测到图片 URL，正在下载: $IMG_URL"
      curl -s -o "$OUTPUT_FILE" "$IMG_URL"
      echo "✅ 下载完成: $OUTPUT_FILE"
    else
      echo "❌ 未能从响应中解析图片 URL"
      exit 1
    fi
  fi
else
  echo "❌ 生图失败，HTTP 状态码: $HTTP_CODE"
  echo "   响应内容:"
  cat "$OUTPUT_FILE"
  exit 1
fi
