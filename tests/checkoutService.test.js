
const { calculateCheckout } = require('../src/services/checkoutService');
test('discount before tax', () => {
  const r = calculateCheckout({ items: [{ name: 'A', price: 100, quantity: 1 }], taxRate: 0.2, discount: 10 });
  expect(r.total).toBe(108);
});
