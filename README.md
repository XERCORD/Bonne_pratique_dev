# 🛒 Checkout Simplifié

> Système de checkout simplifié avec calcul de panier, taxes et remises avancées  
> API REST développée en Python avec Flask  
> ✨ **Interface web moderne** avec design NeoGlass violet  
> ✨ Remises par catégorie, documentation complète, tests à 100%

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
| [🏗️ Architecture](#️-architecture) | Principes et structure du projet |
| [📦 Installation](#-installation) | Guide d'installation pas à pas |
| [🎯 Utilisation](#-utilisation) | Exemples d'utilisation de l'API |
| [🧪 Tests](#-tests) | Comment lancer les tests |
| [🔍 Qualité](#-qualité-du-code) | Outils de qualité de code |
| [📝 Workflow Git](#-workflow-git) | Guide de contribution |
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
| **Interface Web** | ✅ | Interface NeoGlass moderne intégrée |
| **Tests** | ✅ | **8/8 tests réussis (100%)** - Voir [Résultats](docs/TESTS_RESULTS.md) |
| **Linting** | ✅ | Aucune erreur de linting détectée |
| **Remises par catégorie** | ✅ | Fonctionnalité implémentée et testée |
| **Documentation** | ✅ | Documentation complète des calculs disponible |

### 🆕 Dernières mises à jour

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

#### Option 1 : Avec Make

```bash
make run
```

#### Option 2 : Commande directe

```bash
python -m src.main
```

> 🌐 L'application sera accessible sur **http://localhost:5000**
> 
> **Interface web** : Ouvrez votre navigateur sur http://localhost:5000 pour accéder à l'interface NeoGlass moderne avec design violet, glassmorphism et animations.

### 🎨 Interface Web

Le projet inclut maintenant une **interface web complète** avec :
- ✅ Design moderne NeoGlass violet
- ✅ Glassmorphism et effets visuels
- ✅ Mode clair/sombre
- ✅ Animations fluides
- ✅ Calcul en temps réel
- ✅ Affichage de ticket de caisse stylisé

Accédez simplement à http://localhost:5000 dans votre navigateur !

---

### 📝 Exemples d'utilisation

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
