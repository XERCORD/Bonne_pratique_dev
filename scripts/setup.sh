#!/bin/bash
# Script d'initialisation du projet

set -e

echo "🚀 Initialisation du projet Checkout..."

# Créer un environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python -m venv venv

# Activer l'environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements-dev.txt

# Vérifier le code
echo "🔍 Vérification du code..."
make lint || echo "⚠️  Des erreurs de linting ont été détectées"
make type-check || echo "⚠️  Des erreurs de type ont été détectées"

# Lancer les tests
echo "🧪 Lancement des tests..."
make test

echo "✅ Projet initialisé avec succès !"
echo "Pour démarrer l'application : make run"

