"""Tests des modèles de données."""

import pytest
from decimal import Decimal

from src.models.cart import Cart, CartItem
from src.models.product import Product
from src.models.discount import Discount, DiscountType


class TestProduct:
    """Tests pour le modèle Product."""

    def test_create_valid_product(self):
        """Test la création d'un produit valide."""
        product = Product(
            id="prod1", name="Laptop", price=Decimal("999.99"), category="electronics"
        )
        assert product.id == "prod1"
        assert product.name == "Laptop"
        assert product.price == Decimal("999.99")

    def test_product_empty_id_raises_error(self):
        """Test qu'un produit avec un ID vide lève une erreur."""
        with pytest.raises(ValueError, match="L'ID du produit ne peut pas être vide"):
            Product(id="", name="Test", price=Decimal("10"), category="other")

    def test_product_negative_price_raises_error(self):
        """Test qu'un produit avec un prix négatif lève une erreur."""
        with pytest.raises(ValueError, match="Le prix ne peut pas être négatif"):
            Product(id="prod1", name="Test", price=Decimal("-10"), category="other")


class TestCart:
    """Tests pour le modèle Cart."""

    def test_create_empty_cart(self):
        """Test la création d'un panier vide."""
        cart = Cart()
        assert cart.is_empty()
        assert cart.subtotal == Decimal("0")

    def test_add_item_to_cart(self):
        """Test l'ajout d'un article au panier."""
        cart = Cart()
        product = Product(id="prod1", name="Test", price=Decimal("10"), category="other")
        cart.add_item(product, quantity=2)
        assert not cart.is_empty()
        assert len(cart.items) == 1
        assert cart.items[0].quantity == 2
        assert cart.subtotal == Decimal("20")

    def test_add_same_product_twice(self):
        """Test l'ajout du même produit deux fois."""
        cart = Cart()
        product = Product(id="prod1", name="Test", price=Decimal("10"), category="other")
        cart.add_item(product, quantity=2)
        cart.add_item(product, quantity=3)
        assert len(cart.items) == 1
        assert cart.items[0].quantity == 5

    def test_remove_item_from_cart(self):
        """Test la suppression d'un article du panier."""
        cart = Cart()
        product = Product(id="prod1", name="Test", price=Decimal("10"), category="other")
        cart.add_item(product, quantity=2)
        cart.remove_item("prod1")
        assert cart.is_empty()

    def test_update_quantity(self):
        """Test la mise à jour de la quantité."""
        cart = Cart()
        product = Product(id="prod1", name="Test", price=Decimal("10"), category="other")
        cart.add_item(product, quantity=2)
        cart.update_quantity("prod1", 5)
        assert cart.items[0].quantity == 5

    def test_update_quantity_to_zero_removes_item(self):
        """Test que mettre la quantité à 0 retire l'article."""
        cart = Cart()
        product = Product(id="prod1", name="Test", price=Decimal("10"), category="other")
        cart.add_item(product, quantity=2)
        cart.update_quantity("prod1", 0)
        assert cart.is_empty()


class TestDiscount:
    """Tests pour le modèle Discount."""

    def test_create_percentage_discount(self):
        """Test la création d'une remise en pourcentage."""
        discount = Discount(
            code="SAVE10", discount_type=DiscountType.PERCENTAGE, value=Decimal("10")
        )
        assert discount.calculate_discount(Decimal("100")) == Decimal("10")

    def test_create_fixed_discount(self):
        """Test la création d'une remise fixe."""
        discount = Discount(
            code="SAVE5", discount_type=DiscountType.FIXED, value=Decimal("5")
        )
        assert discount.calculate_discount(Decimal("100")) == Decimal("5")

    def test_discount_with_min_amount(self):
        """Test une remise avec montant minimum."""
        discount = Discount(
            code="SAVE10",
            discount_type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            min_amount=Decimal("50"),
        )
        assert discount.calculate_discount(Decimal("30")) == Decimal("0")
        assert discount.calculate_discount(Decimal("100")) == Decimal("10")

    def test_percentage_discount_over_100_raises_error(self):
        """Test qu'une remise en pourcentage > 100% lève une erreur."""
        with pytest.raises(ValueError, match="ne peut pas dépasser 100%"):
            Discount(
                code="INVALID",
                discount_type=DiscountType.PERCENTAGE,
                value=Decimal("150"),
            )

