// Frontend JavaScript for Checkout NeoGlass
let items = [];

// DOM Elements
const itemsList = document.getElementById('itemsList');
const addItemBtn = document.getElementById('addItemBtn');
const checkoutForm = document.getElementById('checkoutForm');
const resetBtn = document.getElementById('resetBtn');
const loader = document.getElementById('loader');
const ticketContainer = document.getElementById('ticketContainer');
const ticketItems = document.getElementById('ticketItems');
const ticketTotals = document.getElementById('ticketTotals');
const ticketDate = document.getElementById('ticketDate');
const themeToggle = document.getElementById('themeToggle');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadTheme();
  updateItemsList();
  createParticles();
});

// Theme Toggle
if (themeToggle) {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'light') {
    document.body.classList.add('light');
    themeToggle.textContent = '☀️';
    themeToggle.setAttribute('aria-pressed', 'true');
  }

  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light');
    const isLight = document.body.classList.contains('light');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    themeToggle.textContent = isLight ? '☀️' : '🌙';
    themeToggle.setAttribute('aria-pressed', isLight);
  });
}

function loadTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'light') {
    document.body.classList.add('light');
  }
}

// Add Item
if (addItemBtn) {
  addItemBtn.addEventListener('click', () => {
    items.push({ name: '', price: 0, quantity: 1 });
    updateItemsList();
  });
}

// Update Items List
function updateItemsList() {
  if (!itemsList) return;
  
  itemsList.innerHTML = '';
  
  if (items.length === 0) {
    itemsList.innerHTML = '<p style="color: var(--muted); text-align: center; padding: 20px;">No items added</p>';
    return;
  }

  items.forEach((item, index) => {
    const row = document.createElement('div');
    row.className = 'item-row';
    row.innerHTML = `
      <input type="text" placeholder="Item name" value="${item.name}" data-index="${index}" data-field="name" />
      <input type="number" step="0.01" placeholder="Price" value="${item.price}" data-index="${index}" data-field="price" />
      <input type="number" step="1" min="1" placeholder="Qty" value="${item.quantity}" data-index="${index}" data-field="quantity" />
      <button type="button" class="btn" data-index="${index}" data-action="remove" style="padding: 8px; min-width: 40px;">×</button>
    `;
    itemsList.appendChild(row);
  });

  // Attach event listeners
  itemsList.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', (e) => {
      const index = parseInt(e.target.dataset.index);
      const field = e.target.dataset.field;
      const value = field === 'name' ? e.target.value : parseFloat(e.target.value) || 0;
      items[index][field] = value;
    });
  });

  itemsList.querySelectorAll('[data-action="remove"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const index = parseInt(e.target.dataset.index);
      items.splice(index, 1);
      updateItemsList();
    });
  });
}

// Form Submit
if (checkoutForm) {
  checkoutForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const taxRate = parseFloat(document.getElementById('taxRate')?.value || 0);
    const discount = parseFloat(document.getElementById('discount')?.value || 0);
    
    // Validate items
    const validItems = items.filter(item => item.name && item.price > 0 && item.quantity > 0);
    
    if (validItems.length === 0) {
      showError('Please add at least one valid item');
      return;
    }

    // Show loader
    if (loader) loader.setAttribute('aria-hidden', 'false');
    
    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          items: validItems,
          taxRate,
          discount
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Calculation error');
      }

      const result = await response.json();
      displayResult(validItems, result, taxRate, discount);
    } catch (error) {
      showError(error.message || 'An error occurred');
    } finally {
      if (loader) loader.setAttribute('aria-hidden', 'true');
    }
  });
}

// Reset
if (resetBtn) {
  resetBtn.addEventListener('click', () => {
    items = [];
    updateItemsList();
    if (checkoutForm) checkoutForm.reset();
    if (ticketContainer) {
      ticketItems.innerHTML = '<div class="ticket-empty">No calculation yet</div>';
      ticketTotals.innerHTML = '';
    }
  });
}

// Display Result
function displayResult(items, result, taxRate, discount) {
  if (!ticketItems || !ticketTotals) return;

  // Update date
  if (ticketDate) {
    ticketDate.textContent = new Date().toLocaleString('en-US');
  }

  // Display items
  ticketItems.innerHTML = items.map(item => `
    <div class="ticket-item">
      <div class="ticket-item-name">${item.name}</div>
      <div class="ticket-item-details">${item.quantity} × ${item.price.toFixed(2)}€</div>
      <div class="ticket-item-price">${(item.price * item.quantity).toFixed(2)}€</div>
    </div>
  `).join('');

  // Display totals
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const appliedDiscount = Math.min(discount, subtotal);
  const subtotalAfterDiscount = subtotal - appliedDiscount;
  
  ticketTotals.innerHTML = `
    <div class="ticket-total-row subtotal">
      <span class="ticket-total-label">Subtotal</span>
      <span class="ticket-total-value">${subtotal.toFixed(2)}€</span>
    </div>
    ${appliedDiscount > 0 ? `
    <div class="ticket-total-row discount">
      <span class="ticket-total-label">Discount</span>
      <span class="ticket-total-value">-${appliedDiscount.toFixed(2)}€</span>
    </div>
    ` : ''}
    ${taxRate > 0 ? `
    <div class="ticket-total-row tax">
      <span class="ticket-total-label">Tax (${(taxRate * 100).toFixed(0)}%)</span>
      <span class="ticket-total-value">${result.taxAmount.toFixed(2)}€</span>
    </div>
    ` : ''}
    <div class="ticket-total-row final">
      <span class="ticket-total-label">Total</span>
      <span class="ticket-total-value">${result.total.toFixed(2)}€</span>
    </div>
  `;

  // Add printing animation
  const ticket = document.getElementById('ticket');
  if (ticket) {
    ticket.classList.add('printing');
    setTimeout(() => ticket.classList.remove('printing'), 800);
  }
}

// Show Error
function showError(message) {
  if (!ticketItems) return;
  ticketItems.innerHTML = `<div class="ticket-error">${message}</div>`;
  ticketTotals.innerHTML = '';
}

// Create Particles
function createParticles() {
  const particlesContainer = document.getElementById('particles');
  if (!particlesContainer) return;

  for (let i = 0; i < 15; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 10 + 's';
    particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
    particlesContainer.appendChild(particle);
  }
}

