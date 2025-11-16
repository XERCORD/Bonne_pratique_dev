const { validateCheckoutPayload } = require('../src/utils/validators');

test('empty payload → 400', () => {
  expect(() => validateCheckoutPayload(null)).toThrow();
  expect(() => validateCheckoutPayload(undefined)).toThrow();
  expect(() => validateCheckoutPayload({})).toThrow();
});

test('empty items → 400', () => {
  expect(() => validateCheckoutPayload({ items: [] })).toThrow();
  expect(() => validateCheckoutPayload({ items: null })).toThrow();
  expect(() => validateCheckoutPayload({ items: undefined })).toThrow();
});

test('negative price → 400', () => {
  expect(() =>
    validateCheckoutPayload({
      items: [{ name: 'A', price: -10, quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();
});

test('item without name → 400', () => {
  expect(() =>
    validateCheckoutPayload({
      items: [{ price: 10, quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();

  expect(() =>
    validateCheckoutPayload({
      items: [{ name: '', price: 10, quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();
});

test('non-numeric price → 400', () => {
  expect(() =>
    validateCheckoutPayload({
      items: [{ name: 'A', price: '10', quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();

  expect(() =>
    validateCheckoutPayload({
      items: [{ name: 'A', price: NaN, quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();
});

test('invalid quantity → 400', () => {
  expect(() =>
    validateCheckoutPayload({
      items: [{ name: 'A', price: 10, quantity: 0 }],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();

  expect(() =>
    validateCheckoutPayload({
      items: [{ name: 'A', price: 10, quantity: -1 }],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();

  expect(() =>
    validateCheckoutPayload({
      items: [{ name: 'A', price: 10, quantity: 1.5 }],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();
});

test('negative taxRate → 400', () => {
  expect(() =>
    validateCheckoutPayload({
      items: [{ name: 'A', price: 10, quantity: 1 }],
      taxRate: -0.1,
      discount: 0
    })
  ).toThrow();
});

test('negative discount → 400', () => {
  expect(() =>
    validateCheckoutPayload({
      items: [{ name: 'A', price: 10, quantity: 1 }],
      taxRate: 0.2,
      discount: -5
    })
  ).toThrow();
});

test('item not an object → 400', () => {
  expect(() =>
    validateCheckoutPayload({
      items: ['not an object'],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();

  expect(() =>
    validateCheckoutPayload({
      items: [null],
      taxRate: 0.2,
      discount: 0
    })
  ).toThrow();
});

test('valid payload should not throw', () => {
  expect(() =>
    validateCheckoutPayload({
      items: [{ name: 'A', price: 10, quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    })
  ).not.toThrow();
});
