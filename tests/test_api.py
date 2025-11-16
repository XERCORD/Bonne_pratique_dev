"""Tests de l'API REST."""

import json
from decimal import Decimal

import pytest

from src.api.app import create_app


@pytest.fixture
def client():
    """Crée un client de test Flask."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests pour l'endpoint de santé."""

    def test_health_check(self, client):
        """Test l'endpoint de santé."""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"


class TestProductEndpoints:
    """Tests pour les endpoints de produits."""

    def test_create_product(self, client):
        """Test la création d'un produit."""
        response = client.post(
            "/products",
            json={
                "id": "prod1",
                "name": "Laptop",
                "price": "999.99",
                "category": "electronics",
            },
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["id"] == "prod1"

    def test_create_product_missing_field(self, client):
        """Test la création d'un produit avec un champ manquant."""
        response = client.post(
            "/products",
            json={"id": "prod1", "name": "Laptop"},
        )
        assert response.status_code == 400

    def test_get_product(self, client):
        """Test la récupération d'un produit."""
        # Créer d'abord un produit
        client.post(
            "/products",
            json={
                "id": "prod1",
                "name": "Laptop",
                "price": "999.99",
                "category": "electronics",
            },
        )

        # Récupérer le produit
        response = client.get("/products/prod1")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == "prod1"
        assert data["name"] == "Laptop"

    def test_get_nonexistent_product(self, client):
        """Test la récupération d'un produit inexistant."""
        response = client.get("/products/nonexistent")
        assert response.status_code == 404


class TestDiscountEndpoints:
    """Tests pour les endpoints de remises."""

    def test_create_discount(self, client):
        """Test la création d'une remise."""
        response = client.post(
            "/discounts",
            json={
                "code": "SAVE10",
                "type": "percentage",
                "value": "10",
            },
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["code"] == "SAVE10"


class TestCheckoutEndpoint:
    """Tests pour l'endpoint de checkout."""

    def test_checkout_without_discount(self, client):
        """Test le checkout sans remise."""
        # Créer un produit
        client.post(
            "/products",
            json={
                "id": "prod1",
                "name": "Laptop",
                "price": "1000",
                "category": "electronics",
            },
        )

        # Faire le checkout
        response = client.post(
            "/checkout",
            json={"items": [{"product_id": "prod1", "quantity": 1}]},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert Decimal(data["subtotal"]) == Decimal("1000")
        assert Decimal(data["total"]) > Decimal("1000")  # Avec taxes

    def test_checkout_with_discount(self, client):
        """Test le checkout avec remise."""
        # Créer un produit
        client.post(
            "/products",
            json={
                "id": "prod1",
                "name": "Laptop",
                "price": "1000",
                "category": "electronics",
            },
        )

        # Créer une remise
        client.post(
            "/discounts",
            json={"code": "SAVE10", "type": "percentage", "value": "10"},
        )

        # Faire le checkout
        response = client.post(
            "/checkout",
            json={
                "items": [{"product_id": "prod1", "quantity": 1}],
                "discount_code": "SAVE10",
            },
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert Decimal(data["discount_amount"]) > Decimal("0")

    def test_checkout_empty_cart(self, client):
        """Test le checkout avec un panier vide."""
        response = client.post("/checkout", json={"items": []})
        assert response.status_code == 400

    def test_checkout_nonexistent_product(self, client):
        """Test le checkout avec un produit inexistant."""
        response = client.post(
            "/checkout",
            json={"items": [{"product_id": "nonexistent", "quantity": 1}]},
        )
        assert response.status_code == 404

