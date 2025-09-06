@echo off
echo 🚀 Starting Gomin...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Run the app
echo ✨ Starting Flask app...
cd app
python app.py

pause
