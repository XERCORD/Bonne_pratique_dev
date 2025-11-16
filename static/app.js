const express = require('express');
const dotenv = require('dotenv');
const path = require('path');
const checkoutRoutes = require('./routes/checkoutRoutes');
const logger = require('./utils/logger');

dotenv.config();
const app = express();

app.use(express.static(path.join(__dirname, '..', 'public')));
app.use(express.json());
app.use('/api', checkoutRoutes);

// Health check endpoint - provides system status
app.get('/health', (req, res) => {
  const healthCheck = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV || 'development',
    service: 'Checkout NeoGlass API',
    version: '1.0.0',
    checks: {
      server: 'operational',
      memory: {
        used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
        total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024),
        unit: 'MB'
      }
    }
  };
  res.json(healthCheck);
});

// API Documentation endpoint
app.get('/docs', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'public', 'docs.html'));
});

app.use((err, req, res, next) => {
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';
  logger.error('Unhandled error', { status, message });
  res.status(status).json({ error: message });
});

const PORT = process.env.PORT || 3000;
if (require.main === module) {
  app.listen(PORT, () => logger.info(`Server started on port ${PORT}`));
}
module.exports = app;