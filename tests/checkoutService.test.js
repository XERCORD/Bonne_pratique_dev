const { calculateCheckout } = require('../src/services/checkoutService');

test('discount before tax', () => {
  const r = calculateCheckout({
    items: [{ name: 'A', price: 100, quantity: 1 }],
    taxRate: 0.2,
    discount: 10
  });
  expect(r.total).toBe(108);
});

test('discount = 0', () => {
  const r = calculateCheckout({
    items: [{ name: 'A', price: 100, quantity: 1 }],
    taxRate: 0.2,
    discount: 0
  });
  expect(r.total).toBe(120);
  expect(r.totalBeforeTax).toBe(100);
  expect(r.taxAmount).toBe(20);
});

test('discount > subtotal', () => {
  const r = calculateCheckout({
    items: [{ name: 'A', price: 100, quantity: 1 }],
    taxRate: 0.2,
    discount: 150
  });
  // Discount should be capped at subtotal (100)
  expect(r.totalBeforeTax).toBe(0);
  expect(r.taxAmount).toBe(0);
  expect(r.total).toBe(0);
});

test('taxRate = 0', () => {
  const r = calculateCheckout({
    items: [{ name: 'A', price: 100, quantity: 1 }],
    taxRate: 0,
    discount: 10
  });
  expect(r.totalBeforeTax).toBe(90);
  expect(r.taxAmount).toBe(0);
  expect(r.total).toBe(90);
});

test('multiple items', () => {
  const r = calculateCheckout({
    items: [
      { name: 'A', price: 10, quantity: 2 },
      { name: 'B', price: 20, quantity: 3 },
      { name: 'C', price: 5, quantity: 1 }
    ],
    taxRate: 0.1,
    discount: 5
  });
  // Subtotal: (10*2) + (20*3) + (5*1) = 20 + 60 + 5 = 85
  // After discount: 85 - 5 = 80
  // Tax: 80 * 0.1 = 8
  // Total: 80 + 8 = 88
  expect(r.totalBeforeTax).toBe(80);
  expect(r.taxAmount).toBe(8);
  expect(r.total).toBe(88);
});
