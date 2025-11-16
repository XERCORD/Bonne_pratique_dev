"""Modèle de produit."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    """Représente un produit dans le catalogue."""

    id: str
    name: str
    price: Decimal
    category: str

    def __post_init__(self) -> None:
        """Valide les données du produit."""
        if not self.id:
            raise ValueError("L'ID du produit ne peut pas être vide")
        if not self.name:
            raise ValueError("Le nom du produit ne peut pas être vide")
        if self.price < 0:
            raise ValueError("Le prix ne peut pas être négatif")

