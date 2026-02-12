// script.js

document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to all remove buttons
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();

            const cartId = button.getAttribute('data-cart-id');
            removeCartItem(cartId);
        });
    });

    function updateCartTable() {
        // Use a direct URL to fetch the updated HTML content
        fetch('/cart')
            .then(response => response.text())
            .then(html => {
                const cartTable = document.getElementById('cart-table');
                cartTable.innerHTML = html;
            })
            .catch(error => console.error(error));
    }
});
