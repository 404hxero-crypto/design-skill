#!/bin/bash
# ============================================================
# 按物料类型生图 - 便捷封装脚本
# 根据物料类型自动匹配 image_size，调用 generate_image.sh
# ============================================================
#
# 用法:
#   ./generate_by_material.sh "<物料类型>" "<生图提示词>" "<输出文件名>"
#
# 物料类型与比例映射:
#   ---- 线上 / 社交媒体 ----
#   wechat_cover   公众号封面      -> landscape_4_3
#   xhs            小红书           -> portrait_4_3
#   xhs_square     小红书方图       -> square
#   douyin         抖音             -> portrait_16_9
#   bilibili       B站封面          -> landscape_16_9
#   h5             H5 页面          -> portrait_16_9
#   banner         Banner 横幅      -> landscape_16_9
#   ---- 线下 / 实体物料 ----
#   poster         海报             -> portrait_4_3
#   poster_v       竖版海报         -> portrait_16_9
#   rollup         易拉宝           -> portrait_16_9
#   board          展板             -> landscape_4_3
#
# 示例:
#   ./generate_by_material.sh "xhs" "fresh floral style product cover, pastel colors" "xhs_001"
#   ./generate_by_material.sh "poster" "brand campaign poster, bold typography, blue" "poster_a2"
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

MATERIAL_TYPE="${1:?❌ 缺少参数: 物料类型 (wechat_cover|xhs|douyin|bilibili|h5|banner|poster|rollup|board ...)}"
PROMPT="${2:?❌ 缺少参数: 生图提示词 (prompt)}"
OUTPUT_NAME="${3:-generated_image}"

# ---------- 物料类型 -> image_size 映射 ----------
get_image_size() {
  case "$1" in
    wechat_cover)  echo "landscape_4_3" ;;
    xhs)           echo "portrait_4_3" ;;
    xhs_square)    echo "square" ;;
    douyin)        echo "portrait_16_9" ;;
    bilibili)      echo "landscape_16_9" ;;
    h5)            echo "portrait_16_9" ;;
    banner)        echo "landscape_16_9" ;;
    banner_sq)     echo "square_hd" ;;
    poster)        echo "portrait_4_3" ;;
    poster_v)      echo "portrait_16_9" ;;
    rollup)        echo "portrait_16_9" ;;
    board)         echo "landscape_4_3" ;;
    *)             echo "" ;;
  esac
}

IMAGE_SIZE=$(get_image_size "$MATERIAL_TYPE")

if [ -z "$IMAGE_SIZE" ]; then
  echo "❌ 未知物料类型: $MATERIAL_TYPE"
  echo "   支持的类型: wechat_cover xhs xhs_square douyin bilibili h5 banner poster poster_v rollup board"
  exit 1
fi

echo "🎯 物料类型: $MATERIAL_TYPE  ->  比例: $IMAGE_SIZE"
echo "----------------------------------------"

# ---------- 调用主生图脚本 ----------
bash "${SCRIPT_DIR}/generate_image.sh" "$PROMPT" "$IMAGE_SIZE" "$OUTPUT_NAME"
