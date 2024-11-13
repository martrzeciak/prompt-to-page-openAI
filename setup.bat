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

REM Create .env file if it does not exist
if not exist .env (
    echo Creating .env file...
) else (
    echo .env file already exists.
)

echo Setup complete!
pause