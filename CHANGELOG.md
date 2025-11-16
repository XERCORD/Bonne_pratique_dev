# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère à [Semantic Versioning](https://semver.org/lang/fr/).

## 👤 Auteurs

**Romain** et **Xerly**

Projet réalisé dans le cadre du cours sur les bonnes pratiques de développement.

## [1.0.0] - 2025-01-XX

### Ajouté
- Système de gestion de produits avec catégories
- Système de panier d'achat avec ajout/modification/suppression d'articles
- Calcul de taxes configurable par catégorie de produit
- Système de remises (pourcentage ou montant fixe) avec montant minimum optionnel
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

