"""Application Flask principale."""

import logging
from decimal import Decimal
from typing import Dict, Optional

from flask import Flask, jsonify, request
from flask_cors import CORS

from ..models.cart import Cart
from ..models.discount import Discount, DiscountType
from ..models.product import Product
from ..services.checkout_service import CheckoutService
from ..services.tax_calculator import TaxCalculator

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Crée et configure l'application Flask."""
    app = Flask(__name__)
    
    # Configuration CORS pour permettre les requêtes depuis le navigateur
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Configuration des taux de taxe par défaut
    default_tax_rates = {
        "food": Decimal("0.10"),
        "electronics": Decimal("0.20"),
        "clothing": Decimal("0.15"),
        "other": Decimal("0.18"),
    }

    tax_calculator = TaxCalculator(default_tax_rates)
    checkout_service = CheckoutService(tax_calculator)

    # Stockage en mémoire (pour la démo, utiliser une DB en production)
    products_db: Dict[str, Product] = {}
    discounts_db: Dict[str, Discount] = {}

    @app.route("/health", methods=["GET"])
    def health_check() -> tuple:
        """Endpoint de santé de l'API."""
        return jsonify({"status": "ok"}), 200

    @app.route("/products", methods=["POST"])
    def create_product() -> tuple:
        """Crée un nouveau produit."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Données JSON requises"}), 400

            product = Product(
                id=data["id"],
                name=data["name"],
                price=Decimal(str(data["price"])),
                category=data.get("category", "other"),
            )

            if product.id in products_db:
                return jsonify({"error": "Produit déjà existant"}), 409

            products_db[product.id] = product

            logger.info("Produit créé", extra={"product_id": product.id, "name": product.name})
            return jsonify({"id": product.id, "name": product.name}), 201

        except KeyError as e:
            logger.warning("Champ manquant dans la requête", extra={"field": str(e)})
            return jsonify({"error": f"Champ requis manquant: {e}"}), 400
        except ValueError as e:
            logger.warning("Données invalides", extra={"error": str(e)})
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error("Erreur lors de la création du produit", exc_info=True)
            return jsonify({"error": "Erreur interne du serveur"}), 500

    @app.route("/products/<product_id>", methods=["GET"])
    def get_product(product_id: str) -> tuple:
        """Récupère un produit par son ID."""
        try:
            product = products_db.get(product_id)
            if not product:
                logger.warning("Produit non trouvé", extra={"product_id": product_id})
                return jsonify({"error": "Produit non trouvé"}), 404

            return (
                jsonify(
                    {
                        "id": product.id,
                        "name": product.name,
                        "price": str(product.price),
                        "category": product.category,
                    }
                ),
                200,
            )
        except Exception as e:
            logger.error("Erreur lors de la récupération du produit", exc_info=True)
            return jsonify({"error": "Erreur interne du serveur"}), 500

    @app.route("/discounts", methods=["POST"])
    def create_discount() -> tuple:
        """Crée une nouvelle remise."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Données JSON requises"}), 400

            discount_type = DiscountType(data["type"])
            discount = Discount(
                code=data["code"],
                discount_type=discount_type,
                value=Decimal(str(data["value"])),
                min_amount=Decimal(str(data["min_amount"])) if data.get("min_amount") else None,
                category=data.get("category"),
            )

            if discount.code in discounts_db:
                return jsonify({"error": "Code de remise déjà existant"}), 409

            discounts_db[discount.code] = discount

            logger.info("Remise créée", extra={"code": discount.code})
            return jsonify({"code": discount.code}), 201

        except KeyError as e:
            logger.warning("Champ manquant dans la requête", extra={"field": str(e)})
            return jsonify({"error": f"Champ requis manquant: {e}"}), 400
        except ValueError as e:
            logger.warning("Données invalides", extra={"error": str(e)})
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error("Erreur lors de la création de la remise", exc_info=True)
            return jsonify({"error": "Erreur interne du serveur"}), 500

    @app.route("/checkout", methods=["POST"])
    def checkout() -> tuple:
        """Calcule le total du panier avec taxes et remises."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Données JSON requises"}), 400

            items = data.get("items", [])
            if not items:
                return jsonify({"error": "Le panier ne peut pas être vide"}), 400

            cart = Cart()
            for item_data in items:
                product_id = item_data["product_id"]
                quantity = item_data["quantity"]

                product = products_db.get(product_id)
                if not product:
                    logger.warning("Produit non trouvé dans le panier", extra={"product_id": product_id})
                    return jsonify({"error": f"Produit {product_id} non trouvé"}), 404

                cart.add_item(product, quantity)

            discount_code = data.get("discount_code")
            discount: Optional[Discount] = None
            if discount_code:
                discount = discounts_db.get(discount_code)
                if not discount:
                    logger.warning("Code de remise invalide", extra={"code": discount_code})
                    return jsonify({"error": f"Code de remise {discount_code} invalide"}), 404

            result = checkout_service.calculate_total(cart, discount)

            logger.info("Checkout calculé", extra={"total": str(result["total"])})
            return (
                jsonify(
                    {
                        "subtotal": str(result["subtotal"]),
                        "discount_amount": str(result["discount_amount"]),
                        "subtotal_after_discount": str(result["subtotal_after_discount"]),
                        "tax_amount": str(result["tax_amount"]),
                        "total": str(result["total"]),
                    }
                ),
                200,
            )

        except KeyError as e:
            logger.warning("Champ manquant dans la requête", extra={"field": str(e)})
            return jsonify({"error": f"Champ requis manquant: {e}"}), 400
        except ValueError as e:
            logger.warning("Données invalides", extra={"error": str(e)})
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error("Erreur lors du checkout", exc_info=True)
            return jsonify({"error": "Erreur interne du serveur"}), 500

    return app

