"""
Script de test complet pour vérifier toutes les fonctionnalités.
Ce script peut être exécuté sans pytest.
"""

import sys
from decimal import Decimal

# Ajouter le répertoire racine au path
sys.path.insert(0, '.')

from src.models.product import Product
from src.models.cart import Cart, CartItem
from src.models.discount import Discount, DiscountType
from src.services.tax_calculator import TaxCalculator
from src.services.checkout_service import CheckoutService


class Colors:
    """Codes couleur pour l'affichage."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_test(name: str):
    """Affiche le nom du test."""
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Test: {name}{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}")


def assert_test(condition: bool, message: str):
    """Affiche le résultat d'un test."""
    if condition:
        print(f"{Colors.GREEN}[OK] {message}{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[FAIL] {message}{Colors.END}")
        return False


def test_product_creation():
    """Test la création de produits."""
    print_test("Création de produits")
    
    try:
        product = Product(
            id="prod1",
            name="Laptop",
            price=Decimal("999.99"),
            category="electronics"
        )
        assert_test(product.id == "prod1", "ID du produit correct")
        assert_test(product.name == "Laptop", "Nom du produit correct")
        assert_test(product.price == Decimal("999.99"), "Prix du produit correct")
        assert_test(product.category == "electronics", "Catégorie du produit correct")
        return True
    except Exception as e:
        assert_test(False, f"Erreur: {e}")
        return False


def test_product_validation():
    """Test la validation des produits."""
    print_test("Validation des produits")
    
    tests_passed = 0
    tests_total = 0
    
    # Test prix négatif
    tests_total += 1
    try:
        Product(id="prod1", name="Test", price=Decimal("-10"), category="other")
        assert_test(False, "Prix négatif devrait lever une erreur")
    except ValueError:
        assert_test(True, "Prix négatif correctement rejeté")
        tests_passed += 1
    
    # Test ID vide
    tests_total += 1
    try:
        Product(id="", name="Test", price=Decimal("10"), category="other")
        assert_test(False, "ID vide devrait lever une erreur")
    except ValueError:
        assert_test(True, "ID vide correctement rejeté")
        tests_passed += 1
    
    return tests_passed == tests_total


def test_cart_operations():
    """Test les opérations sur le panier."""
    print_test("Opérations sur le panier")
    
    cart = Cart()
    product = Product(id="prod1", name="Test", price=Decimal("10"), category="other")
    
    # Test ajout
    cart.add_item(product, quantity=2)
    assert_test(len(cart.items) == 1, "Article ajouté au panier")
    assert_test(cart.items[0].quantity == 2, "Quantité correcte")
    assert_test(cart.subtotal == Decimal("20"), "Sous-total correct")
    
    # Test ajout du même produit
    cart.add_item(product, quantity=3)
    assert_test(cart.items[0].quantity == 5, "Quantité mise à jour")
    assert_test(cart.subtotal == Decimal("50"), "Sous-total mis à jour")
    
    # Test suppression
    cart.remove_item("prod1")
    assert_test(cart.is_empty(), "Panier vide après suppression")
    
    return True


def test_discount_calculation():
    """Test le calcul des remises."""
    print_test("Calcul des remises")
    
    # Remise en pourcentage
    discount_pct = Discount(
        code="SAVE10",
        discount_type=DiscountType.PERCENTAGE,
        value=Decimal("10")
    )
    result = discount_pct.calculate_discount(Decimal("100"))
    assert_test(result == Decimal("10"), "Remise 10% sur 100€ = 10€")
    
    # Remise fixe
    discount_fixed = Discount(
        code="SAVE50",
        discount_type=DiscountType.FIXED,
        value=Decimal("50")
    )
    result = discount_fixed.calculate_discount(Decimal("100"))
    assert_test(result == Decimal("50"), "Remise fixe 50€ sur 100€ = 50€")
    
    # Remise avec minimum
    discount_min = Discount(
        code="SAVE10MIN100",
        discount_type=DiscountType.PERCENTAGE,
        value=Decimal("10"),
        min_amount=Decimal("100")
    )
    result_low = discount_min.calculate_discount(Decimal("50"))
    assert_test(result_low == Decimal("0"), "Remise non appliquée si < minimum")
    
    result_high = discount_min.calculate_discount(Decimal("150"))
    assert_test(result_high == Decimal("15"), "Remise appliquée si >= minimum")
    
    return True


