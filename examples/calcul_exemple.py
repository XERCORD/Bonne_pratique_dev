"""
Exemple de calcul des taxes et remises.

Ce script démontre comment fonctionne le système de calcul
des taxes et remises avec différents scénarios.
"""

from decimal import Decimal

from src.models.cart import Cart
from src.models.discount import Discount, DiscountType
from src.models.product import Product
from src.services.checkout_service import CheckoutService
from src.services.tax_calculator import TaxCalculator


def print_separator(title: str = ""):
    """Affiche un séparateur visuel."""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    print()


def print_calculation_details(result: dict, title: str = "Détails du calcul"):
    """Affiche les détails d'un calcul."""
    print(f"\n{title}:")
    print("-" * 50)
    print(f"  Sous-total (avant remise)    : {result['subtotal']:>10.2f} €")
    print(f"  Remise appliquée             : {result['discount_amount']:>10.2f} €")
    print(f"  Sous-total (après remise)    : {result['subtotal_after_discount']:>10.2f} €")
    print(f"  Taxes                       : {result['tax_amount']:>10.2f} €")
    print(f"  {'TOTAL À PAYER':<30} : {result['total']:>10.2f} €")
    print("-" * 50)


def scenario_1_sans_remise():
    """Scénario 1 : Achat sans remise."""
    print_separator("SCÉNARIO 1 : Achat sans remise")

    # Configuration des taxes
    tax_rates = {
        "electronics": Decimal("0.20"),  # 20% pour l'électronique
        "food": Decimal("0.10"),  # 10% pour la nourriture
    }
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)

    # Création du panier
    cart = Cart()
    cart.add_item(
        Product(id="laptop", name="Laptop", price=Decimal("999.99"), category="electronics"),
        quantity=1,
    )
    cart.add_item(
        Product(id="apple", name="Pomme", price=Decimal("1.50"), category="food"),
        quantity=3,
    )

    print("Panier :")
    print("  - 1x Laptop (999.99 €) - Électronique")
    print("  - 3x Pomme (1.50 €) - Nourriture")

    # Calcul
    result = checkout_service.calculate_total(cart)

    print_calculation_details(result)


def scenario_2_remise_pourcentage():
    """Scénario 2 : Remise en pourcentage."""
    print_separator("SCÉNARIO 2 : Remise en pourcentage (10%)")

    tax_rates = {"electronics": Decimal("0.20")}
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)

    cart = Cart()
    cart.add_item(
        Product(id="laptop", name="Laptop", price=Decimal("1000"), category="electronics"),
        quantity=1,
    )

    # Remise de 10%
    discount = Discount(
        code="SAVE10", discount_type=DiscountType.PERCENTAGE, value=Decimal("10")
    )

    print("Panier :")
    print("  - 1x Laptop (1000.00 €)")
    print(f"\nRemise : {discount.code} - {discount.value}%")

    result = checkout_service.calculate_total(cart, discount)

    print_calculation_details(result)
    print(f"\nÉconomie réalisée : {result['discount_amount']:.2f} €")


def scenario_3_remise_fixe():
    """Scénario 3 : Remise fixe."""
    print_separator("SCÉNARIO 3 : Remise fixe (50 €)")

    tax_rates = {"electronics": Decimal("0.20")}
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)

    cart = Cart()
    cart.add_item(
        Product(id="laptop", name="Laptop", price=Decimal("1000"), category="electronics"),
        quantity=1,
    )

    # Remise fixe de 50€
    discount = Discount(
        code="SAVE50", discount_type=DiscountType.FIXED, value=Decimal("50")
    )

    print("Panier :")
    print("  - 1x Laptop (1000.00 €)")
    print(f"\nRemise : {discount.code} - {discount.value} €")

    result = checkout_service.calculate_total(cart, discount)

    print_calculation_details(result)
    print(f"\nÉconomie réalisée : {result['discount_amount']:.2f} €")


