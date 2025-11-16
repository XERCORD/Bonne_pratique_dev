# 🛒 Checkout Simplifié

> Système de checkout simplifié avec calcul de panier, taxes et remises avancées  
> API REST développée en Python avec Flask  
> ✨ **Nouveau** : Interface web interactive, remises par catégorie, documentation complète, tests à 100%

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Testé%20et%20Validé-success.svg)](https://github.com/XERCORD/Bonne_pratique_dev)
[![License](https://img.shields.io/badge/License-Educatif-lightgrey.svg)](LICENSE)

[🔗 Repository GitHub](https://github.com/XERCORD/Bonne_pratique_dev) | [📚 Documentation](docs/ARCHITECTURE.md) | [🐛 Bug Report](docs/BUG_REPORT.md)

</div>

---

## 📑 Table des matières

| Section | Description |
|---------|-------------|
| [✅ Statut](#-statut-du-projet) | Vérifications et tests effectués |
| [🚀 Fonctionnalités](#-fonctionnalités) | Liste des fonctionnalités disponibles |
| [🌐 Interface Web](#-interface-web) | Site web interactif pour tester le checkout |
| [🏗️ Architecture](#️-architecture) | Principes et structure du projet |
| [📦 Installation](#-installation) | Guide d'installation pas à pas |
| [🎯 Utilisation](#-utilisation) | Exemples d'utilisation de l'API |
| [🧪 Tests](#-tests) | Comment lancer les tests |
| [🔍 Qualité](#-qualité-du-code) | Outils de qualité de code |
| [📝 Workflow Git](#-workflow-git) | Guide de contribution |
| [🔧 Dépannage](#-dépannage) | Solutions aux problèmes courants |
| [📚 Documentation](#-documentation) | Liens vers la documentation |

---

## ✅ Statut du projet

<div align="center">

### 🎯 Tous les composants ont été vérifiés et testés

</div>

| Composant | Status | Détails |
|-----------|--------|---------|
| **Syntaxe Python** | ✅ | Tous les fichiers compilent sans erreur |
| **Imports** | ✅ | Tous les modules s'importent correctement |
| **Structure** | ✅ | Architecture modulaire cohérente |
| **Logique métier** | ✅ | Création d'objets et calculs fonctionnent |
| **Application Flask** | ✅ | L'API peut être créée et démarrée |
| **Tests** | ✅ | **8/8 tests réussis (100%)** - Voir [Résultats](docs/TESTS_RESULTS.md) |
| **Linting** | ✅ | Aucune erreur de linting détectée |
| **Remises par catégorie** | ✅ | Fonctionnalité implémentée et testée |
| **Documentation** | ✅ | Documentation complète des calculs disponible |

### 🆕 Dernières mises à jour

- ✅ **Interface web interactive** : Site web HTML/CSS/JS pour tester le checkout sans ligne de commande
- ✅ **Script tout-en-un** : `lancer_tout.bat` pour lancer API + serveur web automatiquement
- ✅ **Configuration CORS** : Support complet des requêtes cross-origin depuis le navigateur
- ✅ **Serveur web intégré** : Serveur HTTP simple pour servir l'interface web
- ✅ **Scripts de lancement Windows** : Fichiers `.bat` pour démarrer l'API et le serveur web facilement
- ✅ **Remises par catégorie** : Les remises peuvent maintenant cibler une catégorie spécifique
- ✅ **Documentation des calculs** : Guide complet avec formules et exemples
- ✅ **Scripts de démonstration** : Exemples pratiques pour tester le système
- ✅ **Tests complets** : Suite de tests couvrant tous les cas d'usage

> 💡 **Note importante** : Pour exécuter les tests complets et lancer l'API, installez d'abord les dépendances avec `pip install -r requirements-dev.txt`

---

## 🚀 Fonctionnalités

<div align="center">

### 🎁 Ce que vous pouvez faire avec ce projet

</div>

| Fonctionnalité | Description | Endpoint |
|----------------|-------------|----------|
| 📦 **Gestion de produits** | Création et récupération de produits avec prix et catégorie | `POST /products`<br>`GET /products/{id}` |
| 🛒 **Gestion de panier** | Ajout, modification et suppression d'articles | Intégré dans `/checkout` |
| 💰 **Calcul de taxes** | Taxes configurables par catégorie avec calcul proportionnel après remise | Calculé automatiquement |
| 🎫 **Système de remises avancé** | Remises en pourcentage ou montant fixe, avec montant minimum et **remises par catégorie** | `POST /discounts` |
| 🌐 **API REST** | Endpoints pour toutes les opérations | Voir section [Utilisation](#-utilisation) |

### 🎯 Fonctionnalités avancées des remises

- ✅ **Remise globale** : S'applique à tout le panier
- ✅ **Remise par catégorie** : S'applique uniquement aux produits d'une catégorie spécifique
- ✅ **Montant minimum** : Remise conditionnelle selon le montant du panier
- ✅ **Pourcentage ou fixe** : Deux types de remises disponibles

> 📖 **Documentation complète** : Consultez [Calcul Taxes/Remises](docs/CALCUL_TAXES_REMISES.md) pour tous les détails

---

## 🌐 Interface Web

### 🎨 Site web interactif

Le projet inclut une **interface web complète** pour tester le checkout de manière visuelle et intuitive, sans avoir besoin d'utiliser `curl` ou Postman.

#### ✨ Fonctionnalités de l'interface

- 🎨 **Design moderne** : Interface en violet sombre avec un design soigné
- 📦 **Gestion de produits** : Créer des produits directement depuis l'interface
- 🎫 **Gestion de remises** : Créer des remises (pourcentage, fixe, par catégorie)
- 🛒 **Panier interactif** : Ajouter, retirer des articles du panier
- 💰 **Calcul en temps réel** : Calculer le checkout avec affichage détaillé (sous-total, remise, taxes, total)
- ⚙️ **Configuration API** : Changer l'URL de l'API facilement

#### 🚀 Utilisation rapide

**⭐ Option 1 : Script tout-en-un (Recommandé)**

Le plus simple pour démarrer :

```bash
.\lancer_tout.bat
```

Ce script lance automatiquement :
- ✅ L'API Flask sur `http://localhost:5000`
- ✅ Le serveur web sur `http://localhost:8000`
- ✅ Ouvre le navigateur automatiquement

**Option 2 : Lancer séparément**

1. **Lancer l'API** (fenêtre 1) :
   ```bash
   # Windows
   .\lancer_api.bat
   
   # Linux/Mac ou Make
   make run
   
   # Commande directe
   python -m src.main
   ```

2. **Lancer le serveur web** (fenêtre 2) :
   ```bash
   # Windows
   .\lancer_web.bat
   
   # Linux/Mac
   python serve_web.py
   ```

3. **Ouvrir dans le navigateur** :
   - `http://localhost:8000/index.html`

**Option 3 : Sans serveur web (moins recommandé)**

Si vous ouvrez `index.html` directement, assurez-vous que :
- L'API est lancée sur `http://localhost:5000`
- CORS est activé (inclus automatiquement)

#### 📁 Fichiers de l'interface

| Fichier | Description |
|---------|-------------|
| `index.html` | Page principale avec toutes les sections |
| `styles.css` | Styles en violet sombre |
| `app.js` | Logique JavaScript pour interagir avec l'API |
| `serve_web.py` | Serveur HTTP simple pour servir l'interface web |
| `lancer_tout.bat` | ⭐ Script tout-en-un (API + serveur web) |
| `lancer_api.bat` | Script Windows pour lancer l'API (avec vérifications) |
| `lancer_api_simple.bat` | Script Windows simplifié pour lancer l'API |
| `lancer_web.bat` | Script Windows pour lancer le serveur web |

#### 🔧 Configuration CORS

L'API est configurée avec **CORS activé** pour permettre les requêtes depuis le navigateur. Le package `flask-cors` est inclus dans les dépendances.

> 💡 **Astuce** : Utilisez `lancer_tout.bat` pour un démarrage simple et automatique !
> 
> ⚠️ **Note** : Pour éviter les erreurs "Failed to fetch", utilisez le serveur web (`http://localhost:8000`) plutôt que d'ouvrir `index.html` directement.

---

## 🏗️ Architecture

<div align="center">

### 🎨 Principes de conception appliqués

</div>

| Principe | Description | Application |
|----------|-------------|-------------|
| **KISS** | Keep It Simple, Stupid | Solutions simples, pas d'usine à gaz |
| **DRY** | Don't Repeat Yourself | Factorisation pour une seule source de vérité |
| **YAGNI** | You Aren't Gonna Need It | Pas de fonctionnalités anticipées non utilisées |
| **SOLID** | Principes SOLID | Séparation des responsabilités, chaque module a un rôle unique |

📖 **Pour plus de détails** : Consultez la [Note d'architecture](docs/ARCHITECTURE.md)

---

## 📦 Installation

### 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :

- ✅ Python 3.9 ou supérieur
- ✅ pip (gestionnaire de paquets Python)

### 🔧 Installation des dépendances

#### Option 1 : Avec Make (recommandé)

```bash
make install-dev
```

#### Option 2 : Installation manuelle

```bash
pip install -r requirements-dev.txt
```

### ✅ Vérification rapide

Après installation, vérifiez que tout fonctionne :

```bash
python -c "from src.models import Product, Cart, Discount; from src.services import CheckoutService, TaxCalculator; from src.api import create_app; print('✅ OK')"
```

> 💡 Si vous voyez `✅ OK`, tout est prêt !

---

## 🎯 Utilisation

### 🚀 Démarrer l'application

#### ⭐ Option 1 : Script tout-en-un (Recommandé)

Le plus simple pour démarrer l'API + interface web :

```bash
lancer_tout.bat
```

Ce script lance automatiquement :
- ✅ L'API Flask sur `http://localhost:5000`
- ✅ Le serveur web sur `http://localhost:8000`
- ✅ Ouvre le navigateur automatiquement

#### Option 2 : Scripts Windows (.bat)

**Lancer l'API uniquement** :
```bash
# Version complète (avec vérifications)
lancer_api.bat

# Version simple (lancement rapide)
lancer_api_simple.bat
```

**Lancer le serveur web** :
```bash
lancer_web.bat
```

> 💡 Les scripts `.bat` vérifient automatiquement Python et les dépendances, et proposent de les installer si nécessaire.

#### Option 3 : Avec Make

```bash
# Lancer l'API
make run

# Dans une autre fenêtre, lancer le serveur web
python serve_web.py
```

#### Option 4 : Commandes directes

```bash
# Fenêtre 1 : Lancer l'API
python -m src.main

# Fenêtre 2 : Lancer le serveur web
python serve_web.py
```

> 🌐 L'API sera accessible sur **http://localhost:5000**  
> 🌐 L'interface web sera accessible sur **http://localhost:8000/index.html**

> 💡 **Recommandation** : Utilisez `lancer_tout.bat` pour un démarrage simple et automatique !

---

### 🌐 Utiliser l'interface web (recommandé)

La façon la plus simple de tester le checkout est d'utiliser l'interface web :

**Méthode rapide** :
```bash
lancer_tout.bat
```
Le navigateur s'ouvrira automatiquement sur `http://localhost:8000/index.html`

**Méthode manuelle** :
1. Lancez l'API (voir section [Démarrer l'application](#-démarrer-lapplication))
2. Lancez le serveur web : `lancer_web.bat` ou `python serve_web.py`
3. Ouvrez `http://localhost:8000/index.html` dans votre navigateur
4. Allez dans la section "🧪 Tester"
5. Suivez les instructions à l'écran

> 💡 L'interface web permet de tester toutes les fonctionnalités sans ligne de commande !  
> ⚠️ **Important** : Utilisez `http://localhost:8000/index.html` plutôt que d'ouvrir `index.html` directement pour éviter les erreurs CORS.

### 📝 Exemples d'utilisation (API REST)

#### 1️⃣ Créer un produit

```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "id": "prod1",
    "name": "Laptop",
    "price": "999.99",
    "category": "electronics"
  }'
```

**Réponse attendue :**
```json
{
  "id": "prod1",
  "name": "Laptop"
}
```

---

#### 2️⃣ Récupérer un produit

```bash
curl http://localhost:5000/products/prod1
```

**Réponse attendue :**
```json
{
  "id": "prod1",
  "name": "Laptop",
  "price": "999.99",
  "category": "electronics"
}
```

---

#### 3️⃣ Créer une remise

**Remise globale (10%) :**
```bash
curl -X POST http://localhost:5000/discounts \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SAVE10",
    "type": "percentage",
    "value": "10"
  }'
```

**Remise par catégorie (10% sur électronique uniquement) :**
```bash
curl -X POST http://localhost:5000/discounts \
  -H "Content-Type: application/json" \
  -d '{
    "code": "ELECTRO10",
    "type": "percentage",
    "value": "10",
    "category": "electronics"
  }'
```

**Remise avec montant minimum (10% si panier >= 100€) :**
```bash
curl -X POST http://localhost:5000/discounts \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SAVE10MIN100",
    "type": "percentage",
    "value": "10",
    "min_amount": "100"
  }'
```

**Réponse attendue :**
```json
{
  "code": "SAVE10"
}
```

---

#### 4️⃣ Calculer le checkout

```bash
curl -X POST http://localhost:5000/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": "prod1", "quantity": 2}
    ],
    "discount_code": "SAVE10"
  }'
```

**Réponse attendue :**
```json
{
  "subtotal": "1999.98",
  "discount_amount": "199.998",
  "subtotal_after_discount": "1799.982",
  "tax_amount": "359.9964",
  "total": "2159.9784"
}
```

> 💡 **Note** : Les taxes sont calculées **après** l'application de la remise, proportionnellement au montant réduit.

---

## 🧪 Tests

### ▶️ Lancer les tests

#### Option 1 : Script de test complet (sans dépendances)

```bash
python test_all.py
```

> ✅ Ce script teste tous les composants sans nécessiter pytest

#### Option 2 : Avec Make (si pytest installé)

```bash
make test
```

#### Option 3 : Avec pytest directement

```bash
pytest tests/ -v
```

### 📊 Couverture de code

Générer un rapport de couverture HTML :

```bash
pytest --cov=src --cov-report=html
```

> 📁 Le rapport sera disponible dans `htmlcov/index.html`

### ✅ Résultats des tests

**Statut actuel** : ✅ **8/8 tests réussis (100%)**

| Catégorie | Tests | Statut |
|-----------|-------|--------|
| **Modèles** | Création, validation, opérations | ✅ |
| **Services** | Taxes, checkout, remises | ✅ |
| **Remises** | Pourcentage, fixe, minimum, catégorie | ✅ |
| **Cas limites** | Panier vide, validations | ✅ |

Voir [Résultats des tests](docs/TESTS_RESULTS.md) pour plus de détails.

### 🎯 Exemples de démonstration

Pour voir des exemples de calculs en action :

```bash
python examples/calcul_exemple.py
```

Ce script démontre 6 scénarios différents :
1. Achat sans remise
2. Remise en pourcentage
3. Remise fixe
4. Remise avec montant minimum
5. Remise par catégorie
6. Panier complexe avec plusieurs produits

---

## 🔍 Qualité du code

### 🛠️ Commandes disponibles

| Commande | Description | Make |
|----------|-------------|------|
| **Formatter** | Formate le code avec Black | `make format` |
| **Linting** | Vérifie le style avec Flake8 | `make lint` |
| **Types** | Vérifie les types avec MyPy | `make type-check` |
| **Tout vérifier** | Lance toutes les vérifications | `make lint format type-check test` |

### 📋 Exécution individuelle

```bash
# Formatter
black src tests

# Linting
flake8 src tests

# Types
mypy src
```

---

## 📝 Workflow Git

### 🌿 Structure des branches

| Branche | Usage |
|---------|-------|
| `main` | Branche principale (production) |
| `develop` | Branche de développement |
| `feature/*` | Nouvelles fonctionnalités |
| `fix/*` | Corrections de bugs |
| `docs/*` | Documentation uniquement |

### 🔄 Exemple de workflow

```bash
# 1. Créer une branche pour une nouvelle fonctionnalité
git checkout -b feature/ajout-remise-categorie

# 2. Faire des commits structurés
git commit -m "feat: ajout du support des remises par catégorie"

# 3. Pousser et créer une PR
git push origin feature/ajout-remise-categorie
```

### 📌 Convention de commits

| Préfixe | Usage | Exemple |
|---------|-------|--------|
| `feat:` | Nouvelle fonctionnalité | `feat: ajout calcul taxes` |
| `fix:` | Correction de bug | `fix: correction calcul remise` |
| `docs:` | Documentation | `docs: mise à jour README` |
| `test:` | Tests | `test: ajout tests checkout` |
| `refactor:` | Refactoring | `refactor: simplification service` |
| `style:` | Formatage | `style: formatage avec black` |

📖 **Pour plus de détails** : Consultez le [Guide de contribution](CONTRIBUTING.md)

---

## 📚 Documentation

| Document | Description | Lien |
|----------|-------------|------|
| **Architecture** | Découpage en responsabilités, dépendances, choix KISS/DRY/YAGNI | [📖 Voir](docs/ARCHITECTURE.md) |
| **Calcul Taxes/Remises** | Documentation complète du système de calcul avec formules et exemples | [💰 Voir](docs/CALCUL_TAXES_REMISES.md) |
| **Résultats Tests** | Résultats détaillés de tous les tests effectués | [✅ Voir](docs/TESTS_RESULTS.md) |
| **Bug Report** | Exemple de bug report avec méthode de débogage | [🐛 Voir](docs/BUG_REPORT.md) |
| **Améliorations** | Liste des améliorations possibles du projet | [🚀 Voir](docs/AMELIORATIONS_POSSIBLES.md) |
| **PR Example** | Exemple de Pull Request | [🔀 Voir](docs/PR_EXAMPLE.md) |
| **Git Workflow** | Exemple de workflow Git complet | [🌿 Voir](docs/GIT_WORKFLOW_EXAMPLE.md) |
| **Contributing** | Guide de contribution | [✍️ Voir](CONTRIBUTING.md) |
| **Guide de démarrage** | Guide de démarrage rapide et dépannage | [🚀 Voir](GUIDE_DEMARRAGE.md) |

---

## 🔧 Configuration

### 🌍 Variables d'environnement

> ℹ️ Aucune variable d'environnement requise pour le moment.

Les taux de taxe sont configurés par défaut dans `src/api/app.py`.

### 📝 Logging

Les logs sont configurés dans `src/main.py` et utilisent le niveau **INFO** par défaut.

---

## 🐛 Gestion des erreurs

Toutes les erreurs sont gérées explicitement avec :

- ✅ Retours HTTP appropriés (400, 404, 409, 500)
- ✅ Messages d'erreur clairs et explicites
- ✅ Logs actionnables avec contexte non sensible

---

## 🔧 Dépannage

### ❌ Erreur "Failed to fetch"

**Problème** : Le navigateur ne peut pas se connecter à l'API.

**Solutions** :
1. ✅ **Utilisez le script tout-en-un** : `lancer_tout.bat` (recommandé)
2. ✅ **Vérifiez que l'API est lancée** : Ouvrez `http://localhost:5000/health` dans votre navigateur
3. ✅ **Utilisez le serveur web** : Ouvrez `http://localhost:8000/index.html` au lieu d'ouvrir `index.html` directement
4. ✅ **Vérifiez que flask-cors est installé** : `pip install flask-cors==4.0.0`

### ❌ Module flask_cors not found

**Solution** :
```bash
pip install flask-cors==4.0.0
```

Ou utilisez `lancer_api.bat` qui l'installe automatiquement.

### ❌ Port 5000 ou 8000 déjà utilisé

**Solution** : Un autre programme utilise le port
- Fermez l'autre programme
- Ou modifiez les ports dans `src/main.py` (port 5000) et `serve_web.py` (port 8000)

### 📖 Guide complet

Consultez [GUIDE_DEMARRAGE.md](GUIDE_DEMARRAGE.md) pour un guide de dépannage complet.

---

## 📄 Licence

Ce projet est un projet éducatif réalisé dans le cadre d'un cours sur les bonnes pratiques de développement.

---

## 👤 Auteurs

<div align="center">

### **Romain** et **Xerly**

Projet réalisé dans le cadre du cours sur les bonnes pratiques de développement.

[🔗 Repository GitHub](https://github.com/XERCORD/Bonne_pratique_dev)

</div>

---

<div align="center">

**Fait avec ❤️ pour l'apprentissage des bonnes pratiques de développement**

[⬆️ Retour en haut](#-checkout-simplifié)

</div>
