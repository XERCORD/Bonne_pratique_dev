@echo off
chcp 65001 >nul
title Serveur Web - Interface Checkout
color 0B

echo.
echo   🌐 Lancement du serveur web...
echo   📂 http://localhost:8000/index.html
echo.
echo   Appuyez sur Ctrl+C pour arrêter
echo.

python serve_web.py

pause

