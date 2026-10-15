#!/usr/bin/env bash
# AI CPB Agent - macOS / Linux Skill Installer

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="$SCRIPT_DIR/.agents/skills/taiwan-invoice-deductor"
DEST_DIR="$HOME/.gemini/config/skills/taiwan-invoice-deductor"

echo "========================================================"
echo "  AI CPB Agent - 台灣營業稅進項發票申報 Skill 安裝程式"
echo "========================================================"
echo ""

if [ ! -d "$SOURCE_DIR" ]; then
    echo "[錯誤] 找不到技能原始目錄：$SOURCE_DIR"
    exit 1
fi

echo "正在將 Skill 安裝至全域目錄：$DEST_DIR ..."
mkdir -p "$HOME/.gemini/config/skills"
cp -R "$SOURCE_DIR" "$HOME/.gemini/config/skills/"

if [ $? -eq 0 ]; then
    echo ""
    echo "[成功] Skill 已成功安裝至全域設定！"
    echo "使用方法："
    echo "1. 將發票照片放入 invoices/ 資料夾"
    echo "2. 在 Gemini / Antigravity 聊天室輸入：「請幫我處理發票」"
    echo ""
else
    echo ""
    echo "[失敗] 安裝過程發生錯誤。"
    exit 1
fi
