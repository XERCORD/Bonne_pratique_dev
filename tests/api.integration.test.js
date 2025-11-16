const request = require('supertest');
const app = require('../src/app');

test('valid API call', async () => {
  const res = await request(app)
    .post('/api/checkout')
    .send({
      items: [{ name: 'A', price: 10, quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    });

  expect(res.statusCode).toBe(200);
  expect(res.body.total).toBe(12);
});

test('empty payload → 400', async () => {
  const res = await request(app).post('/api/checkout').send({});

  expect(res.statusCode).toBe(400);
});

test('empty items → 400', async () => {
  const res = await request(app).post('/api/checkout').send({
    items: [],
    taxRate: 0.2,
    discount: 0
  });

  expect(res.statusCode).toBe(400);
});

test('negative price → 400', async () => {
  const res = await request(app)
    .post('/api/checkout')
    .send({
      items: [{ name: 'A', price: -10, quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    });

  expect(res.statusCode).toBe(400);
});

test('item without name → 400', async () => {
  const res = await request(app)
    .post('/api/checkout')
    .send({
      items: [{ price: 10, quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    });

  expect(res.statusCode).toBe(400);
});

test('non-numeric price → 400', async () => {
  const res = await request(app)
    .post('/api/checkout')
    .send({
      items: [{ name: 'A', price: 'invalid', quantity: 1 }],
      taxRate: 0.2,
      discount: 0
    });

  expect(res.statusCode).toBe(400);
});

test('invalid quantity → 400', async () => {
  const res = await request(app)
    .post('/api/checkout')
    .send({
      items: [{ name: 'A', price: 10, quantity: 0 }],
      taxRate: 0.2,
      discount: 0
    });

  expect(res.statusCode).toBe(400);
});

test('negative taxRate → 400', async () => {
  const res = await request(app)
    .post('/api/checkout')
    .send({
      items: [{ name: 'A', price: 10, quantity: 1 }],
      taxRate: -0.1,
      discount: 0
    });

  expect(res.statusCode).toBe(400);
});

test('negative discount → 400', async () => {
  const res = await request(app)
    .post('/api/checkout')
    .send({
      items: [{ name: 'A', price: 10, quantity: 1 }],
      taxRate: 0.2,
      discount: -5
    });

  expect(res.statusCode).toBe(400);
});
