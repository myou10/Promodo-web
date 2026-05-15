@echo off
cd /d "%~dp0"
echo ===================================================
echo Dang khoi dong Smart Focus Tracker...
echo ===================================================
echo.
echo Ung dung se tu dong mo tren trinh duyet cua ban.
echo Neu khong, vui long truy cap: http://localhost:8000
echo.
echo De tat ung dung, ban chi can dong cua so bao lenh nay.
echo.
start http://localhost:8000
python -m http.server 8000
