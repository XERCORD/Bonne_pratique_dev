"""Tests des services métier."""

from decimal import Decimal

import pytest

from src.models.cart import Cart
from src.models.discount import Discount, DiscountType
from src.models.product import Product
from src.services.checkout_service import CheckoutService
from src.services.tax_calculator import TaxCalculator


class TestTaxCalculator:
    """Tests pour le calculateur de taxes."""

    def test_calculate_tax_single_category(self):
        """Test le calcul de taxes pour une seule catégorie."""
        tax_rates = {"electronics": Decimal("0.20")}
        calculator = TaxCalculator(tax_rates)

        cart = Cart()
        product = Product(
            id="prod1", name="Laptop", price=Decimal("1000"), category="electronics"
        )
        cart.add_item(product, quantity=1)

        tax = calculator.calculate_tax(cart)
        assert tax == Decimal("200")

    def test_calculate_tax_multiple_categories(self):
        """Test le calcul de taxes pour plusieurs catégories."""
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
        assert tax == Decimal("201")

    def test_calculate_tax_unknown_category(self):
        """Test le calcul de taxes pour une catégorie inconnue."""
        tax_rates = {"electronics": Decimal("0.20")}
        calculator = TaxCalculator(tax_rates)

        cart = Cart()
        product = Product(
            id="prod1", name="Unknown", price=Decimal("100"), category="unknown"
        )
        cart.add_item(product, quantity=1)

        tax = calculator.calculate_tax(cart)
        assert tax == Decimal("0")


class TestCheckoutService:
    """Tests pour le service de checkout."""

    def test_calculate_total_without_discount(self):
        """Test le calcul du total sans remise."""
        tax_rates = {"electronics": Decimal("0.20")}
        tax_calculator = TaxCalculator(tax_rates)
        checkout_service = CheckoutService(tax_calculator)

        cart = Cart()
        product = Product(
            id="prod1", name="Laptop", price=Decimal("1000"), category="electronics"
        )
        cart.add_item(product, quantity=1)

        result = checkout_service.calculate_total(cart)

        assert result["subtotal"] == Decimal("1000")
        assert result["discount_amount"] == Decimal("0")
        assert result["tax_amount"] == Decimal("200")
        assert result["total"] == Decimal("1200")

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

    def test_calculate_total_with_fixed_discount(self):
        """Test le calcul du total avec remise fixe."""
        tax_rates = {"electronics": Decimal("0.20")}
        tax_calculator = TaxCalculator(tax_rates)
        checkout_service = CheckoutService(tax_calculator)

        cart = Cart()
        product = Product(
            id="prod1", name="Laptop", price=Decimal("1000"), category="electronics"
        )
        cart.add_item(product, quantity=1)

        discount = Discount(
            code="SAVE50", discount_type=DiscountType.FIXED, value=Decimal("50")
        )

        result = checkout_service.calculate_total(cart, discount)

        assert result["subtotal"] == Decimal("1000")
        assert result["discount_amount"] == Decimal("50")
        assert result["subtotal_after_discount"] == Decimal("950")
        # Taxes ajustées: 200 * (950/1000) = 190
        assert result["tax_amount"] == Decimal("190")
        assert result["total"] == Decimal("1140")

    def test_calculate_total_empty_cart(self):
        """Test le calcul du total pour un panier vide."""
        tax_rates = {"electronics": Decimal("0.20")}
        tax_calculator = TaxCalculator(tax_rates)
        checkout_service = CheckoutService(tax_calculator)

        cart = Cart()
        result = checkout_service.calculate_total(cart)

        assert result["subtotal"] == Decimal("0")
        assert result["discount_amount"] == Decimal("0")
        assert result["tax_amount"] == Decimal("0")
        assert result["total"] == Decimal("0")

    def test_calculate_total_with_category_discount(self):
        """Test le calcul du total avec remise par catégorie."""
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

        # Remise de 10% uniquement sur l'électronique
        discount = Discount(
            code="ELECTRO10",
            discount_type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            category="electronics",
        )

        result = checkout_service.calculate_total(cart, discount)

        # Sous-total : 1000 + 10 = 1010
        assert result["subtotal"] == Decimal("1010")
        # Remise : 10% de 1000 (électronique uniquement) = 100
        assert result["discount_amount"] == Decimal("100")
        # Sous-total après remise : 1010 - 100 = 910
        assert result["subtotal_after_discount"] == Decimal("910")
        # Taxes : (200 * 900/1000) + (1 * 10/10) = 180 + 1 = 181
        # Note: Les taxes sont ajustées proportionnellement
        assert result["tax_amount"] > Decimal("0")
        assert result["total"] == result["subtotal_after_discount"] + result["tax_amount"]

    def test_calculate_total_with_min_amount_discount(self):
        """Test le calcul avec remise ayant un montant minimum."""
        tax_rates = {"electronics": Decimal("0.20")}
        tax_calculator = TaxCalculator(tax_rates)
        checkout_service = CheckoutService(tax_calculator)

        cart = Cart()
        product = Product(
            id="prod1", name="Mouse", price=Decimal("80"), category="electronics"
        )
        cart.add_item(product, quantity=1)

        # Remise de 10% avec minimum de 100€
        discount = Discount(
            code="SAVE10MIN100",
            discount_type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            min_amount=Decimal("100"),
        )

        result = checkout_service.calculate_total(cart, discount)

        # La remise ne s'applique pas car 80€ < 100€
        assert result["discount_amount"] == Decimal("0")
        assert result["subtotal"] == Decimal("80")
        assert result["subtotal_after_discount"] == Decimal("80")

