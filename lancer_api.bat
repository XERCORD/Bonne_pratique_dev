@echo off
chcp 65001 >nul
echo ========================================
echo   🚀 Lancement de l'API Checkout
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python 3.9+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version
echo.

REM Vérifier si les dépendances sont installées
echo 🔍 Vérification des dépendances...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask n'est pas installé
    echo.
    set /p install="Voulez-vous installer les dépendances maintenant ? (O/N): "
    if /i "%install%"=="O" (
        echo.
        echo 📦 Installation des dépendances...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo ❌ Erreur lors de l'installation des dépendances
            pause
            exit /b 1
        )
        echo ✅ Dépendances installées avec succès
        echo.
    ) else (
        echo.
        echo ℹ️  Pour installer les dépendances manuellement, exécutez:
        echo    pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
) else (
    python -c "import flask_cors" >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  flask-cors n'est pas installé
        echo.
        echo 📦 Installation de flask-cors...
        pip install flask-cors==4.0.0
        if errorlevel 1 (
            echo ❌ Erreur lors de l'installation de flask-cors
            pause
            exit /b 1
        )
        echo ✅ flask-cors installé avec succès
        echo.
    ) else (
        echo ✅ Dépendances OK
        echo.
    )
)

REM Changer vers le répertoire du script
cd /d "%~dp0"

REM Afficher l'URL de l'API
echo ========================================
echo   🌐 API sera accessible sur:
echo   http://localhost:5000
echo ========================================
echo.
echo 💡 Pour tester l'API:
echo    1. Utilisez lancer_tout.bat pour lancer API + serveur web
echo    2. Ou ouvrez index.html via http://localhost:8000 (après lancer_web.bat)
echo    3. Ou ouvrez index.html directement dans votre navigateur
echo.
echo ⚠️  Appuyez sur Ctrl+C pour arrêter l'API
echo.
echo ========================================
echo.

REM Lancer l'API
python -m src.main

REM Si l'API s'arrête, garder la fenêtre ouverte
if errorlevel 1 (
    echo.
    echo ❌ L'API s'est arrêtée avec une erreur
    pause
)

