@echo off
echo 正在啟動 YouTube 下載器...
echo.

REM 檢查是否安裝了 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤：未找到 Python，請先安裝 Python 3.7 或更高版本
    pause
    exit /b 1
)

REM 檢查是否安裝了 pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤：未找到 pip，請確認 Python 安裝正確
    pause
    exit /b 1
)

REM 安裝依賴
echo 正在安裝依賴套件...
pip install -r requirements.txt

REM 啟動應用
echo.
echo 正在啟動應用程式...
echo 請在瀏覽器中開啟 http://localhost:8501
echo.
streamlit run app.py

pause