@echo off
REM Comentari za hris4o i didko :D
REM posle da nqma ama ti ne si pisal komentari

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1

IF ERRORLEVEL 1 (
    echo PyInstaller not found. Installing PyInstaller...
    pip install pyinstaller
) ELSE (
    echo PyInstaller is already installed.
)

REM BUILD the application
pyinstaller main.spec

REM Move the executable to the root directory
move .\dist\main.exe .\
rmdir .\dist /s /q
rmdir .\build /s /q

echo Build completed successfully.
pause