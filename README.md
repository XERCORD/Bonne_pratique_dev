# 🟣 Bonne Pratique de Développement

### \*Projet réalisé par **Xerly** & **Romain\***

### _Formation : Ynov -- Module "Bonnes pratiques de développement"_

---

# 🚀 Checkout NeoGlass --- Mini projet démonstratif

Ce dépôt contient un projet complet illustrant les **bonnes pratiques de
développement**, conçu et réalisé par **Xerly** et **Romain** dans le
cadre du module _"Bonne pratique de dév"_.\
L'objectif est de mettre en pratique :

- une architecture propre et maintenable\
- une API structurée (Node.js + Express)\
- une interface moderne, claire et professionnelle\
- des tests unitaires & d'intégration\
- des validations robustes\
- du code lisible suivant les principes KISS, DRY et YAGNI

Le projet implémente une **API Checkout** ainsi qu'un **frontend
NeoGlass violet** complet.

---

# ✨ Fonctionnalités principales

## 🔧 Backend (Node.js + Express)

- Endpoint principal : `POST /api/checkout`
- Validation stricte du payload (prix, quantités, taxe, remise...)
- Calcul propre et fiable :
  - sous-total\
  - remise\
  - taxes\
  - total final\
- Architecture claire :
  - `controllers/`\
  - `services/`\
  - `utils/validators.js`\
  - `routes/`\
- Gestion centralisée des erreurs\
- Logging via Winston

---

## 🟣 Frontend --- Checkout NeoGlass

Une interface premium, moderne et responsive :

- Thème violet NeoGlass\
- Logo SVG créé from scratch\
- Particules animées en fond\
- Glassmorphism\
- Light/Dark mode (persistant via localStorage)\
- Formulaire dynamique (ajout / suppression de produits)\
- Animation du résultat\
- Loader stylé\
- Design responsive et accessible

Le frontend communique directement avec l'API backend.

---

# 🧪 Tests

Inclus dans le projet :

- **Tests unitaires** (Jest)\
- **Tests d'intégration API** (SuperTest)

Lancer les tests :

```bash
npm test
```

---

# 🐳 Docker

Construire l'image :

```bash
docker build -t checkout-neoglass .
```

Lancer l'application :

```bash
docker run -p 3000:3000 checkout-neoglass
```

---

# 📁 Structure du projet

    .
    ├── src/
    │   ├── controllers/
    │   ├── routes/
    │   ├── services/
    │   ├── utils/
    │   └── app.js
    ├── public/
    │   ├── index.html
    │   ├── styles.css
    │   ├── app.js
    │   └── logo.svg
    ├── tests/
    ├── docs/
    ├── Dockerfile
    ├── .env.example
    ├── package.json
    └── README.md

---

# 📦 Installation & lancement

### 1. Installer les dépendances

```bash
npm install
```

### 2. Lancer le serveur

```bash
npm start
```

### 3. Accéder à l'interface

👉 http://localhost:3000

---

# 📚 Objectifs pédagogiques

Ce projet met en pratique les bonnes pratiques suivantes :

✔ Code lisible, clair et organisé\
✔ Architecture modulaire (pattern MVC léger)\
✔ Validation robuste des entrées\
✔ Gestion d'erreurs cohérente\
✔ Séparation propre Front / Back\
✔ UI premium & UX agréable\
✔ Documentation complète\
✔ Utilisation correcte de Git et des branches

---

# 👤 Auteurs

- **Xerly**\
- **Romain**

Projet réalisé dans le cadre du module :\
🎓 _Bonne pratique de dév --- Ynov_
