// Configuration
let cartItems = [];
let apiBaseUrl = 'http://localhost:5001';

// Fonction pour obtenir l'URL de l'API
function getApiUrl() {
    const urlInput = document.getElementById('api-url');
    if (urlInput) {
        apiBaseUrl = urlInput.value || 'http://localhost:5001';
    }
    return apiBaseUrl;
}

// Vérifier la santé de l'API
async function checkApiHealth() {
    const statusDiv = document.getElementById('api-status');
    const apiUrl = getApiUrl();
    
    statusDiv.innerHTML = '<span class="loading">Vérification en cours...</span>';
    
    try {
        const response = await fetch(`${apiUrl}/health`);
        if (response.ok) {
            const data = await response.json();
            statusDiv.innerHTML = '<span class="success">✅ API connectée et fonctionnelle</span>';
        } else {
            statusDiv.innerHTML = '<span class="error">❌ API non disponible</span>';
        }
    } catch (error) {
        statusDiv.innerHTML = `<span class="error">❌ Erreur de connexion: ${error.message}</span>`;
    }
}

// Créer un produit
async function createProduct(event) {
    event.preventDefault();
    const resultDiv = document.getElementById('product-result');
    const apiUrl = getApiUrl();
    
    const product = {
        id: document.getElementById('product-id').value,
        name: document.getElementById('product-name').value,
        price: document.getElementById('product-price').value,
        category: document.getElementById('product-category').value
    };
    
    resultDiv.innerHTML = '<span class="loading">Création en cours...</span>';
    
    try {
        const response = await fetch(`${apiUrl}/products`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(product)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultDiv.innerHTML = `
                <div class="success-box">
                    <strong>✅ Produit créé avec succès !</strong><br>
                    ID: ${data.id}<br>
                    Nom: ${data.name}
                </div>
            `;
            // Afficher une notification
            showToast(`Produit "${data.name}" créé avec succès !`, 'success');
            // Réinitialiser le formulaire
            document.getElementById('product-form').reset();
            // Recharger la liste des produits
            loadProducts();
        } else {
            resultDiv.innerHTML = `
                <div class="error-box">
                    <strong>❌ Erreur:</strong> ${data.error}
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="error-box">
                <strong>❌ Erreur de connexion:</strong> ${error.message}
            </div>
        `;
    }
}

// Créer une remise
async function createDiscount(event) {
    event.preventDefault();
    const resultDiv = document.getElementById('discount-result');
    const apiUrl = getApiUrl();
    
    const discount = {
        code: document.getElementById('discount-code').value,
        type: document.getElementById('discount-type').value,
        value: document.getElementById('discount-value').value
    };
    
    const minAmount = document.getElementById('discount-min-amount').value;
    if (minAmount) {
        discount.min_amount = minAmount;
    }
    
    const category = document.getElementById('discount-category').value;
    if (category) {
        discount.category = category;
    }
    
    resultDiv.innerHTML = '<span class="loading">Création en cours...</span>';
    
    try {
        const response = await fetch(`${apiUrl}/discounts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(discount)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultDiv.innerHTML = `
                <div class="success-box">
                    <strong>✅ Remise créée avec succès !</strong><br>
                    Code: ${data.code}
                </div>
            `;
            // Afficher une notification
            showToast(`Remise "${data.code}" créée avec succès !`, 'success');
            // Réinitialiser le formulaire
            document.getElementById('discount-form').reset();
        } else {
            resultDiv.innerHTML = `
                <div class="error-box">
                    <strong>❌ Erreur:</strong> ${data.error}
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="error-box">
                <strong>❌ Erreur de connexion:</strong> ${error.message}
            </div>
        `;
    }
}

// Afficher une notification toast
function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️'
    };
    
    const icon = icons[type] || icons.info;
    
    toast.innerHTML = `
        <div class="toast-icon">${icon}</div>
        <div class="toast-message">${message}</div>
        <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
    `;
    
    container.appendChild(toast);
    
    // Animation d'entrée
    setTimeout(() => {
        toast.classList.add('toast-show');
    }, 10);
    
    // Suppression automatique
    if (duration > 0) {
        setTimeout(() => {
            toast.classList.remove('toast-show');
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, 300);
        }, duration);
    }
}

// Ajouter au panier
async function addToCart(event) {
    event.preventDefault();
    const apiUrl = getApiUrl();
    const productId = document.getElementById('cart-product-id').value;
    const quantity = parseInt(document.getElementById('cart-quantity').value);
    
    if (!productId) {
        showToast('Veuillez entrer un ID de produit', 'warning');
        return;
    }
    
    // Vérifier que le produit existe
    try {
        const response = await fetch(`${apiUrl}/products/${productId}`);
        if (!response.ok) {
            showToast(`Produit "${productId}" non trouvé. Créez d'abord le produit.`, 'error');
            return;
        }
        
        const product = await response.json();
        
        // Ajouter au panier local
        const existingItem = cartItems.find(item => item.product_id === productId);
        if (existingItem) {
            existingItem.quantity += quantity;
            showToast(`${quantity} × ${product.name} ajouté au panier (quantité mise à jour)`, 'success');
        } else {
            cartItems.push({
                product_id: productId,
                quantity: quantity,
                product: product
            });
            showToast(`${quantity} × ${product.name} ajouté au panier`, 'success');
        }
        
        updateCartDisplay();
        document.getElementById('cart-product-id').value = '';
        document.getElementById('cart-quantity').value = 1;
    } catch (error) {
        showToast(`Erreur de connexion: ${error.message}`, 'error');
    }
}

// Mettre à jour l'affichage du panier
function updateCartDisplay() {
    const cartItemsDiv = document.getElementById('cart-items');
    
    if (cartItems.length === 0) {
        cartItemsDiv.innerHTML = '<p class="empty-cart">Aucun article dans le panier</p>';
        return;
    }
    
    let html = '<div class="cart-items-list">';
    cartItems.forEach((item, index) => {
        const product = item.product || { name: item.product_id, price: 'N/A' };
        html += `
            <div class="cart-item">
                <div class="cart-item-info">
                    <strong>${product.name || item.product_id}</strong>
                    <span class="cart-item-details">
                        ${product.price ? `${product.price}€` : ''} × ${item.quantity}
                    </span>
                </div>
                <button onclick="removeCartItem(${index})" class="btn-remove">✕</button>
            </div>
        `;
    });
    html += '</div>';
    cartItemsDiv.innerHTML = html;
}

// Retirer un article du panier
function removeCartItem(index) {
    cartItems.splice(index, 1);
    updateCartDisplay();
}

// Vider le panier
function clearCart() {
    if (cartItems.length === 0) {
        showToast('Le panier est déjà vide', 'info');
        return;
    }
    
    // Créer une notification de confirmation personnalisée
    const confirmToast = document.createElement('div');
    confirmToast.className = 'toast toast-warning toast-confirm';
    confirmToast.innerHTML = `
        <div class="toast-icon">⚠️</div>
        <div class="toast-message">Voulez-vous vraiment vider le panier ?</div>
        <div class="toast-actions">
            <button class="toast-btn toast-btn-confirm" onclick="confirmClearCart()">Oui</button>
            <button class="toast-btn toast-btn-cancel" onclick="this.closest('.toast').remove()">Non</button>
        </div>
    `;
    
    const container = document.getElementById('toast-container');
    container.appendChild(confirmToast);
    setTimeout(() => confirmToast.classList.add('toast-show'), 10);
}

// Confirmer la suppression du panier
function confirmClearCart() {
    cartItems = [];
    updateCartDisplay();
    document.getElementById('checkout-result').innerHTML = '';
    showToast('Panier vidé avec succès', 'success');
    
    // Supprimer la notification de confirmation
    const confirmToast = document.querySelector('.toast-confirm');
    if (confirmToast) {
        confirmToast.classList.remove('toast-show');
        setTimeout(() => confirmToast.remove(), 300);
    }
}

// Calculer le checkout
async function calculateCheckout(event) {
    event.preventDefault();
    const resultDiv = document.getElementById('checkout-result');
    const apiUrl = getApiUrl();
    
    if (cartItems.length === 0) {
        resultDiv.innerHTML = `
            <div class="error-box">
                <strong>❌ Le panier est vide !</strong>
            </div>
        `;
        return;
    }
    
    const checkoutData = {
        items: cartItems.map(item => ({
            product_id: item.product_id,
            quantity: item.quantity
        }))
    };
    
    const discountCode = document.getElementById('checkout-discount-code').value;
    if (discountCode) {
        checkoutData.discount_code = discountCode;
    }
    
    resultDiv.innerHTML = '<span class="loading">Calcul en cours...</span>';
    
    try {
        const response = await fetch(`${apiUrl}/checkout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(checkoutData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultDiv.innerHTML = `
                <div class="checkout-success">
                    <h4>💰 Résultat du checkout</h4>
                    <div class="checkout-details">
                        <div class="checkout-line">
                            <span>Sous-total :</span>
                            <strong>${parseFloat(data.subtotal).toFixed(2)}€</strong>
                        </div>
                        ${parseFloat(data.discount_amount) > 0 ? `
                            <div class="checkout-line discount">
                                <span>Remise :</span>
                                <strong>-${parseFloat(data.discount_amount).toFixed(2)}€</strong>
                            </div>
                            <div class="checkout-line">
                                <span>Sous-total après remise :</span>
                                <strong>${parseFloat(data.subtotal_after_discount).toFixed(2)}€</strong>
                            </div>
                        ` : ''}
                        <div class="checkout-line">
                            <span>Taxes :</span>
                            <strong>${parseFloat(data.tax_amount).toFixed(2)}€</strong>
                        </div>
                        <div class="checkout-line total">
                            <span>Total :</span>
                            <strong>${parseFloat(data.total).toFixed(2)}€</strong>
                        </div>
                    </div>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="error-box">
                    <strong>❌ Erreur:</strong> ${data.error}
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="error-box">
                <strong>❌ Erreur de connexion:</strong> ${error.message}
            </div>
        `;
    }
}

// Toggle les champs de remise
function toggleDiscountFields() {
    const type = document.getElementById('discount-type').value;
    const valueLabel = document.querySelector('label[for="discount-value"]');
    if (valueLabel) {
        if (type === 'percentage') {
            valueLabel.textContent = 'Valeur (%) :';
        } else {
            valueLabel.textContent = 'Valeur (€) :';
        }
    }
}

// Charger et afficher tous les produits
async function loadProducts() {
    const productsListDiv = document.getElementById('products-list');
    const apiUrl = getApiUrl();
    
    if (!productsListDiv) return;
    
    productsListDiv.innerHTML = '<span class="loading">Chargement des produits...</span>';
    
    try {
        const response = await fetch(`${apiUrl}/products`);
        const data = await response.json();
        
        if (response.ok && data.products && data.products.length > 0) {
            let html = '';
            data.products.forEach(product => {
                const categoryEmoji = {
                    'food': '🍔',
                    'electronics': '💻',
                    'clothing': '👕',
                    'other': '📦'
                }[product.category] || '📦';
                
                html += `
                    <div class="product-card">
                        <div class="product-icon">${categoryEmoji}</div>
                        <div class="product-info">
                            <h4 class="product-name">${product.name}</h4>
                            <p class="product-id">ID: ${product.id}</p>
                            <p class="product-category">Catégorie: ${product.category}</p>
                            <p class="product-price">${parseFloat(product.price).toFixed(2)}€</p>
                        </div>
                    </div>
                `;
            });
            productsListDiv.innerHTML = html;
        } else {
            productsListDiv.innerHTML = '<p class="empty-state">Aucun produit créé pour le moment</p>';
        }
    } catch (error) {
        productsListDiv.innerHTML = `
            <div class="error-box">
                <strong>❌ Erreur de connexion:</strong> ${error.message}
            </div>
        `;
    }
}

// Afficher une documentation dans la modal
async function showDocumentation(filePath, title) {
    const modal = document.getElementById('doc-modal');
    const modalTitle = document.getElementById('doc-modal-title');
    const modalContent = document.getElementById('doc-modal-content');
    const modalLoading = document.getElementById('doc-modal-loading');
    
    // Afficher la modal
    modal.style.display = 'flex';
    modalTitle.textContent = title;
    modalContent.innerHTML = '';
    modalLoading.style.display = 'block';
    
    try {
        // Charger le fichier Markdown
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`Erreur ${response.status}: ${response.statusText}`);
        }
        
        const markdown = await response.text();
        
        // Convertir le Markdown en HTML avec marked.js
        if (typeof marked !== 'undefined') {
            const html = marked.parse(markdown);
            modalContent.innerHTML = html;
        } else {
            // Fallback si marked.js n'est pas chargé
            modalContent.innerHTML = `<pre>${markdown}</pre>`;
        }
        
        modalLoading.style.display = 'none';
        
        // Scroll en haut du contenu
        modalContent.scrollTop = 0;
    } catch (error) {
        modalLoading.style.display = 'none';
        modalContent.innerHTML = `
            <div class="error-box">
                <strong>❌ Erreur lors du chargement de la documentation:</strong><br>
                ${error.message}
            </div>
        `;
    }
}

// Fermer la modal de documentation
function closeDocModal() {
    const modal = document.getElementById('doc-modal');
    modal.style.display = 'none';
}

// Fermer la modal avec la touche Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeDocModal();
    }
});

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Mettre à jour l'URL de l'API si elle change
    const apiUrlInput = document.getElementById('api-url');
    if (apiUrlInput) {
        apiUrlInput.addEventListener('change', function() {
            apiBaseUrl = this.value || 'http://localhost:5001';
        });
    }
    
    updateCartDisplay();
    // Charger les produits au chargement de la page
    loadProducts();
});

