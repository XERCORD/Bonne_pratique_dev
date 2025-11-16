# Bug Report — Discount Applied Incorrectly

## Title
Discount exceeding subtotal not properly capped, resulting in negative total

## Context
During testing of the checkout API, a user attempted to apply a discount of 150€ on a cart with a subtotal of 100€. The system should cap the discount at the subtotal value (100€), but instead allowed the discount to exceed the subtotal, resulting in a negative total.

**Environment:**
- Node.js v18.x
- Express 4.18.2
- Service: `checkoutService.js`

## Steps to Reproduce

1. Send a POST request to `/api/checkout` with the following payload:
```json
{
  "items": [
    { "name": "Product A", "price": 100, "quantity": 1 }
  ],
  "taxRate": 0.2,
  "discount": 150
}
```

2. Observe the response

## Expected Result

The discount should be capped at the subtotal (100€), resulting in:
- Subtotal: 100€
- Applied discount: 100€ (capped)
- Subtotal after discount: 0€
- Tax (20%): 0€
- **Total: 0€**

## Observed Result

The discount was not properly capped, resulting in:
- Subtotal: 100€
- Applied discount: 150€ (should be 100€)
- Subtotal after discount: -50€
- Tax (20%): -10€
- **Total: -60€** ❌

## Log Excerpt

```
2025-11-16 10:30:15 [info]: Incoming request {"method":"POST","path":"/api/checkout","ip":"::1"}
2025-11-16 10:30:15 [info]: Checkout computed {"itemCount":1,"totalBeforeTax":-50}
```

## Root Cause

In `src/services/checkoutService.js`, the discount calculation was missing the cap logic:

```javascript
// BEFORE (buggy code)
function calculateCheckout({ items, taxRate = 0, discount = 0 }) {
  const subtotal = items.reduce((acc, it) => acc + it.price * it.quantity, 0);
  const appliedDiscount = discount; // ❌ No cap applied
  const subtotalAfterDiscount = subtotal - appliedDiscount;
  // ...
}
```

The discount was directly applied without checking if it exceeded the subtotal.

## Fix

Added proper discount capping using `Math.min()` to ensure the discount never exceeds the subtotal:

```javascript
// AFTER (fixed code)
function calculateCheckout({ items, taxRate = 0, discount = 0 }) {
  const subtotal = items.reduce((acc, it) => acc + it.price * it.quantity, 0);
  const appliedDiscount = Math.min(Math.max(Number(discount) || 0, 0), subtotal); // ✅ Capped
  const subtotalAfterDiscount = subtotal - appliedDiscount;
  // ...
}
```

**Changes made:**
- Added `Math.min(discount, subtotal)` to cap the discount
- Added `Math.max(..., 0)` to ensure discount is never negative
- Added `Number()` conversion for type safety

## Added Non-Regression Test

Added a test case in `tests/checkoutService.test.js` to prevent regression:

```javascript
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
```

## Impact

- **Severity:** Medium
- **Priority:** High
- **Affected users:** Any user applying a discount exceeding the cart subtotal
- **Status:** ✅ Fixed and tested
