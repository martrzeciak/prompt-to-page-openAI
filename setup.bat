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
    echo # Environment Variables > .env
    echo Creating .env file...
) else (
    echo .env file already exists.
)

REM Check if 'output' folder exists, if not create it
if not exist output (
    echo Creating 'output' folder...
    mkdir output
) else (
    echo 'output' folder already exists.
)

REM Check if 'images' folder exists inside 'output', if not create it
if not exist output\images (
    echo Creating 'images' folder inside 'output'...
    mkdir output\images
) else (
    echo 'images' folder already exists inside 'output'.
)

echo Setup complete!