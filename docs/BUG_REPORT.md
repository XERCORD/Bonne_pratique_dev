# Bug Report : Calcul incorrect des taxes avec remise

## 📋 Informations générales

- **Titre** : Calcul incorrect des taxes lors de l'application d'une remise
- **Date de découverte** : 2025-01-XX
- **Priorité** : Haute
- **Sévérité** : Critique (affecte le calcul financier)
- **Statut** : Résolu

## 🔍 Étapes de reproduction

1. Créer un produit avec un prix de 1000€ dans la catégorie "electronics" (taux de taxe 20%)
2. Créer une remise de 10% (code "SAVE10")
3. Effectuer un checkout avec ce produit et cette remise
4. Observer le montant des taxes calculé

**Commande de reproduction** :

```bash
# 1. Créer le produit
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{"id": "prod1", "name": "Laptop", "price": "1000", "category": "electronics"}'

# 2. Créer la remise
curl -X POST http://localhost:5000/discounts \
  -H "Content-Type: application/json" \
  -d '{"code": "SAVE10", "type": "percentage", "value": "10"}'

# 3. Checkout
curl -X POST http://localhost:5000/checkout \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product_id": "prod1", "quantity": 1}], "discount_code": "SAVE10"}'
```

## ⚠️ Comportement attendu vs observé

### Comportement attendu

Les taxes devraient être calculées sur le montant **après** application de la remise :
- Sous-total : 1000€
- Remise (10%) : 100€
- Sous-total après remise : 900€
- Taxes (20% sur 900€) : 180€
- **Total : 1080€**

### Comportement observé (avant correction)

Les taxes étaient calculées sur le montant **avant** remise, puis la remise était appliquée au total :
- Sous-total : 1000€
- Taxes (20% sur 1000€) : 200€
- Total avant remise : 1200€
- Remise (10% sur 1200€) : 120€
- **Total : 1080€** ❌ (même résultat mais logique incorrecte)

**OU** dans certains cas :
- Sous-total : 1000€
- Taxes (20% sur 1000€) : 200€
- Remise (10% sur 1000€) : 100€
- **Total : 1100€** ❌ (incorrect)

## 📊 Logs et traces

### Logs avant correction

```
2025-01-XX 10:15:23 - src.api.app - INFO - Checkout calculé {"total": "1100.00"}
```

### Stack trace (si applicable)

Aucune exception levée, le bug était dans la logique métier.

## 🔬 Analyse et cause racine

### Méthode de débogage

1. **Reproduction** : Reproduction du bug avec les étapes ci-dessus
2. **Isolation** : Test unitaire créé pour isoler le problème dans `CheckoutService`
3. **Observation** : Analyse du code dans `src/services/checkout_service.py`
4. **Hypothèse** : Les taxes étaient calculées avant l'application de la remise
5. **Vérification** : Test unitaire confirmant l'hypothèse

### Cause racine

Dans `src/services/checkout_service.py`, la méthode `calculate_total` calculait les taxes sur le sous-total original, puis appliquait la remise. La logique métier correcte est :

1. Calculer le sous-total
2. Appliquer la remise
3. Calculer les taxes sur le montant après remise

**Code problématique** (avant correction) :

```python
# Calcul des taxes sur le montant original
tax_amount = self.tax_calculator.calculate_tax(cart)

# Application de la remise
discount_amount = discount.calculate_discount(subtotal)
subtotal_after_discount = subtotal - discount_amount

# Total incorrect
total = subtotal_after_discount + tax_amount  # Taxes calculées sur montant original
```

## ✅ Correctif appliqué

### Solution

Modifier la logique pour calculer les taxes proportionnellement au montant après remise :

```python
# Calcul des taxes sur le montant original
tax_amount = self.tax_calculator.calculate_tax(cart)

# Application de la remise
discount_amount = discount.calculate_discount(subtotal)
subtotal_after_discount = subtotal - discount_amount

# Ajustement proportionnel des taxes
if subtotal > 0:
    tax_ratio = subtotal_after_discount / subtotal
    tax_amount = tax_amount * tax_ratio

total = subtotal_after_discount + tax_amount
```

### Fichiers modifiés

- `src/services/checkout_service.py` : Correction de la logique de calcul

### Commit

```
fix: correction du calcul des taxes avec remise

Les taxes sont maintenant calculées proportionnellement au montant
après application de la remise, conformément à la logique métier.

Fixes #1
```

## 🧪 Tests ajoutés

### Test unitaire

Ajout d'un test dans `tests/test_services.py` :

```python
def test_calculate_total_with_percentage_discount(self):
    """Test le calcul du total avec remise en pourcentage."""
    tax_rates = {"electronics": Decimal("0.20")}
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)

    cart = Cart()
    product = Product(
        id="prod1", name="Laptop", price=Decimal("1000"), category="electronics"
    )
    cart.add_item(product, quantity=1)

    discount = Discount(
        code="SAVE10", discount_type=DiscountType.PERCENTAGE, value=Decimal("10")
    )

    result = checkout_service.calculate_total(cart, discount)

    assert result["subtotal"] == Decimal("1000")
    assert result["discount_amount"] == Decimal("100")
    assert result["subtotal_after_discount"] == Decimal("900")
    # Taxes ajustées proportionnellement: 200 * (900/1000) = 180
    assert result["tax_amount"] == Decimal("180")
    assert result["total"] == Decimal("1080")
```

### Résultat

✅ Tous les tests passent
✅ Le calcul est maintenant correct
✅ La logique métier est respectée

## 🛡️ Prévention

### Mesures préventives

1. **Tests unitaires** : Test ajouté pour couvrir ce cas d'usage
2. **Tests d'intégration** : Test API ajouté pour vérifier le comportement end-to-end
3. **Documentation** : Commentaires ajoutés dans le code pour expliquer la logique
4. **Code review** : Vérification de la logique métier lors des PRs

### Améliorations futures

- Ajouter des tests de propriétés (property-based testing) pour vérifier les invariants
- Documenter explicitement la logique métier dans la documentation API
- Ajouter des validations supplémentaires pour détecter les incohérences

## 📝 Notes supplémentaires

Ce bug a été découvert lors de l'écriture des tests unitaires. Il illustre l'importance de :
- Tester tous les cas d'usage, y compris les cas limites
- Vérifier la logique métier, pas seulement que le code fonctionne
- Documenter les règles métier pour éviter les malentendus

