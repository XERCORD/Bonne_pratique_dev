# 🚀 Guide Git - Pousser le projet sur GitHub

Ce guide vous explique étape par étape comment pousser votre projet sur GitHub.

## 📋 Prérequis

- ✅ Avoir un compte GitHub
- ✅ Avoir créé le repository : [https://github.com/XERCORD/Bonne_pratique_dev](https://github.com/XERCORD/Bonne_pratique_dev)
- ✅ Avoir Git installé sur votre machine

---

## 🔧 Étape 1 : Initialiser Git

```bash
git init
```

---

## 📝 Étape 2 : Ajouter tous les fichiers

```bash
git add .
```

> 💡 Cette commande ajoute tous les fichiers du projet (sauf ceux dans `.gitignore`)

---

## 💾 Étape 3 : Faire le premier commit

```bash
git commit -m "feat: système de checkout simplifié initial

- Gestion de produits avec catégories
- Système de panier d'achat
- Calcul de taxes par catégorie
- Système de remises avancé (globale, par catégorie, avec minimum)
- API REST complète
- Tests unitaires et d'intégration (8/8 tests réussis)
- Documentation complète (architecture, calculs, bug report)
- Configuration formatter/linter (black, flake8, mypy)"
```

---

## 🔗 Étape 4 : Connecter au repository GitHub

```bash
git remote add origin https://github.com/XERCORD/Bonne_pratique_dev.git
```

---

## 🌿 Étape 5 : Renommer la branche en main (si nécessaire)

```bash
git branch -M main
```

---

## ⬆️ Étape 6 : Pousser sur GitHub

```bash
git push -u origin main
```

> ⚠️ **Note** : Si c'est la première fois, GitHub vous demandera vos identifiants.

---

## ✅ Vérification

Après le push, vérifiez sur GitHub que tous les fichiers sont bien présents.

---

## 🔄 Commandes rapides pour les prochaines fois

Une fois le repo configuré, pour les prochaines modifications :

```bash
# 1. Voir les fichiers modifiés
git status

# 2. Ajouter les fichiers modifiés
git add .

# 3. Faire un commit
git commit -m "feat: description de la modification"

# 4. Pousser sur GitHub
git push
```

---

## 🆘 En cas de problème

### Erreur : "remote origin already exists"

```bash
# Supprimer l'ancien remote
git remote remove origin

# Ajouter le nouveau
git remote add origin https://github.com/XERCORD/Bonne_pratique_dev.git
```

### Erreur : "authentication failed"

1. Vérifiez vos identifiants GitHub
2. Ou utilisez un token d'accès personnel :
   - GitHub → Settings → Developer settings → Personal access tokens
   - Créez un token avec les permissions `repo`
   - Utilisez le token comme mot de passe

### Erreur : "refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
```

### ⚠️ Force Push (Push forcé)

**ATTENTION** : Le force push écrase l'historique sur GitHub. Utilisez-le uniquement si vous êtes sûr de ce que vous faites !

#### Quand utiliser le force push ?

- ✅ Vous travaillez seul sur le projet
- ✅ Vous voulez réécrire l'historique (après un rebase, amend, etc.)
- ✅ Le repository distant a des commits que vous voulez remplacer

#### ⚠️ Quand NE PAS utiliser le force push ?

- ❌ Si d'autres personnes travaillent sur le projet
- ❌ Sur une branche partagée (main, develop)
- ❌ Si vous n'êtes pas sûr de ce que vous faites

#### Commandes pour forcer le push

**Option 1 : Force push simple**
```bash
git push -f origin main
```

**Option 2 : Force push avec lease (plus sûr)**
```bash
git push --force-with-lease origin main
```

> 💡 `--force-with-lease` est plus sûr car il vérifie que personne d'autre n'a poussé entre temps. Si quelqu'un a poussé, la commande échouera.

**Option 3 : Force push d'une branche spécifique**
```bash
git push -f origin nom-de-la-branche
```

#### Exemple de scénario

```bash
# Vous avez fait des modifications locales et un amend
git commit --amend -m "feat: nouveau message de commit"

# Le push normal échoue car l'historique a changé
git push origin main
# Erreur: ! [rejected] main -> main (non-fast-forward)

# Solution : Force push (si vous êtes sûr)
git push -f origin main
# ou plus sûr
git push --force-with-lease origin main
```

#### ⚠️ Récupérer après un force push accidentel

Si quelqu'un a fait un force push et que vous avez perdu des commits :

```bash
# Récupérer l'historique perdu (si disponible)
git reflog

# Revenir à un commit spécifique
git reset --hard HEAD@{n}  # où n est le numéro dans reflog
```

---

## 📚 Bonnes pratiques

### Messages de commit

Utilisez la convention [Conventional Commits](https://www.conventionalcommits.org/) :

- `feat:` : Nouvelle fonctionnalité
- `fix:` : Correction de bug
- `docs:` : Documentation
- `test:` : Tests
- `refactor:` : Refactoring
- `style:` : Formatage

### Exemples

```bash
git commit -m "feat: ajout des remises par catégorie"
git commit -m "fix: correction du calcul des taxes"
git commit -m "docs: mise à jour du README"
git commit -m "test: ajout de tests pour remises par catégorie"
```

---

## 🎯 Checklist avant de pousser

- [ ] Tous les fichiers sont ajoutés (`git add .`)
- [ ] Le message de commit est clair et descriptif
- [ ] Les tests passent (`python test_all.py`)
- [ ] Le code est formaté (`make format` si disponible)
- [ ] Aucune information sensible dans le code (mots de passe, clés API, etc.)

---

## 📖 Pour plus d'informations

- [Guide de contribution](CONTRIBUTING.md)
- [Workflow Git](docs/GIT_WORKFLOW_EXAMPLE.md)

