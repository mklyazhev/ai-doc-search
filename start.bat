@echo off
echo Starting AI Document Search Assistant...

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.11 or higher
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file based on .env.example
    pause
    exit /b 1
)

echo.
echo Starting Telegram bot...
python -m src.start

pause