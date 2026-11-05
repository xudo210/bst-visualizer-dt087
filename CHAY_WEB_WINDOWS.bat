@echo off
cd /d "%~dp0"
echo ================================================
echo    DT087 - BST VISUALIZER (BAN CUOI)
echo ================================================
echo Neu chua cai thu vien, chay: python -m pip install -r requirements-web.txt
echo Dang khoi dong website...
python web_app.py
if errorlevel 1 (
 echo.
 echo Khong khoi dong duoc. Kiem tra Python va Flask.
 echo Thu: python -m pip install -r requirements-web.txt
)
pause
