# 💰 Système de Calcul des Taxes et Remises

Ce document explique en détail comment fonctionne le système de calcul des taxes et remises dans le projet.

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Calcul des taxes](#calcul-des-taxes)
- [Système de remises](#système-de-remises)
- [Ordre de calcul](#ordre-de-calcul)
- [Exemples de calculs](#exemples-de-calculs)

---

## 🎯 Vue d'ensemble

Le système de checkout calcule le total final en suivant cet ordre :

1. **Sous-total** : Somme de tous les articles du panier
2. **Remise** : Application de la remise (si applicable)
3. **Sous-total après remise** : Sous-total moins la remise
4. **Taxes** : Calcul des taxes sur le montant après remise
5. **Total final** : Sous-total après remise + Taxes

```
Sous-total → Remise → Sous-total après remise → Taxes → Total final
```

---

## 💸 Calcul des taxes

### Principe

Les taxes sont calculées **par catégorie de produit** avec des taux configurables.

### Configuration

Les taux de taxe sont définis dans `src/api/app.py` :

```python
default_tax_rates = {
    "food": Decimal("0.10"),        # 10% pour la nourriture
    "electronics": Decimal("0.20"), # 20% pour l'électronique
    "clothing": Decimal("0.15"),  # 15% pour les vêtements
    "other": Decimal("0.18"),      # 18% par défaut
}
```

### Formule de calcul

Pour chaque article dans le panier :

```
Taxe article = (Prix × Quantité) × Taux de taxe de la catégorie
```

**Exemple** :
- Laptop : 1000€ × 1 × 20% = 200€ de taxes
- Pomme : 2€ × 5 × 10% = 1€ de taxes
- **Total taxes** : 201€

### Code source

```python
# src/services/tax_calculator.py
def calculate_tax(self, cart: Cart) -> Decimal:
    total_tax = Decimal("0")
    for item in cart.items:
        category = item.product.category
        tax_rate = self.tax_rates.get(category, Decimal("0"))
        item_tax = item.subtotal * tax_rate
        total_tax += item_tax
    return total_tax
```

### Cas particuliers

- **Catégorie inconnue** : Taux de 0% (pas de taxe)
- **Panier vide** : Taxes = 0€

---

## 🎫 Système de remises

### Types de remises

Le système supporte deux types de remises :

#### 1. Remise en pourcentage

Réduction d'un pourcentage du montant.

**Exemple** : Remise de 10% sur 1000€ = 100€ de réduction

```python
discount = Discount(
    code="SAVE10",
    discount_type=DiscountType.PERCENTAGE,
    value=Decimal("10")  # 10%
)
```

#### 2. Remise fixe

Réduction d'un montant fixe.

**Exemple** : Remise de 50€ sur 1000€ = 50€ de réduction

```python
discount = Discount(
    code="SAVE50",
    discount_type=DiscountType.FIXED,
    value=Decimal("50")  # 50€
)
```

### Options avancées

#### Montant minimum

La remise ne s'applique que si le panier atteint un montant minimum.

```python
discount = Discount(
    code="SAVE10MIN100",
    discount_type=DiscountType.PERCENTAGE,
    value=Decimal("10"),
    min_amount=Decimal("100")  # Minimum 100€
)
```

**Exemple** :
- Panier de 80€ → Remise = 0€ (minimum non atteint)
- Panier de 150€ → Remise = 15€ (10% de 150€)

#### Remise par catégorie

La remise s'applique uniquement aux produits d'une catégorie spécifique.

```python
discount = Discount(
    code="ELECTRO10",
    discount_type=DiscountType.PERCENTAGE,
    value=Decimal("10"),
    category="electronics"  # Uniquement sur l'électronique
)
```

**Exemple** :
- Panier : Laptop 1000€ (électronique) + Pomme 10€ (nourriture)
- Remise : 10% uniquement sur l'électronique = 100€ de remise
- La pomme n'est pas affectée par la remise

### Formule de calcul

#### Remise globale

```
Remise = calculate_discount(sous-total)
```

#### Remise par catégorie

```
Sous-total catégorie = Σ (articles de la catégorie)
Remise = calculate_discount(sous-total catégorie)
```

### Code source

```python
# src/models/discount.py
def calculate_discount(self, amount: Decimal) -> Decimal:
    # Vérification du montant minimum
    if self.min_amount is not None and amount < self.min_amount:
        return Decimal("0")
    
    # Calcul selon le type
    if self.discount_type == DiscountType.PERCENTAGE:
        return amount * (self.value / Decimal("100"))
    else:  # FIXED
        return min(self.value, amount)  # Ne peut pas dépasser le montant
```

---

## 🔄 Ordre de calcul

### Étape par étape

Le calcul suit toujours cet ordre :

#### 1. Calcul du sous-total

```python
subtotal = sum(item.subtotal for item in cart.items)
```

#### 2. Application de la remise

```python
if discount.category:
    # Remise par catégorie
    category_subtotal = sum(
        item.subtotal 
        for item in cart.items 
        if item.product.category == discount.category
    )
    discount_amount = discount.calculate_discount(category_subtotal)
else:
    # Remise globale
    discount_amount = discount.calculate_discount(subtotal)
```

#### 3. Sous-total après remise

```python
subtotal_after_discount = subtotal - discount_amount
```

#### 4. Calcul des taxes

Les taxes sont calculées sur le montant **après remise**, proportionnellement.

```python
# Taxes sur le montant original
tax_amount_original = tax_calculator.calculate_tax(cart)

# Application proportionnelle de la remise
if subtotal > 0:
    tax_ratio = subtotal_after_discount / subtotal
    tax_amount = tax_amount_original * tax_ratio
```

**Exemple** :
- Sous-total : 1000€
- Remise : 10% = 100€
- Sous-total après remise : 900€
- Taxes originales : 200€ (20% de 1000€)
- Taxes après remise : 180€ (200€ × 900/1000)

#### 5. Total final

```python
total = subtotal_after_discount + tax_amount
```

---

## 📊 Exemples de calculs

### Exemple 1 : Sans remise

**Panier** :
- 1x Laptop (1000€) - Électronique (20% taxe)
- 3x Pomme (1.50€) - Nourriture (10% taxe)

**Calcul** :
1. Sous-total : 1000€ + 4.50€ = 1004.50€
2. Remise : 0€
3. Sous-total après remise : 1004.50€
4. Taxes : (1000€ × 20%) + (4.50€ × 10%) = 200€ + 0.45€ = 200.45€
5. **Total** : 1004.50€ + 200.45€ = **1204.95€**

---

### Exemple 2 : Remise en pourcentage (10%)

**Panier** :
- 1x Laptop (1000€) - Électronique (20% taxe)

**Remise** : SAVE10 - 10%

**Calcul** :
1. Sous-total : 1000€
2. Remise : 10% de 1000€ = 100€
3. Sous-total après remise : 900€
4. Taxes : 200€ × (900/1000) = 180€
5. **Total** : 900€ + 180€ = **1080€**

---

### Exemple 3 : Remise fixe (50€)

**Panier** :
- 1x Laptop (1000€) - Électronique (20% taxe)

**Remise** : SAVE50 - 50€

**Calcul** :
1. Sous-total : 1000€
2. Remise : 50€
3. Sous-total après remise : 950€
4. Taxes : 200€ × (950/1000) = 190€
5. **Total** : 950€ + 190€ = **1140€**

---

### Exemple 4 : Remise par catégorie

**Panier** :
- 1x Laptop (1000€) - Électronique (20% taxe)
- 5x Pomme (2€) - Nourriture (10% taxe)

**Remise** : ELECTRO10 - 10% sur l'électronique uniquement

**Calcul** :
1. Sous-total : 1000€ + 10€ = 1010€
2. Remise : 10% de 1000€ (électronique) = 100€
   - La pomme n'est pas affectée
3. Sous-total après remise : 1010€ - 100€ = 910€
4. Taxes :
   - Électronique : 200€ × (900/1000) = 180€
   - Nourriture : 1€ (inchangé)
   - Total taxes : 181€
5. **Total** : 910€ + 181€ = **1091€**

---

### Exemple 5 : Remise avec montant minimum

**Panier** :
- 1x Souris (80€) - Électronique (20% taxe)

**Remise** : SAVE10MIN100 - 10% (minimum 100€)

**Calcul** :
1. Sous-total : 80€
2. Remise : 0€ (80€ < 100€ minimum)
3. Sous-total après remise : 80€
4. Taxes : 80€ × 20% = 16€
5. **Total** : 80€ + 16€ = **96€**

---

## 🧮 Formules récapitulatives

### Remise en pourcentage

```
Remise = Montant × (Pourcentage / 100)
```

### Remise fixe

```
Remise = min(Montant fixe, Montant du panier)
```

### Taxes après remise

```
Taxes = Taxes_originales × (Sous-total_après_remise / Sous-total_original)
```

### Total final

```
Total = Sous-total_après_remise + Taxes_après_remise
```

---

## 🧪 Tester les calculs

Pour voir des exemples de calculs en action, exécutez :

```bash
python examples/calcul_exemple.py
```

Ce script démontre tous les scénarios de calcul avec des exemples détaillés.

---

## 📝 Notes importantes

1. **Les taxes sont toujours calculées après la remise** : Cela signifie que la remise réduit également le montant des taxes.

2. **Les remises par catégorie** : Si une remise est spécifique à une catégorie, elle n'affecte que les produits de cette catégorie, mais les taxes de toutes les catégories sont recalculées proportionnellement.

3. **Précision décimale** : Tous les calculs utilisent `Decimal` pour éviter les erreurs d'arrondi.

4. **Validation** : Toutes les valeurs sont validées (prix positifs, remises entre 0-100%, etc.)

---

## 🔗 Voir aussi

- [Architecture du projet](ARCHITECTURE.md)
- [Code source du service de checkout](../src/services/checkout_service.py)
- [Code source du calculateur de taxes](../src/services/tax_calculator.py)
- [Modèle de remise](../src/models/discount.py)

