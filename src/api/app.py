"""Application Flask principale."""

import logging
import os
from decimal import Decimal
from typing import Dict, Optional

from flask import Flask, jsonify, request, send_from_directory

from ..models.cart import Cart
from ..models.discount import Discount, DiscountType
from ..models.product import Product
from ..services.checkout_service import CheckoutService
from ..services.tax_calculator import TaxCalculator

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Crée et configure l'application Flask."""
    # Définir le dossier static (à la racine du projet)
    static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
    app = Flask(__name__, static_folder=static_folder, static_url_path="")

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

    @app.route("/")
    def index():
        """Page d'accueil - Interface web."""
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/health")
    def health():
        """Page Health Check HTML ou JSON selon l'Accept header."""
        wants_json = (
            request.args.get("format") == "json"
            or (request.headers.get("Accept") and "application/json" in request.headers.get("Accept")
                and "text/html" not in request.headers.get("Accept", ""))
        )
        
        if wants_json:
            return health_check_json()
        return send_from_directory(app.static_folder, "health.html")

    @app.route("/docs")
    def docs_page():
        """Page Documentation HTML."""
        return send_from_directory(app.static_folder, "docs.html")

    def health_check_json() -> tuple:
        """Endpoint de santé de l'API (JSON)."""
        import sys
        import platform
        import os
        from datetime import datetime
        
        # Essayer d'importer psutil, sinon utiliser des valeurs par défaut
        try:
            import psutil
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            memory_used_mb = memory_info.rss / 1024 / 1024
            memory_total_mb = psutil.virtual_memory().total / 1024 / 1024
        except ImportError:
            # psutil n'est pas installé, utiliser des valeurs par défaut
            memory_used_mb = 0
            memory_total_mb = 0
        except Exception:
            memory_used_mb = 0
            memory_total_mb = 0
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": 0,  # Flask ne garde pas l'uptime, on peut l'implémenter si besoin
            "environment": os.getenv("FLASK_ENV", "development"),
            "service": "Checkout Python API",
            "version": "1.0.0",
            "pythonVersion": platform.python_version(),
            "platform": platform.system(),
            "memory": {
                "used": round(memory_used_mb),
                "total": round(memory_total_mb),
                "unit": "MB"
            },
            "checks": {
                "server": "operational",
                "api": "operational"
            }
        }), 200

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
    @app.route("/api/checkout", methods=["POST"])
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
            
            # Adapter pour accepter le format du frontend (name, price, quantity)
            # ou le format API standard (product_id, quantity)
            for item_data in items:
                if "product_id" in item_data:
                    # Format API standard
                    product_id = item_data["product_id"]
                    quantity = item_data["quantity"]
                    product = products_db.get(product_id)
                    if not product:
                        logger.warning("Produit non trouvé dans le panier", extra={"product_id": product_id})
                        return jsonify({"error": f"Produit {product_id} non trouvé"}), 404
                    cart.add_item(product, quantity)
                else:
                    # Format frontend (name, price, quantity)
                    name = item_data.get("name", "")
                    price = Decimal(str(item_data.get("price", 0)))
                    quantity = item_data.get("quantity", 1)
                    category = item_data.get("category", "other")
                    
                    if not name or price <= 0 or quantity <= 0:
                        continue
                    
                    # Créer un produit temporaire
                    temp_product = Product(
                        id=f"temp_{hash(name)}_{hash(str(price))}",
                        name=name,
                        price=price,
                        category=category
                    )
                    cart.add_item(temp_product, quantity)

            # Gérer la remise : peut être un code ou un montant direct
            discount: Optional[Discount] = None
            discount_code = data.get("discount_code")
            discount_amount = data.get("discount")
            tax_rate = data.get("taxRate", 0.20)  # Taux de taxe par défaut
            
            if discount_code:
                discount = discounts_db.get(discount_code)
                if not discount:
                    logger.warning("Code de remise invalide", extra={"code": discount_code})
                    return jsonify({"error": f"Code de remise {discount_code} invalide"}), 404
            elif discount_amount and discount_amount > 0:
                # Créer une remise fixe temporaire
                discount = Discount(
                    code="TEMP_FIXED",
                    discount_type=DiscountType.FIXED,
                    value=Decimal(str(discount_amount)),
                    min_amount=None,
                    category=None
                )

            result = checkout_service.calculate_total(cart, discount)
            
            # Si un taux de taxe personnalisé est fourni, recalculer les taxes
            # (le système par défaut utilise des taxes par catégorie)
            if tax_rate and tax_rate > 0:
                subtotal_after_discount = result["subtotal_after_discount"]
                # Appliquer le taux de taxe personnalisé global
                custom_tax_amount = subtotal_after_discount * Decimal(str(tax_rate))
                custom_total = subtotal_after_discount + custom_tax_amount
                result["tax_amount"] = custom_tax_amount
                result["total"] = custom_total

            logger.info("Checkout calculé", extra={"total": str(result["total"])})
            return (
                jsonify(
                    {
                        "subtotal": str(result["subtotal"]),
                        "discount_amount": str(result["discount_amount"]),
                        "subtotal_after_discount": str(result["subtotal_after_discount"]),
                        "tax_amount": str(result["tax_amount"]),
                        "taxAmount": float(result["tax_amount"]),  # Format pour le frontend
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

