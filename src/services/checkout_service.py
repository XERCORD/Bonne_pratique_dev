"""Service de checkout."""

from decimal import Decimal
from typing import Optional

from ..models.cart import Cart
from ..models.discount import Discount
from .tax_calculator import TaxCalculator


class CheckoutService:
    """Service principal pour le processus de checkout."""

    def __init__(self, tax_calculator: TaxCalculator) -> None:
        """
        Initialise le service de checkout.

        Args:
            tax_calculator: Calculateur de taxes
        """
        self.tax_calculator = tax_calculator

    def calculate_total(
        self, cart: Cart, discount: Optional[Discount] = None
    ) -> dict:
        """
        Calcule le total final du panier avec taxes et remises.

        Logique de calcul :
        1. Calcul du sous-total (somme de tous les articles)
        2. Application de la remise (globale ou par catégorie)
        3. Calcul des taxes sur le montant après remise
        4. Calcul du total final

        Args:
            cart: Le panier d'achat
            discount: Remise optionnelle à appliquer

        Returns:
            Dictionnaire contenant:
                - subtotal: Sous-total avant taxes et remises
                - discount_amount: Montant de la remise appliquée
                - subtotal_after_discount: Sous-total après remise
                - tax_amount: Montant des taxes (calculées après remise)
                - total: Total final à payer
        """
        if cart.is_empty():
            return {
                "subtotal": Decimal("0"),
                "discount_amount": Decimal("0"),
                "subtotal_after_discount": Decimal("0"),
                "tax_amount": Decimal("0"),
                "total": Decimal("0"),
            }

        # Étape 1 : Calcul du sous-total
        subtotal = cart.subtotal

        # Étape 2 : Calcul de la remise
        discount_amount = self._calculate_discount_amount(cart, discount, subtotal)

        # Étape 3 : Sous-total après remise
        subtotal_after_discount = subtotal - discount_amount

        # Étape 4 : Calcul des taxes sur le montant après remise
        # Les taxes sont calculées proportionnellement au montant après remise
        tax_amount = self._calculate_tax_after_discount(
            cart, subtotal, subtotal_after_discount
        )

        # Étape 5 : Total final
        total = subtotal_after_discount + tax_amount

        return {
            "subtotal": subtotal,
            "discount_amount": discount_amount,
            "subtotal_after_discount": subtotal_after_discount,
            "tax_amount": tax_amount,
            "total": total,
        }

    def _calculate_discount_amount(
        self, cart: Cart, discount: Optional[Discount], subtotal: Decimal
    ) -> Decimal:
        """
        Calcule le montant de la remise à appliquer.

        Si la remise a une catégorie spécifiée, elle s'applique uniquement
        aux produits de cette catégorie. Sinon, elle s'applique au total.

        Args:
            cart: Le panier d'achat
            discount: Remise optionnelle
            subtotal: Sous-total du panier

        Returns:
            Montant de la remise
        """
        if not discount:
            return Decimal("0")

        # Si la remise est spécifique à une catégorie
        if discount.category:
            # Calculer le sous-total uniquement pour cette catégorie
            category_subtotal = sum(
                item.subtotal
                for item in cart.items
                if item.product.category == discount.category
            )
            return discount.calculate_discount(category_subtotal)
        else:
            # Remise globale sur tout le panier
            return discount.calculate_discount(subtotal)

    def _calculate_tax_after_discount(
        self, cart: Cart, subtotal: Decimal, subtotal_after_discount: Decimal
    ) -> Decimal:
        """
        Calcule les taxes sur le montant après remise.

        Les taxes sont calculées proportionnellement au montant après remise.
        Cela signifie que si une remise de 10% est appliquée, les taxes
        sont également réduites de 10%.

        Args:
            cart: Le panier d'achat
            subtotal: Sous-total avant remise
            subtotal_after_discount: Sous-total après remise

        Returns:
            Montant des taxes après remise
        """
        # Calcul des taxes sur le montant original
        tax_amount = self.tax_calculator.calculate_tax(cart)

        # Application proportionnelle de la remise aux taxes
        if subtotal > 0:
            tax_ratio = subtotal_after_discount / subtotal
            tax_amount = tax_amount * tax_ratio

        return tax_amount

