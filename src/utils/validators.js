function isNumber(value) {
  return typeof value === 'number' && Number.isFinite(value);
}

function validateItem(item) {
  if (!item || typeof item !== 'object') throw make('Each item must be an object');
  if (!item.name) throw make('Item.name must be a non-empty string');
  if (!isNumber(item.price) || item.price < 0) throw make('Item.price must be >= 0');
  if (!Number.isInteger(item.quantity) || item.quantity <= 0)
    throw make('Item.quantity must be a positive integer');
}

function validateCheckoutPayload(payload) {
  if (!payload || typeof payload !== 'object') throw make('Payload must be an object');
  if (!Array.isArray(payload.items) || payload.items.length === 0)
    throw make('items must be non-empty');
  payload.items.forEach(validateItem);
  if (!isNumber(payload.taxRate) || payload.taxRate < 0) throw make('taxRate must be >= 0');
  if (payload.discount === undefined) payload.discount = 0;
  if (!isNumber(payload.discount) || payload.discount < 0) throw make('discount must be >= 0');
}

function make(msg) {
  const e = new Error(msg);
  e.status = 400;
  return e;
}

module.exports = { validateCheckoutPayload };
