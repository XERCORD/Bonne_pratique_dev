# Exemple de Workflow Git Complet

Ce document montre un exemple concret de workflow Git pour ce projet, avec des commandes réelles.

## 📋 Scénario : Ajout d'une nouvelle fonctionnalité

### Contexte
Nous voulons ajouter la possibilité de calculer les taxes après application de la remise (au lieu de calculer les taxes avant).

## 🔄 Workflow étape par étape

### 1. S'assurer d'être à jour

```bash
# Se placer sur la branche principale
git checkout main
git pull origin main

# Créer/aller sur la branche develop
git checkout develop
git pull origin develop
```

### 2. Créer une branche feature

```bash
# Créer et basculer sur une nouvelle branche
git checkout -b feature/taxes-after-discount

# Vérifier qu'on est sur la bonne branche
git branch
# * feature/taxes-after-discount
#   develop
#   main
```

### 3. Développer la fonctionnalité

#### Étape 3.1 : Modifier le code

Modifier `src/services/checkout_service.py` pour calculer les taxes après la remise.

#### Étape 3.2 : Commiter les changements

```bash
# Voir les fichiers modifiés
git status

# Ajouter les fichiers modifiés
git add src/services/checkout_service.py

# Commiter avec un message structuré
git commit -m "feat: calcul des taxes après application de la remise

Les taxes sont maintenant calculées sur le montant après remise,
au lieu d'être calculées avant. Cela respecte mieux la logique
métier standard des systèmes de checkout."
```

#### Étape 3.3 : Ajouter des tests

```bash
# Modifier les tests
git add tests/test_services.py

# Commiter les tests
git commit -m "test: ajout de tests pour calcul taxes après remise"
```

#### Étape 3.4 : Mettre à jour la documentation

```bash
# Mettre à jour le README si nécessaire
git add README.md

# Commiter
git commit -m "docs: mise à jour README avec nouvelle logique de calcul"
```

### 4. Vérifier le code avant de pousser

```bash
# Formater le code
make format

# Vérifier le linting
make lint

# Vérifier les types
make type-check

# Lancer les tests
make test
```

### 5. Pousser la branche

```bash
# Pousser la branche sur le remote
git push origin feature/taxes-after-discount

# Si c'est la première fois, configurer le tracking
git push -u origin feature/taxes-after-discount
```

### 6. Créer une Pull Request

Sur GitHub/GitLab, créer une PR avec :

**Titre** :
```
feat: calcul des taxes après application de la remise
```

**Description** :
```markdown
## Contexte
Actuellement, les taxes sont calculées avant l'application de la remise.
Cette PR modifie la logique pour calculer les taxes après la remise,
ce qui est plus conforme aux pratiques standard.

## Changements
- Modification de `CheckoutService.calculate_total()` pour calculer les taxes après remise
- Mise à jour des tests pour refléter le nouveau comportement
- Documentation mise à jour

## Tests
- [x] Tests unitaires ajoutés
- [x] Tests d'intégration mis à jour
- [x] Tous les tests passent

## Checklist
- [x] Code formaté (black)
- [x] Pas d'erreurs de linting (flake8)
- [x] Pas d'erreurs de type (mypy)
- [x] Documentation mise à jour
```

### 7. Répondre aux commentaires de review

```bash
# Faire les modifications demandées
# ... modifier le code ...

# Commiter les corrections
git add src/services/checkout_service.py
git commit -m "fix: correction du calcul proportionnel des taxes

Suite aux commentaires de review, j'ai ajusté la logique pour
calculer les taxes de manière proportionnelle au montant après remise."

# Pousser les changements (la PR se met à jour automatiquement)
git push origin feature/taxes-after-discount
```

### 8. Après le merge

```bash
# Retourner sur develop
git checkout develop

# Récupérer les dernières modifications
git pull origin develop

# Supprimer la branche locale (optionnel)
git branch -d feature/taxes-after-discount

# Supprimer la branche distante (si elle existe encore)
git push origin --delete feature/taxes-after-discount
```

## 📊 Historique des commits (exemple)

```bash
# Voir l'historique des commits
git log --oneline --graph

# Résultat attendu :
# * a1b2c3d (HEAD -> feature/taxes-after-discount) docs: mise à jour README
# * d4e5f6g test: ajout de tests pour calcul taxes après remise
# * g7h8i9j feat: calcul des taxes après application de la remise
# * j0k1l2m (develop) fix: correction bug calcul remise
# * m3n4o5p (main) feat: système de remises initial
```

## 🔍 Commandes utiles

### Voir les différences

```bash
# Différence avec develop
git diff develop

# Différence pour un fichier spécifique
git diff develop src/services/checkout_service.py

# Différence staged (après git add)
git diff --staged
```

### Gérer les commits

```bash
# Modifier le dernier commit (si pas encore poussé)
git commit --amend -m "nouveau message"

# Ajouter des fichiers au dernier commit
git add fichier_oublié.py
git commit --amend --no-edit

# Voir l'historique
git log --oneline -10  # 10 derniers commits
```

### Gérer les branches

```bash
# Lister toutes les branches
git branch -a

# Supprimer une branche locale
git branch -d nom_branche

# Supprimer une branche distante
git push origin --delete nom_branche
```

## ✅ Bonnes pratiques

1. **Commits fréquents** : Ne pas attendre d'avoir tout fini
2. **Messages clairs** : Décrire ce qui a changé et pourquoi
3. **Branches courtes** : Une branche = une fonctionnalité/bug fix
4. **Tests avant push** : Toujours vérifier que les tests passent
5. **PRs concises** : Une PR = une fonctionnalité, pas plusieurs

## 🚫 À éviter

- ❌ Commits avec "fix bug", "update", "changes"
- ❌ Branches qui restent ouvertes trop longtemps
- ❌ PRs avec beaucoup de changements non liés
- ❌ Pousser du code qui ne compile pas / tests qui échouent
- ❌ Commits qui mélangent plusieurs changements non liés

