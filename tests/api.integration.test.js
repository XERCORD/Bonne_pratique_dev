
const request = require('supertest');
const app = require('../src/app');
test('valid API call', async () => {
  const res = await request(app).post('/api/checkout').send({ items: [{ name: 'A', price: 10, quantity: 1 }], taxRate: 0.2, discount: 0 });
  expect(res.statusCode).toBe(200);
  expect(res.body.total).toBe(12);
});
