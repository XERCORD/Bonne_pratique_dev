
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

app.get('/health', (req, res) => res.json({ status: 'ok' }));

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
