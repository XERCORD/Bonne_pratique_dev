# Architecture — Checkout NeoGlass API

## Vue d'ensemble

L'application suit une architecture modulaire inspirée du pattern MVC, avec une séparation claire des responsabilités.

## Diagramme de flux

```
┌─────────────────┐
│   Frontend      │
│  (public/)      │
│  index.html      │
│  frontend.js    │
└────────┬────────┘
         │ HTTP POST
         │ /api/checkout
         ▼
┌─────────────────┐
│   Routes        │
│ checkoutRoutes  │
│  .post('/checkout') │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Controllers    │
│checkoutController│
│  - Validation   │
│  - Logging      │
│  - Error handling│
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌─────────────────┐ ┌─────────────────┐
│   Services      │ │    Utils         │
│checkoutService  │ │  validators.js   │
│  - Calcul       │ │  - Validation   │
│  - Business     │ │  - Error format │
│    logic        │ │                 │
└─────────────────┘ └─────────────────┘
```

## Structure des dossiers

```
src/
├── app.js                 # Point d'entrée, configuration Express
├── routes/
│   └── checkoutRoutes.js  # Définition des routes API
├── controllers/
│   └── checkoutController.js  # Gestion des requêtes HTTP
├── services/
│   └── checkoutService.js    # Logique métier (calculs)
└── utils/
    ├── validators.js      # Validation centralisée
    └── logger.js          # Configuration Winston
```

## Flux de traitement d'une requête

1. **Frontend** (`public/frontend.js`)
   - Collecte les données du formulaire
   - Envoie une requête POST à `/api/checkout`

2. **Routes** (`src/routes/checkoutRoutes.js`)
   - Route `/api/checkout` → `controller.checkout`

3. **Controller** (`src/controllers/checkoutController.js`)
   - Reçoit la requête HTTP
   - Valide le payload via `validators.validateCheckoutPayload()`
   - Appelle le service `checkoutService.calculateCheckout()`
   - Log les résultats
   - Gère les erreurs et renvoie la réponse

4. **Service** (`src/services/checkoutService.js`)
   - Logique métier pure (sans dépendance HTTP)
   - Calcul du sous-total
   - Application de la remise (capped)
   - Calcul des taxes
   - Calcul du total final

5. **Utils** (`src/utils/validators.js`)
   - Validation centralisée et réutilisable
   - Vérification des types, valeurs, contraintes
   - Génération d'erreurs formatées

## Justification KISS / DRY / YAGNI

### Pourquoi un service séparé ? (KISS + DRY)

**KISS (Keep It Simple, Stupid) :**
- Le service contient uniquement la logique de calcul, sans dépendance HTTP
- Facile à comprendre et à tester isolément
- Pas de complexité inutile

**DRY (Don't Repeat Yourself) :**
- La logique de calcul est centralisée dans un seul endroit
- Réutilisable si d'autres endpoints ont besoin de calculs similaires
- Facilite la maintenance (un seul endroit à modifier)

**Exemple :**
```javascript
// ✅ Service séparé - réutilisable
const result = checkoutService.calculateCheckout(payload);

// ❌ Sans service - logique dupliquée dans chaque controller
const subtotal = items.reduce(...);
const discount = Math.min(...);
// ... répété partout
```

### Pourquoi une validation centralisée ? (DRY + KISS)

**DRY :**
- Les règles de validation sont définies une seule fois dans `validators.js`
- Réutilisables pour d'autres endpoints futurs
- Cohérence garantie dans toute l'application

**KISS :**
- Validation simple et claire, facile à comprendre
- Messages d'erreur cohérents
- Pas de validation dispersée dans plusieurs fichiers

**Exemple :**
```javascript
// ✅ Validation centralisée
validateCheckoutPayload(payload);

// ❌ Sans validation centralisée - règles dupliquées
if (!payload.items) throw new Error('...');
if (!item.name) throw new Error('...');
// ... répété dans chaque controller
```

### Pourquoi pas de base de données ? (YAGNI)

**YAGNI (You Aren't Gonna Need It) :**
- Le projet est une **démo** de bonnes pratiques, pas un système de production
- Les données sont éphémères (panier "fake")
- Pas de besoin de persistance identifié
- Ajouter une DB ajouterait de la complexité inutile

**Si besoin futur :**
- L'architecture modulaire permet d'ajouter facilement une couche de persistance
- Le service reste indépendant et peut être étendu

### Pourquoi pas de cache ? (YAGNI)

- Les calculs sont simples et rapides
- Pas de charge importante identifiée
- Ajouter un cache serait prématuré

### Pourquoi pas de microservices ? (KISS)

- L'application est simple et monolithique
- Pas de besoin de scalabilité horizontale
- Un monolithe est plus simple à maintenir pour ce cas d'usage

## Principes appliqués

### Séparation des responsabilités

- **Routes** : Définition des endpoints
- **Controllers** : Gestion HTTP, validation, logging
- **Services** : Logique métier pure
- **Utils** : Fonctions utilitaires réutilisables

### Testabilité

- Service isolé → tests unitaires faciles
- Validation centralisée → tests de validation isolés
- Pas de dépendances HTTP dans le service → tests rapides

### Maintenabilité

- Code organisé et modulaire
- Chaque fichier a une responsabilité claire
- Facile à comprendre et à modifier

## Évolutions possibles

Si le projet devait évoluer :

1. **Ajout d'une base de données**
   - Créer `src/repositories/` pour la persistance
   - Le service reste inchangé

2. **Ajout d'authentification**
   - Créer `src/middleware/auth.js`
   - Ajouter aux routes nécessaires

3. **Ajout de plusieurs endpoints**
   - Réutiliser les services et validators existants
   - Créer de nouveaux controllers/routes

L'architecture actuelle permet ces évolutions sans refactoring majeur.

