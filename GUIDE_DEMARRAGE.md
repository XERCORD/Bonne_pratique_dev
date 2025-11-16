# 🚀 Guide de Démarrage Rapide

## ⚠️ Problème "Failed to Fetch" ?

Si vous obtenez une erreur "Failed to fetch" lors de l'utilisation du site web, voici les solutions :

## ✅ Solution 1 : Utiliser le script tout-en-un (Recommandé)

Le plus simple est d'utiliser le script qui lance tout automatiquement :

```bash
lancer_tout.bat
```

Ce script lance :
- ✅ L'API Flask sur `http://localhost:5000`
- ✅ Le serveur web sur `http://localhost:8000`
- ✅ Ouvre automatiquement le navigateur

## ✅ Solution 2 : Lancer séparément

### Étape 1 : Lancer l'API

```bash
lancer_api.bat
```

L'API sera accessible sur `http://localhost:5000`

### Étape 2 : Lancer le serveur web (dans une autre fenêtre)

```bash
lancer_web.bat
```

Le site web sera accessible sur `http://localhost:8000/index.html`

## ✅ Solution 3 : Installation manuelle

Si les scripts ne fonctionnent pas :

1. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

2. **Lancer l'API** :
   ```bash
   python -m src.main
   ```

3. **Dans une autre fenêtre, lancer le serveur web** :
   ```bash
   python serve_web.py
   ```

4. **Ouvrir dans le navigateur** :
   - `http://localhost:8000/index.html`

## 🔧 Vérifications

### Vérifier que l'API fonctionne

Ouvrez dans votre navigateur : `http://localhost:5000/health`

Vous devriez voir : `{"status":"ok"}`

### Vérifier que le serveur web fonctionne

Ouvrez dans votre navigateur : `http://localhost:8000/index.html`

Vous devriez voir l'interface web.

## ❌ Problèmes courants

### "Module flask_cors not found"

**Solution** : Installez flask-cors
```bash
pip install flask-cors==4.0.0
```

### "Port 5000 already in use"

**Solution** : Un autre programme utilise le port 5000
- Fermez l'autre programme
- Ou modifiez le port dans `src/main.py`

### "Port 8000 already in use"

**Solution** : Un autre programme utilise le port 8000
- Fermez l'autre programme
- Ou modifiez le port dans `serve_web.py`

### Le navigateur ne se connecte pas

**Vérifications** :
1. L'API est-elle lancée ? (vérifier `http://localhost:5000/health`)
2. Le serveur web est-il lancé ? (vérifier `http://localhost:8000`)
3. Utilisez-vous `http://localhost:8000/index.html` et non `file:///...`

## 💡 Astuce

Pour tester rapidement, utilisez toujours `lancer_tout.bat` qui lance tout automatiquement !

