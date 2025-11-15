
const checkoutService = require('../services/checkoutService');
const { validateCheckoutPayload } = require('../utils/validators');
const logger = require('../utils/logger');

async function checkout(req, res, next) {
  try {
    const payload = req.body;
    validateCheckoutPayload(payload);
    const result = checkoutService.calculateCheckout(payload);
    logger.info('Checkout computed', { itemCount: payload.items.length, totalBeforeTax: result.totalBeforeTax });
    res.json(result);
  } catch (err) {
    err.status = err.status || 400;
    logger.warn('Checkout failed', { message: err.message });
    next(err);
  }
}
module.exports = { checkout };
