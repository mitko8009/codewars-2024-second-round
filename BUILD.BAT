@echo off
REM Comentari za hris4o i didko :D
REM posle da nqma ama ti ne si pisal komentari

REM Check if Python Dependencies are installed
echo Checking Python Dependencies...
pip install -r requirements.txt
pip install PyQt5
pip install pyinstaller

REM BUILD the application
echo Building the application...
pyinstaller main.spec

REM Move the executable to the root directory
move .\dist\main.exe .\
rmdir .\dist /s /q
rmdir .\build /s /q

echo Build completed successfully.
pause