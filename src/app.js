
const express = require('express');
const dotenv = require('dotenv');
const path = require('path');
const checkoutRoutes = require('./routes/checkoutRoutes');
const logger = require('./utils/logger');

dotenv.config();
const app = express();

app.use(express.json());

// API Documentation endpoint - MUST be before static middleware
app.get('/docs', (req, res) => {
  try {
    const docsPath = path.resolve(__dirname, '..', 'public', 'docs.html');
    logger.info('Serving docs.html', { path: docsPath });
    res.sendFile(docsPath);
  } catch (err) {
    logger.error('Error serving docs.html', { error: err.message });
    res.status(500).json({ error: 'Error serving documentation' });
  }
});

// Health check endpoint - serves HTML page or JSON based on Accept header or query param
app.get('/health', (req, res) => {
  const wantsJson = req.query.format === 'json' || 
                    (req.headers.accept && req.headers.accept.includes('application/json') && !req.headers.accept.includes('text/html'));
  
  if (wantsJson) {
    const healthCheck = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: Math.floor(process.uptime()),
      uptimeFormatted: formatUptime(process.uptime()),
      environment: process.env.NODE_ENV || 'development',
      service: 'Checkout NeoGlass API',
      version: '1.0.0',
      nodeVersion: process.version,
      platform: process.platform,
      memory: {
        used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
        total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024),
        rss: Math.round(process.memoryUsage().rss / 1024 / 1024),
        external: Math.round(process.memoryUsage().external / 1024 / 1024),
        unit: 'MB'
      },
      checks: {
        server: 'operational',
        api: 'operational'
      }
    };
    res.json(healthCheck);
  } else {
    // Serve HTML page by default for browser requests
    res.sendFile(path.resolve(__dirname, '..', 'public', 'health.html'));
  }
});

function formatUptime(seconds) {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  
  if (days > 0) return `${days}j ${hours}h ${minutes}m`;
  if (hours > 0) return `${hours}h ${minutes}m ${secs}s`;
  if (minutes > 0) return `${minutes}m ${secs}s`;
  return `${secs}s`;
}

app.use('/api', checkoutRoutes);

app.use(express.static(path.join(__dirname, '..', 'public')));

app.use((err, req, res, next) => {
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';
  logger.error('Unhandled error', { status, message });
  res.status(status).json({ error: message });
});

const PORT = process.env.PORT || 3000;
if (require.main === module) {
  app.listen(PORT, () => {
    logger.info(`Server started on port ${PORT}`);
    logger.info(`Documentation available at: http://localhost:${PORT}/docs`);
    logger.info(`Health check available at: http://localhost:${PORT}/health`);
  });
}
module.exports = app;
