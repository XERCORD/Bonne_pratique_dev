const { createLogger, format, transports } = require('winston');

// Format structuré avec timestamp, level et message
const structuredFormat = format.combine(
  format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  format.errors({ stack: true }),
  format.splat(),
  format.json()
);

// Format pour la console (plus lisible en développement)
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

// Déterminer le format selon l'environnement
const isDevelopment = process.env.NODE_ENV !== 'production';
const logFormat = isDevelopment ? consoleFormat : structuredFormat;

module.exports = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: logFormat,
  transports: [
    new transports.Console({
      handleExceptions: true,
      handleRejections: true
    })
  ]
  // Ne pas logger de données sensibles (ici OK car panier "fake")
  // En production, ajouter une fonction pour filtrer les données sensibles si nécessaire
});
