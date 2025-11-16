function calculateCheckout({ items, taxRate = 0, discount = 0 }) {
  const subtotal = items.reduce((acc, it) => acc + it.price * it.quantity, 0);
  const appliedDiscount = Math.min(Math.max(Number(discount) || 0, 0), subtotal);
  const subtotalAfterDiscount = subtotal - appliedDiscount;
  const taxAmount = round2(subtotalAfterDiscount * Number(taxRate || 0));
  const total = round2(subtotalAfterDiscount + taxAmount);
  return { totalBeforeTax: round2(subtotalAfterDiscount), taxAmount, total };
}

function round2(n) {
  return Math.round((n + Number.EPSILON) * 100) / 100;
}

module.exports = { calculateCheckout };
