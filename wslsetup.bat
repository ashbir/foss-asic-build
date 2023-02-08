@ECHO OFF
TITLE Setup script for wsl2
ECHO Welcome to wsl installation. Fasten your seatbelt and here we go!
wsl --update --web-download
wsl --list --online
wsl --set-default-version 2
wsl --install -d Ubuntu-20.04 --web-download
wsl --version
ECHO.
ECHO Installation DONE. Please type `ubuntu` on the terminal.
ECHO.
PAUSE