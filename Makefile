.PHONY: help install install-dev test lint format type-check run clean

help:
	@echo "Commandes disponibles:"
	@echo "  make install       - Installe les dépendances de production"
	@echo "  make install-dev   - Installe les dépendances de développement"
	@echo "  make test          - Lance les tests"
	@echo "  make lint          - Vérifie le code avec flake8"
	@echo "  make format        - Formate le code avec black"
	@echo "  make type-check    - Vérifie les types avec mypy"
	@echo "  make run           - Lance l'application"
	@echo "  make clean         - Nettoie les fichiers générés"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest

lint:
	flake8 src tests

format:
	black src tests

type-check:
	mypy src

run:
	python -m src.main

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info

