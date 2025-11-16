# Pull Request — Improve Logging System and Add Request Middleware

## Contexte / Objectif

Améliorer l'observabilité de l'application en :
- Améliorant le formatage des logs avec Winston (format JSON structuré en production)
- Ajoutant un middleware de logging pour tracer toutes les requêtes HTTP
- Configurant le logger pour utiliser `LOG_LEVEL` depuis les variables d'environnement

**Problème résolu :**
Les logs actuels utilisent un format simple qui n'est pas optimal pour l'analyse en production. De plus, il n'y a pas de traçabilité des requêtes HTTP entrantes.

## Changements faits

### 1. Amélioration du logger (`src/utils/logger.js`)

- ✅ Format JSON structuré en production pour faciliter l'analyse
- ✅ Format console lisible en développement avec couleurs
- ✅ Lecture de `process.env.LOG_LEVEL` avec valeur par défaut `'info'`
- ✅ Gestion des erreurs et exceptions non gérées
- ✅ Timestamp et level inclus dans tous les logs

**Avant :**
```javascript
module.exports = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: format.combine(format.timestamp(), format.simple()),
  transports: [new transports.Console()]
});
```

**Après :**
```javascript
const structuredFormat = format.combine(
  format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  format.errors({ stack: true }),
  format.splat(),
  format.json()
);

const consoleFormat = format.combine(
  format.colorize(),
  format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  format.printf(({ timestamp, level, message, ...meta }) => {
    let msg = `${timestamp} [${level}]: ${message}`;
    if (Object.keys(meta).length > 0) {
      msg += ` ${JSON.stringify(meta)}`;
    }
    return msg;
  })
);

const isDevelopment = process.env.NODE_ENV !== 'production';
const logFormat = isDevelopment ? consoleFormat : structuredFormat;

module.exports = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: logFormat,
  transports: [new transports.Console({
    handleExceptions: true,
    handleRejections: true
  })]
});
```

### 2. Middleware de logging (`src/app.js`)

- ✅ Ajout d'un middleware qui log chaque requête HTTP
- ✅ Contexte inclus : `method`, `path`, `ip`

```javascript
// Request logging middleware
app.use((req, res, next) => {
  logger.info('Incoming request', {
    method: req.method,
    path: req.path,
    ip: req.ip
  });
  next();
});
```

### 3. Documentation

- ✅ Ajout de commentaires expliquant les choix de formatage
- ✅ Note sur la sécurité (pas de données sensibles loggées)

## Comment tester

### 1. Tester le format des logs

**En développement (NODE_ENV non défini ou 'development') :**
```bash
npm start
# Faire une requête POST à /api/checkout
# Observer les logs avec format coloré et lisible
```

**En production (NODE_ENV=production) :**
```bash
NODE_ENV=production npm start
# Faire une requête POST à /api/checkout
# Observer les logs au format JSON structuré
```

### 2. Tester le middleware de logging

```bash
npm start
# Faire plusieurs requêtes :
curl http://localhost:3000/health
curl http://localhost:3000/docs
curl -X POST http://localhost:3000/api/checkout -H "Content-Type: application/json" -d '{"items":[{"name":"Test","price":10,"quantity":1}],"taxRate":0.2,"discount":0}'

# Vérifier que chaque requête est loggée avec method, path et ip
```

### 3. Tester le LOG_LEVEL

```bash
LOG_LEVEL=debug npm start
# Les logs devraient être plus verbeux

LOG_LEVEL=error npm start
# Seuls les erreurs devraient être loggées
```

### 4. Tests automatisés

```bash
npm test
# Les tests existants doivent toujours passer
```

## Screenshots

### Format de log en développement
```
2025-11-16 12:45:30 [info]: Incoming request {"method":"POST","path":"/api/checkout","ip":"::1"}
2025-11-16 12:45:30 [info]: Checkout computed {"itemCount":2,"totalBeforeTax":150}
```

### Format de log en production (JSON)
```json
{"timestamp":"2025-11-16 12:45:30","level":"info","message":"Incoming request","method":"POST","path":"/api/checkout","ip":"::1"}
{"timestamp":"2025-11-16 12:45:30","level":"info","message":"Checkout computed","itemCount":2,"totalBeforeTax":150}
```

## Checklist

- [x] Code formaté avec Prettier
- [x] Linter passé sans erreurs
- [x] Tests existants toujours verts
- [x] Documentation mise à jour
- [x] Pas de régression introduite
- [x] Format de logs testé en dev et prod

## Notes

- Le format JSON en production facilite l'intégration avec des outils comme ELK, Datadog, etc.
- Le middleware de logging ajoute un overhead minimal mais améliore grandement l'observabilité
- Aucune donnée sensible n'est loggée (panier "fake" uniquement)
