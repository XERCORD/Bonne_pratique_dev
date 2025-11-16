@echo off
chcp 65001 >nul
title API Checkout Simplifié
color 0A

echo.
echo   🚀 Lancement de l'API Checkout...
echo   🌐 http://localhost:5000
echo.
echo   Appuyez sur Ctrl+C pour arrêter
echo.

python -m src.main

pause

