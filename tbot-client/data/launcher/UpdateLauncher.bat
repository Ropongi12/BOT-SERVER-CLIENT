@echo off
color 0E
echo "Updating T-Bot Rewritten Launcher ..."

if not exist launcher.exe.new goto :end

:loop
taskkill /f /im launcher.exe
tasklist /fi "ImageName eq launcher.exe" /fo csv 2>NUL | find /I "launcher.exe">NUL
if "%ERRORLEVEL%"=="0" goto :loop

echo "Copying files ..."
copy /Y launcher.exe.new launcher.exe
del launcher.exe.new

:end
start launcher.exe