def scenario_4_remise_avec_minimum():
    """Scénario 4 : Remise avec montant minimum."""
    print_separator("SCÉNARIO 4 : Remise avec montant minimum (100 €)")

    tax_rates = {"electronics": Decimal("0.20")}
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)

    # Panier de 80€ (en dessous du minimum)
    cart = Cart()
    cart.add_item(
        Product(id="mouse", name="Souris", price=Decimal("80"), category="electronics"),
        quantity=1,
    )

    # Remise de 10% avec minimum de 100€
    discount = Discount(
        code="SAVE10MIN100",
        discount_type=DiscountType.PERCENTAGE,
        value=Decimal("10"),
        min_amount=Decimal("100"),
    )

    print("Panier :")
    print("  - 1x Souris (80.00 €)")
    print(f"\nRemise : {discount.code} - {discount.value}% (minimum {discount.min_amount} €)")

    result = checkout_service.calculate_total(cart, discount)

    print_calculation_details(result)
    if result["discount_amount"] == 0:
        print("\n⚠️  La remise n'a pas été appliquée (montant minimum non atteint)")


def scenario_5_remise_par_categorie():
    """Scénario 5 : Remise par catégorie."""
    print_separator("SCÉNARIO 5 : Remise par catégorie (électronique uniquement)")

    tax_rates = {
        "electronics": Decimal("0.20"),
        "food": Decimal("0.10"),
    }
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)

    cart = Cart()
    cart.add_item(
        Product(id="laptop", name="Laptop", price=Decimal("1000"), category="electronics"),
        quantity=1,
    )
    cart.add_item(
        Product(id="apple", name="Pomme", price=Decimal("2"), category="food"),
        quantity=5,
    )

    # Remise de 10% uniquement sur l'électronique
    discount = Discount(
        code="ELECTRO10",
        discount_type=DiscountType.PERCENTAGE,
        value=Decimal("10"),
        category="electronics",
    )

    print("Panier :")
    print("  - 1x Laptop (1000.00 €) - Électronique")
    print("  - 5x Pomme (2.00 €) - Nourriture")
    print(f"\nRemise : {discount.code} - {discount.value}% sur la catégorie '{discount.category}'")

    result = checkout_service.calculate_total(cart, discount)

    print_calculation_details(result)
    print(f"\nRemise appliquée uniquement sur l'électronique : {result['discount_amount']:.2f} €")


def scenario_6_panier_complexe():
    """Scénario 6 : Panier complexe avec plusieurs produits."""
    print_separator("SCÉNARIO 6 : Panier complexe avec plusieurs produits")

    tax_rates = {
        "electronics": Decimal("0.20"),
        "clothing": Decimal("0.15"),
        "food": Decimal("0.10"),
    }
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)

    cart = Cart()
    cart.add_item(
        Product(id="laptop", name="Laptop", price=Decimal("1200"), category="electronics"),
        quantity=1,
    )
    cart.add_item(
        Product(id="tshirt", name="T-shirt", price=Decimal("25"), category="clothing"),
        quantity=2,
    )
    cart.add_item(
        Product(id="apple", name="Pomme", price=Decimal("1.50"), category="food"),
        quantity=10,
    )

    discount = Discount(
        code="MEGA15", discount_type=DiscountType.PERCENTAGE, value=Decimal("15")
    )

    print("Panier :")
    print("  - 1x Laptop (1200.00 €) - Électronique (20% taxe)")
    print("  - 2x T-shirt (25.00 €) - Vêtements (15% taxe)")
    print("  - 10x Pomme (1.50 €) - Nourriture (10% taxe)")
    print(f"\nRemise globale : {discount.code} - {discount.value}%")

    result = checkout_service.calculate_total(cart, discount)

    print_calculation_details(result)

    # Détails par catégorie
    print("\nDétails par catégorie :")
    for item in cart.items:
        category_tax_rate = tax_rates.get(item.product.category, Decimal("0")) * 100
        print(
            f"  {item.product.name}: {item.subtotal:.2f} € "
            f"(taxe {category_tax_rate}% = {item.subtotal * category_tax_rate / 100:.2f} €)"
        )


def main():
    """Lance tous les scénarios de démonstration."""
    print("\n" + "=" * 70)
    print("  DÉMONSTRATION DU SYSTÈME DE CALCUL DES TAXES ET REMISES")
    print("=" * 70)

    try:
        scenario_1_sans_remise()
        scenario_2_remise_pourcentage()
        scenario_3_remise_fixe()
        scenario_4_remise_avec_minimum()
        scenario_5_remise_par_categorie()
        scenario_6_panier_complexe()

        print_separator("FIN DE LA DÉMONSTRATION")
        print("✅ Tous les scénarios ont été exécutés avec succès !")

    except Exception as e:
        print(f"\n❌ Erreur lors de l'exécution : {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

