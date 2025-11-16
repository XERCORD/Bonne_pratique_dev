# Note d'Architecture

## 📐 Vue d'ensemble

Ce document décrit l'architecture du système de checkout simplifié, en expliquant les choix de conception, le découpage en responsabilités, les dépendances et l'application des principes KISS, DRY et YAGNI.

## 🏗️ Structure du projet

```
.
├── src/
│   ├── models/          # Modèles de données (Product, Cart, Discount)
│   ├── services/        # Logique métier (CheckoutService, TaxCalculator)
│   ├── api/             # Couche API REST (Flask)
│   └── main.py          # Point d'entrée
├── tests/               # Tests unitaires et d'intégration
├── docs/                # Documentation
├── configs/             # Fichiers de configuration
└── requirements.txt     # Dépendances
```

## 🎯 Découpage en responsabilités

### 1. Couche Modèles (`src/models/`)

**Responsabilité** : Représenter les entités métier et leurs validations.

- **`Product`** : Représente un produit avec ses attributs (id, nom, prix, catégorie)
- **`Cart`** : Représente un panier d'achat avec ses articles
- **`CartItem`** : Représente un article dans le panier (produit + quantité)
- **`Discount`** : Représente une remise applicable

**Principe appliqué** : **Séparation des responsabilités** - Les modèles ne contiennent que la logique de validation et de calcul simple (sous-total d'un article).

### 2. Couche Services (`src/services/`)

**Responsabilité** : Implémenter la logique métier complexe.

- **`TaxCalculator`** : Calcule les taxes applicables selon les catégories de produits
- **`CheckoutService`** : Orchestre le calcul du total final (sous-total, remise, taxes)

**Principe appliqué** : **Séparation des responsabilités** - Chaque service a une responsabilité unique et bien définie.

### 3. Couche API (`src/api/`)

**Responsabilité** : Exposer les fonctionnalités via une API REST.

- **`app.py`** : Définit les endpoints Flask et gère les requêtes HTTP
- Gestion des erreurs HTTP (400, 404, 409, 500)
- Logging des opérations

**Principe appliqué** : **Séparation des responsabilités** - La couche API ne contient pas de logique métier, elle délègue aux services.

## 🔗 Dépendances

### Graphique des dépendances

```
api/
  └──> services/
        └──> models/
```

**Règle** : Les dépendances vont toujours dans un seul sens :
- L'API dépend des services
- Les services dépendent des modèles
- Les modèles ne dépendent de rien (sauf la bibliothèque standard)

### Détail des dépendances

1. **`api/app.py`** → **`services/checkout_service.py`**
   - Utilise `CheckoutService` pour calculer le total

2. **`api/app.py`** → **`services/tax_calculator.py`**
   - Crée une instance de `TaxCalculator` pour le passer à `CheckoutService`

3. **`services/checkout_service.py`** → **`models/cart.py`**
   - Utilise `Cart` pour accéder aux articles

4. **`services/checkout_service.py`** → **`models/discount.py`**
   - Utilise `Discount` pour calculer les remises

5. **`services/tax_calculator.py`** → **`models/cart.py`**
   - Utilise `Cart` pour itérer sur les articles et calculer les taxes

6. **`models/cart.py`** → **`models/product.py`**
   - Utilise `Product` dans `CartItem`

**Aucune dépendance circulaire** : L'architecture respecte le principe de dépendances unidirectionnelles.

## 🎨 Application des principes

### KISS (Keep It Simple, Stupid)

**Choix simples et directs** :

1. **Stockage en mémoire** : Pour la démo, les produits et remises sont stockés en mémoire. En production, on utiliserait une base de données, mais pour ce projet, c'est suffisant.

2. **Pas de framework complexe** : Utilisation de Flask (simple) plutôt que Django (plus complexe) car les besoins sont limités.

3. **Pas de design patterns complexes** : Pas de Factory, Strategy, etc. La logique est directe et lisible.

4. **Calculs simples** : Les calculs de taxes et remises sont implémentés de manière directe, sans sur-ingénierie.

**Exemple** :

```python
# Simple et direct
def calculate_tax(self, cart: Cart) -> Decimal:
    total_tax = Decimal("0")
    for item in cart.items:
        category = item.product.category
        tax_rate = self.tax_rates.get(category, Decimal("0"))
        item_tax = item.subtotal * tax_rate
        total_tax += item_tax
    return total_tax
```

### DRY (Don't Repeat Yourself)

**Factorisations effectuées** :

1. **Calcul de sous-total** : Factorisé dans `CartItem.subtotal` et `Cart.subtotal`
   - Une seule source de vérité pour le calcul

2. **Validation des modèles** : Factorisée dans `__post_init__` pour chaque modèle
   - Évite la duplication de code de validation

3. **Gestion des erreurs** : Pattern réutilisé dans tous les endpoints
   - Try/except avec logging et retour HTTP approprié

4. **Configuration des taxes** : Centralisée dans `TaxCalculator`
   - Un seul endroit pour modifier les taux

**Exemple** :

```python
# DRY : Calcul du sous-total factorisé
@property
def subtotal(self) -> Decimal:
    return self.product.price * Decimal(self.quantity)
```

### YAGNI (You Aren't Gonna Need It)

**Fonctionnalités non implémentées** (car non nécessaires) :

1. **Pas de persistance** : Pas de base de données car non requise pour la démo
2. **Pas d'authentification** : Non nécessaire pour un checkout simplifié
3. **Pas de gestion de commandes** : Seulement le calcul, pas la création de commandes
4. **Pas de gestion de stock** : Non requis pour le calcul
5. **Pas de multiples devises** : Seulement l'euro
6. **Pas de cache** : Non nécessaire pour la démo
7. **Pas de rate limiting** : Non requis pour un projet éducatif

**Ce qui est implémenté** : Exactement ce qui est nécessaire pour répondre aux exigences.

## 🔒 Gestion des erreurs

### Stratégie

1. **Validation au niveau des modèles** : Les modèles valident leurs données dans `__post_init__`
2. **Gestion explicite dans l'API** : Try/except avec logs et retours HTTP appropriés
3. **Messages d'erreur clairs** : Messages explicites pour faciliter le débogage

### Exemple

```python
try:
    product = Product(...)
except ValueError as e:
    logger.warning("Données invalides", extra={"error": str(e)})
    return jsonify({"error": str(e)}), 400
```

## 📊 Logging et observabilité

### Stratégie de logging

1. **Niveaux appropriés** :
   - `INFO` : Opérations normales (création produit, checkout)
   - `WARNING` : Erreurs de validation (champ manquant, produit non trouvé)
   - `ERROR` : Erreurs inattendues (avec `exc_info=True`)

2. **Contexte non sensible** : Les logs contiennent des IDs, pas de données sensibles

3. **Format structuré** : Utilisation de `extra` pour le contexte

### Exemple

```python
logger.info("Produit créé", extra={"product_id": product.id, "name": product.name})
logger.warning("Produit non trouvé", extra={"product_id": product_id})
```

## 🧪 Tests

### Stratégie de test

1. **Tests unitaires** : Chaque modèle et service est testé indépendamment
2. **Tests d'intégration** : Tests des endpoints API
3. **Couverture** : Objectif de couverture élevée pour la logique métier

### Organisation

- `tests/test_models.py` : Tests des modèles
- `tests/test_services.py` : Tests des services
- `tests/test_api.py` : Tests de l'API

## 🚀 Évolutivité

### Points d'extension futurs

1. **Base de données** : Remplacer le stockage en mémoire par une DB
2. **Authentification** : Ajouter JWT si nécessaire
3. **Cache** : Ajouter Redis pour les produits fréquemment consultés
4. **Queue** : Ajouter Celery pour les opérations asynchrones

### Architecture modulaire

L'architecture actuelle permet d'ajouter ces fonctionnalités sans refactoring majeur grâce à la séparation des responsabilités.

## 📝 Conclusion

Cette architecture respecte les principes demandés :
- ✅ **KISS** : Solutions simples, pas d'usine à gaz
- ✅ **DRY** : Factorisation pour une seule source de vérité
- ✅ **YAGNI** : Seulement ce qui est nécessaire
- ✅ **Séparation des responsabilités** : Chaque module a un rôle unique
- ✅ **Dépendances unidirectionnelles** : Pas de dépendances circulaires

L'architecture est maintenable, testable et évolutive.

## 👤 Auteurs

**Romain** et **Xerly**

Projet réalisé dans le cadre du cours sur les bonnes pratiques de développement.

