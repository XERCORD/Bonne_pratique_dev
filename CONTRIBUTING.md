# Guide de Contribution

🔗 **Repository GitHub** : [https://github.com/XERCORD/Bonne_pratique_dev](https://github.com/XERCORD/Bonne_pratique_dev)

## 🌿 Workflow Git

### Structure des branches

- **`main`** : Branche principale, code en production
- **`develop`** : Branche de développement, intégration des features
- **`feature/*`** : Nouvelles fonctionnalités
- **`fix/*`** : Corrections de bugs
- **`docs/*`** : Documentation uniquement
- **`refactor/*`** : Refactoring de code

### Exemple de workflow

#### 1. Créer une branche feature

```bash
# S'assurer d'être à jour
git checkout develop
git pull origin develop

# Créer une nouvelle branche
git checkout -b feature/ajout-remise-categorie
```

#### 2. Développer et commiter

```bash
# Faire des commits structurés et fréquents
git add src/models/discount.py
git commit -m "feat: ajout du champ category dans Discount"

git add src/services/checkout_service.py
git commit -m "feat: implémentation du filtrage par catégorie"

git add tests/
git commit -m "test: ajout des tests pour remises par catégorie"
```

#### 3. Pousser et créer une PR

```bash
# Pousser la branche
git push origin feature/ajout-remise-categorie

# Créer une Pull Request sur GitHub/GitLab
# Titre: feat: ajout du support des remises par catégorie
# Description: Décrire les changements, pourquoi, comment
```

#### 4. Après review et merge

```bash
# Retourner sur develop
git checkout develop
git pull origin develop

# Supprimer la branche locale
git branch -d feature/ajout-remise-categorie
```

## 📝 Convention de commits

Utilisez le format [Conventional Commits](https://www.conventionalcommits.org/) :

### Format

```
<type>(<scope>): <description>

[corps optionnel]

[footer optionnel]
```

### Types

- **`feat`** : Nouvelle fonctionnalité
- **`fix`** : Correction de bug
- **`docs`** : Documentation
- **`style`** : Formatage (pas de changement de code)
- **`refactor`** : Refactoring
- **`test`** : Ajout/modification de tests
- **`chore`** : Tâches de maintenance

### Exemples

```bash
# Feature
git commit -m "feat: ajout du calcul de remises par catégorie"

# Fix
git commit -m "fix: correction du calcul des taxes avec remise"

# Documentation
git commit -m "docs: mise à jour du README avec exemples d'utilisation"

# Test
git commit -m "test: ajout de tests pour remises avec montant minimum"

# Refactoring
git commit -m "refactor: extraction de la logique de calcul dans une méthode dédiée"
```

### Bonnes pratiques

- ✅ **Messages clairs** : Décrire ce qui a changé et pourquoi
- ✅ **Commits atomiques** : Un commit = une modification logique
- ✅ **Commits fréquents** : Ne pas attendre d'avoir tout fini
- ❌ **Éviter** : "fix bug", "update", "changes"

## 🔍 Code Review

### Avant de soumettre une PR

1. **Vérifier le code** :
   ```bash
   make lint
   make format
   make type-check
   make test
   ```

2. **S'assurer que tous les tests passent**

3. **Vérifier la couverture de code**

4. **Mettre à jour la documentation si nécessaire**

### Pendant la review

- Répondre aux commentaires de manière constructive
- Faire les modifications demandées
- Pousser les changements sur la même branche

## 🧪 Tests

### Écrire des tests

- **Tests unitaires** : Tester chaque fonction/méthode isolément
- **Tests d'intégration** : Tester les interactions entre composants
- **Nommage** : `test_<ce_qui_est_testé>_<condition>_<résultat_attendu>`

### Exemple

```python
def test_calculate_total_with_percentage_discount_returns_correct_total():
    """Test que le calcul avec remise en pourcentage retourne le bon total."""
    # Arrange
    cart = Cart()
    product = Product(...)
    cart.add_item(product, quantity=1)
    
    # Act
    result = checkout_service.calculate_total(cart, discount)
    
    # Assert
    assert result["total"] == Decimal("1080")
```

## 📚 Documentation

### Quand mettre à jour la documentation

- Nouvelle fonctionnalité → Mettre à jour le README
- Changement d'API → Mettre à jour les exemples
- Changement d'architecture → Mettre à jour ARCHITECTURE.md
- Bug corrigé → Mettre à jour BUG_REPORT.md si pertinent

## ✅ Checklist avant PR

- [ ] Code formaté avec `black`
- [ ] Pas d'erreurs de linting (`flake8`)
- [ ] Pas d'erreurs de type (`mypy`)
- [ ] Tous les tests passent
- [ ] Nouveaux tests ajoutés si nouvelle fonctionnalité
- [ ] Documentation mise à jour
- [ ] Commits structurés selon la convention
- [ ] Pas de code commenté ou de debug
- [ ] Logs appropriés ajoutés

## 🐛 Signaler un bug

Utilisez le template de bug report dans `docs/BUG_REPORT.md` :

1. **Titre clair** : Description concise du problème
2. **Étapes de reproduction** : Comment reproduire le bug
3. **Comportement attendu vs observé** : Ce qui devrait se passer vs ce qui se passe
4. **Logs/traces** : Logs d'erreur si disponibles
5. **Environnement** : Version Python, OS, etc.

## 💡 Proposer une amélioration

1. Créer une issue avec le label "enhancement"
2. Décrire le problème ou le besoin
3. Proposer une solution
4. Discuter avec les maintainers
5. Implémenter après validation

## 📞 Questions ?

N'hésitez pas à ouvrir une issue pour poser des questions ou demander de l'aide !

## 👤 Auteurs

**Romain** et **Xerly**

Projet réalisé dans le cadre du cours sur les bonnes pratiques de développement.

