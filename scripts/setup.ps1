# Script d'initialisation du projet (PowerShell)

Write-Host "🚀 Initialisation du projet Checkout..." -ForegroundColor Green

# Créer un environnement virtuel
Write-Host "📦 Création de l'environnement virtuel..." -ForegroundColor Yellow
python -m venv venv

# Activer l'environnement virtuel
Write-Host "🔌 Activation de l'environnement virtuel..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Installer les dépendances
Write-Host "📥 Installation des dépendances..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements-dev.txt

# Vérifier le code
Write-Host "🔍 Vérification du code..." -ForegroundColor Yellow
try {
    make lint
} catch {
    Write-Host "⚠️  Des erreurs de linting ont été détectées" -ForegroundColor Red
}

try {
    make type-check
} catch {
    Write-Host "⚠️  Des erreurs de type ont été détectées" -ForegroundColor Red
}

# Lancer les tests
Write-Host "🧪 Lancement des tests..." -ForegroundColor Yellow
make test

Write-Host "✅ Projet initialisé avec succès !" -ForegroundColor Green
Write-Host "Pour démarrer l'application : make run" -ForegroundColor Cyan

