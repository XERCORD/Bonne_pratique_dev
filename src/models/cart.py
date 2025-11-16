"""Modèle de panier d'achat."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from .product import Product


@dataclass
class CartItem:
    """Représente un article dans le panier."""

    product: Product
    quantity: int

    def __post_init__(self) -> None:
        """Valide les données de l'article."""
        if self.quantity <= 0:
            raise ValueError("La quantité doit être strictement positive")

    @property
    def subtotal(self) -> Decimal:
        """Calcule le sous-total de l'article."""
        return self.product.price * Decimal(self.quantity)


@dataclass
class Cart:
    """Représente un panier d'achat."""

    items: List[CartItem] = field(default_factory=list)

    def add_item(self, product: Product, quantity: int = 1) -> None:
        """Ajoute un produit au panier."""
        if quantity <= 0:
            raise ValueError("La quantité doit être strictement positive")

        # Vérifie si le produit existe déjà dans le panier
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += quantity
                return

        # Ajoute un nouvel article
        self.items.append(CartItem(product=product, quantity=quantity))

    def remove_item(self, product_id: str) -> None:
        """Retire un produit du panier."""
        self.items = [item for item in self.items if item.product.id != product_id]

    def update_quantity(self, product_id: str, quantity: int) -> None:
        """Met à jour la quantité d'un produit."""
        if quantity <= 0:
            self.remove_item(product_id)
            return

        for item in self.items:
            if item.product.id == product_id:
                item.quantity = quantity
                return

        raise ValueError(f"Produit {product_id} non trouvé dans le panier")

    @property
    def subtotal(self) -> Decimal:
        """Calcule le sous-total du panier (sans taxes ni remises)."""
        return sum(item.subtotal for item in self.items)

    def is_empty(self) -> bool:
        """Vérifie si le panier est vide."""
        return len(self.items) == 0

