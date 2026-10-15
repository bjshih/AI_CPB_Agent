@echo off
chcp 65001 >nul
echo ========================================================
echo   AI CPB Agent - 台灣營業稅進項發票申報 Skill 安裝程式
echo ========================================================
echo.

set "SOURCE_DIR=%~dp0.agents\skills\taiwan-invoice-deductor"
set "DEST_DIR=%USERPROFILE%\.gemini\config\skills\taiwan-invoice-deductor"

if not exist "%SOURCE_DIR%" (
    echo [錯誤] 找不到技能原始目錄：%SOURCE_DIR%
    pause
    exit /b 1
)

echo 正在將 Skill 安裝至全域目錄：%DEST_DIR% ...
if not exist "%USERPROFILE%\.gemini\config\skills" (
    mkdir "%USERPROFILE%\.gemini\config\skills"
)

xcopy /E /I /Y "%SOURCE_DIR%" "%DEST_DIR%" >nul

if %errorlevel% equ 0 (
    echo.
    echo [成功] Skill 已成功安裝至全域設定！
    echo 現在您可以在任何 Antigravity / Gemini 本機應用程式中隨時調用本技能。
    echo.
    echo 使用方法：
    echo 1. 將發票照片放入 invoices\ 資料夾
    echo 2. 在 Gemini / Antigravity 聊天室輸入：「請幫我處理發票」
    echo.
) else (
    echo.
    echo [失敗] 安裝過程發生錯誤，請檢查權限。
)

pause
