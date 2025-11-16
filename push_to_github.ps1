# Script PowerShell pour pousser le projet sur GitHub

Write-Host "🚀 Initialisation et push vers GitHub" -ForegroundColor Green
Write-Host ""

# Étape 1 : Initialiser Git
Write-Host "📦 Étape 1 : Initialisation de Git..." -ForegroundColor Yellow
git init
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de l'initialisation de Git" -ForegroundColor Red
    exit 1
}

# Étape 2 : Ajouter tous les fichiers
Write-Host "📝 Étape 2 : Ajout des fichiers..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de l'ajout des fichiers" -ForegroundColor Red
    exit 1
}

# Étape 3 : Faire le commit
Write-Host "💾 Étape 3 : Création du commit..." -ForegroundColor Yellow
$commitMessage = @"
feat: système de checkout simplifié initial

- Gestion de produits avec catégories
- Système de panier d'achat
- Calcul de taxes par catégorie
- Système de remises avancé (globale, par catégorie, avec minimum)
- API REST complète
- Tests unitaires et d'intégration (8/8 tests réussis)
- Documentation complète (architecture, calculs, bug report)
- Configuration formatter/linter (black, flake8, mypy)
"@

git commit -m $commitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du commit" -ForegroundColor Red
    exit 1
}

# Étape 4 : Vérifier si le remote existe déjà
Write-Host "🔗 Étape 4 : Configuration du remote..." -ForegroundColor Yellow
$remoteExists = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "⚠️  Le remote 'origin' existe déjà. Suppression..." -ForegroundColor Yellow
    git remote remove origin
}

git remote add origin https://github.com/XERCORD/Bonne_pratique_dev.git
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de l'ajout du remote" -ForegroundColor Red
    exit 1
}

# Étape 5 : Renommer la branche en main
Write-Host "🌿 Étape 5 : Configuration de la branche main..." -ForegroundColor Yellow
git branch -M main
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  La branche est déjà 'main' ou erreur" -ForegroundColor Yellow
}

# Étape 6 : Pousser sur GitHub
Write-Host "⬆️  Étape 6 : Push vers GitHub..." -ForegroundColor Yellow
Write-Host "⚠️  Vous devrez peut-être entrer vos identifiants GitHub" -ForegroundColor Yellow
Write-Host ""
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Succès ! Le projet a été poussé sur GitHub" -ForegroundColor Green
    Write-Host "🔗 Repository : https://github.com/XERCORD/Bonne_pratique_dev" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Erreur lors du push. Vérifiez vos identifiants GitHub." -ForegroundColor Red
    Write-Host "💡 Vous pouvez aussi pousser manuellement avec : git push -u origin main" -ForegroundColor Yellow
}

