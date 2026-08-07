@echo off
setlocal
cd /d "%~dp0"
set PORT=8000

where py >nul 2>&1
if %errorlevel%==0 (
  start "" "http://127.0.0.1:%PORT%/"
  py local_server.py --port %PORT% --bind 127.0.0.1
  exit /b %errorlevel%
)

where python >nul 2>&1
if %errorlevel%==0 (
  start "" "http://127.0.0.1:%PORT%/"
  python local_server.py --port %PORT% --bind 127.0.0.1
  exit /b %errorlevel%
)

echo Python was not found. Install Python to run CyberMentorTok locally.
pause
exit /b 1
