const express = require('express');
const controller = require('../controllers/checkoutController');
const router = express.Router();

router.post('/checkout', controller.checkout);

module.exports = router;
