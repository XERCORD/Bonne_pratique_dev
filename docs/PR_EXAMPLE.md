# Exemple de Pull Request

## 📋 Titre de la PR

```
feat: ajout du support des remises par catégorie de produit
```

## 🎯 Description

Cette PR ajoute la possibilité d'appliquer des remises spécifiques à certaines catégories de produits.

### Contexte

Actuellement, les remises s'appliquent à tout le panier. Il serait utile de pouvoir créer des remises qui ne s'appliquent qu'à certaines catégories (ex: "10% sur tous les produits électroniques").

### Changements

- Ajout du champ `category` optionnel dans le modèle `Discount`
- Modification de `Discount.calculate_discount()` pour prendre en compte la catégorie
- Mise à jour de `CheckoutService` pour filtrer les articles selon la catégorie de la remise
- Ajout de tests unitaires pour ce nouveau comportement

## 🔍 Détails techniques

### Fichiers modifiés

- `src/models/discount.py` : Ajout du champ `category` et logique de filtrage
- `src/services/checkout_service.py` : Filtrage des articles par catégorie
- `tests/test_models.py` : Tests pour les remises par catégorie
- `tests/test_services.py` : Tests d'intégration

### Exemple d'utilisation

```python
# Remise de 10% uniquement sur les produits électroniques
discount = Discount(
    code="ELECTRO10",
    discount_type=DiscountType.PERCENTAGE,
    value=Decimal("10"),
    category="electronics"
)
```

## ✅ Checklist

- [x] Code conforme aux standards (black, flake8, mypy)
- [x] Tests unitaires ajoutés et passent
- [x] Tests d'intégration ajoutés et passent
- [x] Documentation mise à jour
- [x] Pas de régression (tous les tests existants passent)
- [x] Logs appropriés ajoutés

## 🧪 Tests

### Tests ajoutés

- `test_discount_with_category()` : Vérifie qu'une remise avec catégorie ne s'applique qu'aux produits de cette catégorie
- `test_checkout_with_category_discount()` : Test d'intégration complet

### Résultats

```
tests/test_models.py::TestDiscount::test_discount_with_category PASSED
tests/test_services.py::TestCheckoutService::test_checkout_with_category_discount PASSED
```

## 📸 Screenshots (si applicable)

N/A pour cette PR (changements backend uniquement)

## 🔗 Issues liées

Closes #2

## 👥 Reviewers

@reviewer1 @reviewer2

---

## 📝 Notes pour les reviewers

Points d'attention :
1. La logique de filtrage dans `CheckoutService` - est-ce la bonne approche ?
2. Le comportement quand une remise avec catégorie est appliquée à un panier mixte
3. Performance : est-ce que le filtrage est efficace pour de gros paniers ?