def test_tax_calculator():
    """Test le calculateur de taxes."""
    print_test("Calculateur de taxes")
    
    tax_rates = {
        "electronics": Decimal("0.20"),
        "food": Decimal("0.10"),
    }
    calculator = TaxCalculator(tax_rates)
    
    cart = Cart()
    product1 = Product(
        id="prod1", name="Laptop", price=Decimal("1000"), category="electronics"
    )
    product2 = Product(id="prod2", name="Apple", price=Decimal("2"), category="food")
    cart.add_item(product1, quantity=1)
    cart.add_item(product2, quantity=5)
    
    tax = calculator.calculate_tax(cart)
    # 1000 * 0.20 + 10 * 0.10 = 200 + 1 = 201
    assert_test(tax == Decimal("201"), "Calcul taxes multiple catégories")
    
    return True


def test_checkout_service():
    """Test le service de checkout."""
    print_test("Service de checkout")
    
    tax_rates = {"electronics": Decimal("0.20")}
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)
    
    cart = Cart()
    product = Product(
        id="prod1", name="Laptop", price=Decimal("1000"), category="electronics"
    )
    cart.add_item(product, quantity=1)
    
    # Test sans remise
    result = checkout_service.calculate_total(cart)
    assert_test(result["subtotal"] == Decimal("1000"), "Sous-total sans remise")
    assert_test(result["discount_amount"] == Decimal("0"), "Pas de remise")
    assert_test(result["tax_amount"] == Decimal("200"), "Taxes 20%")
    assert_test(result["total"] == Decimal("1200"), "Total sans remise")
    
    # Test avec remise pourcentage
    discount = Discount(
        code="SAVE10",
        discount_type=DiscountType.PERCENTAGE,
        value=Decimal("10")
    )
    result = checkout_service.calculate_total(cart, discount)
    assert_test(result["subtotal"] == Decimal("1000"), "Sous-total")
    assert_test(result["discount_amount"] == Decimal("100"), "Remise 10%")
    assert_test(result["subtotal_after_discount"] == Decimal("900"), "Après remise")
    assert_test(result["tax_amount"] == Decimal("180"), "Taxes ajustées")
    assert_test(result["total"] == Decimal("1080"), "Total avec remise")
    
    return True


def test_checkout_with_category_discount():
    """Test checkout avec remise par catégorie."""
    print_test("Checkout avec remise par catégorie")
    
    tax_rates = {
        "electronics": Decimal("0.20"),
        "food": Decimal("0.10"),
    }
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)
    
    cart = Cart()
    product1 = Product(
        id="prod1", name="Laptop", price=Decimal("1000"), category="electronics"
    )
    product2 = Product(id="prod2", name="Apple", price=Decimal("10"), category="food")
    cart.add_item(product1, quantity=1)
    cart.add_item(product2, quantity=1)
    
    # Remise uniquement sur électronique
    discount = Discount(
        code="ELECTRO10",
        discount_type=DiscountType.PERCENTAGE,
        value=Decimal("10"),
        category="electronics"
    )
    
    result = checkout_service.calculate_total(cart, discount)
    assert_test(result["subtotal"] == Decimal("1010"), "Sous-total")
    assert_test(result["discount_amount"] == Decimal("100"), "Remise sur électronique uniquement")
    assert_test(result["subtotal_after_discount"] == Decimal("910"), "Après remise")
    assert_test(result["total"] > Decimal("0"), "Total calculé")
    
    return True


def test_empty_cart():
    """Test panier vide."""
    print_test("Panier vide")
    
    tax_rates = {"electronics": Decimal("0.20")}
    tax_calculator = TaxCalculator(tax_rates)
    checkout_service = CheckoutService(tax_calculator)
    
    cart = Cart()
    result = checkout_service.calculate_total(cart)
    
    assert_test(result["subtotal"] == Decimal("0"), "Sous-total = 0")
    assert_test(result["discount_amount"] == Decimal("0"), "Remise = 0")
    assert_test(result["tax_amount"] == Decimal("0"), "Taxes = 0")
    assert_test(result["total"] == Decimal("0"), "Total = 0")
    
    return True


def main():
    """Lance tous les tests."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("=" * 70)
    print("  SUITE DE TESTS - SYSTÈME DE CHECKOUT")
    print("=" * 70)
    print(f"{Colors.END}")
    
    tests = [
        ("Création de produits", test_product_creation),
        ("Validation des produits", test_product_validation),
        ("Opérations sur le panier", test_cart_operations),
        ("Calcul des remises", test_discount_calculation),
        ("Calculateur de taxes", test_tax_calculator),
        ("Service de checkout", test_checkout_service),
        ("Remise par catégorie", test_checkout_with_category_discount),
        ("Panier vide", test_empty_cart),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"{Colors.RED}[ERREUR] Erreur dans {name}: {e}{Colors.END}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Résultats: {passed}/{total} tests réussis{Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}[SUCCES] Tous les tests sont passes !{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}[ECHEC] Certains tests ont echoue{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

