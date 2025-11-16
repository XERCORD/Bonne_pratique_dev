"""Configuration du package."""

from setuptools import find_packages, setup

setup(
    name="checkout",
    version="1.0.0",
    description="Système de checkout simplifié avec calcul de panier, taxes et remises",
    author="Romain et Xerly",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "Flask==3.0.0",
    ],
    python_requires=">=3.9",
)

