# Script PowerShell pour forcer un push sur GitHub
# ⚠️ ATTENTION : Ce script écrase l'historique sur GitHub

Write-Host "⚠️  ATTENTION : FORCE PUSH" -ForegroundColor Red
Write-Host "Cette opération va ÉCRASER l'historique sur GitHub" -ForegroundColor Yellow
Write-Host ""

# Demander confirmation
$confirmation = Read-Host "Êtes-vous sûr de vouloir continuer ? (oui/non)"
if ($confirmation -ne "oui" -and $confirmation -ne "o" -and $confirmation -ne "yes" -and $confirmation -ne "y") {
    Write-Host "❌ Opération annulée" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Choisissez le type de force push :" -ForegroundColor Cyan
Write-Host "1. Force push simple (git push -f)" -ForegroundColor White
Write-Host "2. Force push avec lease - RECOMMANDÉ (git push --force-with-lease)" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "Votre choix (1 ou 2)"

# Demander la branche
$branch = Read-Host "Nom de la branche (par défaut: main)"
if ([string]::IsNullOrWhiteSpace($branch)) {
    $branch = "main"
}

Write-Host ""
Write-Host "🚀 Force push de la branche '$branch'..." -ForegroundColor Yellow

if ($choice -eq "2") {
    # Force push avec lease (plus sûr)
    Write-Host "Utilisation de --force-with-lease (plus sûr)" -ForegroundColor Green
    git push --force-with-lease origin $branch
} else {
    # Force push simple
    Write-Host "Utilisation de -f (force simple)" -ForegroundColor Yellow
    git push -f origin $branch
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Force push réussi !" -ForegroundColor Green
    Write-Host "🔗 Repository : https://github.com/XERCORD/Bonne_pratique_dev" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Erreur lors du force push" -ForegroundColor Red
    Write-Host "💡 Vérifiez vos permissions et que la branche existe" -ForegroundColor Yellow
}


