@echo off
chcp 65001 >nul
title API + Serveur Web - Checkout
color 0E

echo ========================================
echo   🚀 Lancement API + Serveur Web
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: Python n'est pas installé
    pause
    exit /b 1
)

REM Vérifier flask-cors
python -c "import flask_cors" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installation de flask-cors...
    pip install flask-cors==4.0.0
)

echo.
echo ✅ Démarrage de l'API sur http://localhost:5000
echo ✅ Démarrage du serveur web sur http://localhost:8000
echo.
echo ⚠️  Appuyez sur Ctrl+C pour arrêter
echo.

REM Lancer l'API en arrière-plan
start "API Checkout" cmd /c "python -m src.main"

REM Attendre un peu pour que l'API démarre
timeout /t 2 /nobreak >nul

REM Lancer le serveur web
python serve_web.py

REM Si on arrive ici, arrêter l'API
taskkill /FI "WINDOWTITLE eq API Checkout*" /T /F >nul 2>&1

pause

