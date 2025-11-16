# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère à [Semantic Versioning](https://semver.org/lang/fr/).

## 👤 Auteurs

**Romain** et **Xerly**

Projet réalisé dans le cadre du cours sur les bonnes pratiques de développement.

## [1.1.0] - 2025-01-XX

### Ajouté
- **Interface web interactive** : Site web HTML/CSS/JS pour tester le checkout sans ligne de commande
  - Design moderne en violet sombre
  - Création de produits depuis l'interface
  - Création de remises (pourcentage, fixe, par catégorie)
  - Gestion interactive du panier
  - Calcul du checkout avec affichage détaillé
  - Configuration de l'URL de l'API
- **Configuration CORS** : Support complet des requêtes cross-origin depuis le navigateur
  - Ajout de `flask-cors` dans les dépendances
  - Configuration CORS dans l'API Flask
- **Serveur web intégré** : Serveur HTTP simple (`serve_web.py`) pour servir l'interface web
  - Évite les problèmes CORS en servant le HTML via HTTP
  - Ouvre automatiquement le navigateur
- **Scripts de lancement Windows** : Fichiers `.bat` pour démarrer l'API et le serveur web facilement
  - `lancer_tout.bat` : ⭐ Script tout-en-un (API + serveur web) - Recommandé
  - `lancer_api.bat` : Version complète avec vérifications automatiques
  - `lancer_api_simple.bat` : Version simplifiée pour lancement rapide
  - `lancer_web.bat` : Script pour lancer le serveur web
- **Guide de démarrage** : `GUIDE_DEMARRAGE.md` avec guide de démarrage rapide et dépannage
  - Solutions pour l'erreur "Failed to fetch"
  - Instructions pour tous les scénarios de lancement
- Mise à jour complète de la documentation (README, PROJET_RESUME, CHANGELOG)

## [1.0.0] - 2025-01-XX

### Ajouté
- Système de gestion de produits avec catégories
- Système de panier d'achat avec ajout/modification/suppression d'articles
- Calcul de taxes configurable par catégorie de produit
- Système de remises (pourcentage ou montant fixe) avec montant minimum optionnel
- Remises par catégorie : Les remises peuvent cibler une catégorie spécifique
- API REST avec endpoints pour :
  - Création et récupération de produits
  - Création de remises
  - Calcul de checkout avec taxes et remises
- Tests unitaires pour tous les modèles et services
- Tests d'intégration pour l'API
- Configuration de formatter (black) et linter (flake8, mypy)
- Documentation complète (README, architecture, bug report)
- Scripts d'initialisation pour Linux et Windows
- Makefile pour automatiser les tâches courantes

### Sécurité
- Validation des données d'entrée dans tous les modèles
- Gestion explicite des erreurs avec messages clairs
- Logs actionnables sans données sensibles

## [Non versionné]

### Ajouté
- Structure de projet avec séparation des responsabilités
- Application des principes KISS, DRY, YAGNI
- Workflow Git documenté avec exemples
- Guide de contribution

