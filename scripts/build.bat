@echo off
setlocal

echo --- Starting Windows build process ---

:: 1. Create & activate virtual environment
echo --- Setting up Python virtual environment ---
if not exist venv ( py -m venv venv )
call venv\Scripts\activate

:: 2. Install dependencies
echo --- Installing dependencies from requirements.txt ---
pip install -r requirements.txt

:: 3. Run PyInstaller
echo --- Building executable with PyInstaller ---
pyinstaller --name "AI-Commit" --windowed --onefile --icon="assets/icon.ico" main.py

echo --- Executable build complete! ---
echo Executable created in the 'dist' folder.
echo.
echo To create the Windows installer (.exe), install Inno Setup from https://jrsoftware.org/isinfo.php
echo then right-click and 'Compile' the 'scripts/installer.iss' file.

endlocal
pause