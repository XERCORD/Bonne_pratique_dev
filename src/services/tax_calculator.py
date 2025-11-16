"""Service de calcul des taxes."""

from decimal import Decimal
from typing import Dict

from ..models.cart import Cart


class TaxCalculator:
    """Calcule les taxes applicables au panier."""

    def __init__(self, tax_rates: Dict[str, Decimal]) -> None:
        """
        Initialise le calculateur de taxes.

        Args:
            tax_rates: Dictionnaire des taux de taxe par catégorie (ex: {"food": 0.10, "electronics": 0.20})
        """
        if not tax_rates:
            raise ValueError("Les taux de taxe ne peuvent pas être vides")
        if any(rate < 0 for rate in tax_rates.values()):
            raise ValueError("Les taux de taxe ne peuvent pas être négatifs")

        self.tax_rates = tax_rates

    def calculate_tax(self, cart: Cart) -> Decimal:
        """
        Calcule le montant total des taxes pour le panier.

        Args:
            cart: Le panier d'achat

        Returns:
            Le montant total des taxes
        """
        total_tax = Decimal("0")

        for item in cart.items:
            category = item.product.category
            tax_rate = self.tax_rates.get(category, Decimal("0"))
            item_tax = item.subtotal * tax_rate
            total_tax += item_tax

        return total_tax

