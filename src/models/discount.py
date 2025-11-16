"""Modèle de remise."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional


class DiscountType(Enum):
    """Type de remise."""

    PERCENTAGE = "percentage"
    FIXED = "fixed"


@dataclass
class Discount:
    """Représente une remise applicable au panier."""

    code: str
    discount_type: DiscountType
    value: Decimal
    min_amount: Optional[Decimal] = None
    category: Optional[str] = None

    def __post_init__(self) -> None:
        """Valide les données de la remise."""
        if not self.code:
            raise ValueError("Le code de remise ne peut pas être vide")
        if self.value < 0:
            raise ValueError("La valeur de remise ne peut pas être négative")
        if self.discount_type == DiscountType.PERCENTAGE and self.value > 100:
            raise ValueError("Une remise en pourcentage ne peut pas dépasser 100%")
        if self.min_amount is not None and self.min_amount < 0:
            raise ValueError("Le montant minimum ne peut pas être négatif")

    def calculate_discount(self, amount: Decimal) -> Decimal:
        """Calcule le montant de la remise pour un montant donné."""
        if self.min_amount is not None and amount < self.min_amount:
            return Decimal("0")

        if self.discount_type == DiscountType.PERCENTAGE:
            return amount * (self.value / Decimal("100"))
        else:  # FIXED
            return min(self.value, amount)

