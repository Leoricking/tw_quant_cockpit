@echo off
REM TW Quant Cockpit v0.3.21 - Update Data
REM [!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
cd /d "%~dp0.."
echo.
echo =========================================================
echo  TW Quant Cockpit -- Update Data (v0.3.21)
echo  Research Only / Read Only / No Real Orders
echo  Production Trading: BLOCKED
echo =========================================================
echo.
python main.py update-data --mode real
echo.
pause
