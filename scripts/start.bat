@echo off
setlocal

:: Start backend (Python venv + main.py) in a new window.
start "AgentOS Backend" cmd /c "cd /d "%~dp0.." && call .venv\Scripts\activate.bat && python main.py"

:: Start frontend (npm run dev) in a new window.
start "AgentOS Frontend" cmd /c "cd /d "%~dp0..\agent-ui" && npm run dev"

echo Backend and frontend started in separate windows.
echo Close those windows to stop the services, or press Ctrl+C here to exit.

:: Keep this window alive so the user has a single point of reference.
pause
