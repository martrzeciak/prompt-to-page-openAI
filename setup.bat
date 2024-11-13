@echo off
REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo Setup complete!
pause