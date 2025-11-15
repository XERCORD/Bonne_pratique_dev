
// Frontend logic: dynamic items, fetch API, theme toggle, particles background, loader handling, animated result
const q = sel => document.querySelector(sel);
const itemsList = q('#itemsList');
const addItemBtn = q('#addItemBtn');
const form = q('#checkoutForm');
const resultOutput = q('#resultOutput');
const loader = q('#loader');
const resetBtn = q('#resetBtn');
const themeToggle = q('#themeToggle');
const particles = q('#particles');

function createItem(name = '', price = '', qty = '1') {
  const row = document.createElement('div');
  row.className = 'item-row';
  row.innerHTML = `
    <input type="text" placeholder="Item name" value="${name}" aria-label="Item name">
    <input type="number" placeholder="Price" step="0.01" value="${price}" aria-label="Item price">
    <input type="number" placeholder="Qty" min="1" value="${qty}" aria-label="Item quantity">
    <button type="button" class="btn remove" aria-label="Remove item">✕</button>
  `;
  row.querySelector('.remove').onclick = () => {
    row.remove();
    if (!itemsList.children.length) addItem();
  };
  itemsList.appendChild(row);
  return row;
}

function addItem(){ createItem('', '', '1'); }
addItemBtn.addEventListener('click', addItem);
addItem();

function setTheme(light){
  if(light){
    document.body.classList.add('light');
    themeToggle.textContent = '☀️';
    themeToggle.setAttribute('aria-pressed','true');
  } else {
    document.body.classList.remove('light');
    themeToggle.textContent = '🌙';
    themeToggle.setAttribute('aria-pressed','false');
  }
  localStorage.setItem('neo-theme', light ? 'light' : 'dark');
}
themeToggle.addEventListener('click', ()=> setTheme(!document.body.classList.contains('light')));
const saved = localStorage.getItem('neo-theme');
if(saved === 'light') setTheme(true);

function showLoading(show){ loader.setAttribute('aria-hidden', show ? 'false' : 'true'); loader.style.visibility = show ? 'visible' : 'hidden'; }

function showResult(obj){
  resultOutput.style.opacity = '0';
  setTimeout(()=> {
    resultOutput.textContent = JSON.stringify(obj, null, 2);
    resultOutput.style.transition = 'opacity 300ms ease';
    resultOutput.style.opacity = '1';
  }, 120);
}

function collectPayload(){
  const items = Array.from(itemsList.children).map(r=>{
    const inputs = r.querySelectorAll('input');
    return { name: inputs[0].value || '', price: parseFloat(inputs[1].value) || 0, quantity: parseInt(inputs[2].value) || 1 };
  });
  const taxRate = parseFloat(q('#taxRate').value) || 0;
  const discount = parseFloat(q('#discount').value) || 0;
  return { items, taxRate, discount };
}

function validate(p){
  if(!Array.isArray(p.items) || p.items.length===0) return 'Add at least one item';
  for(const it of p.items){
    if(!it.name) return 'Each item must have a name';
    if(!isFinite(it.price) || it.price<0) return 'Item price must be >= 0';
    if(!Number.isInteger(it.quantity) || it.quantity<=0) return 'Quantity must be positive integer';
  }
  if(!isFinite(p.taxRate) || p.taxRate<0) return 'Tax rate must be >= 0';
  if(!isFinite(p.discount) || p.discount<0) return 'Discount must be >= 0';
  return null;
}

form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const payload = collectPayload();
  const err = validate(payload);
  if(err){ showResult({ error: err }); return; }
  try{
    showLoading(true);
    const res = await fetch('/api/checkout', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const body = await res.json();
    showResult(body);
  } catch(err){
    showResult({ error: err.message });
  } finally{
    showLoading(false);
  }
});

resetBtn.addEventListener('click', ()=>{
  itemsList.innerHTML = '';
  addItem();
  q('#taxRate').value = '';
  q('#discount').value = '';
  resultOutput.textContent = 'No calculation yet.';
});

// lightweight particle effect using DOM
function spawnParticles(count=28){
  particles.innerHTML = '';
  for(let i=0;i<count;i++){
    const el = document.createElement('div');
    el.className = 'particle';
    const size = 8 + Math.random()*36;
    el.style.width = el.style.height = size + 'px';
    el.style.left = (Math.random()*110) + '%';
    el.style.top = (Math.random()*100) + '%';
    el.style.opacity = 0.06 + Math.random()*0.2;
    particles.appendChild(el);
  }
}
spawnParticles(28);
window.addEventListener('resize', ()=> spawnParticles(window.innerWidth < 600 ? 14 : 28));
