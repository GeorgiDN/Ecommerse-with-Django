function updateTotalPrice(productID) {
    let priceElement = document.querySelector(`#select${productID}`).closest('.cart-info').querySelector('.product-price');
    let quantityElement = document.querySelector(`#select${productID}`);
    let totalElement = document.querySelector(`#select${productID}`).closest('.cart-info').querySelector('.total-sum-per-product');

    if (!priceElement || !quantityElement || !totalElement) return;

    let price = parseFloat(priceElement.textContent.trim());
    let quantity = parseInt(quantityElement.value);

    let total = (price * quantity).toFixed(2);
    totalElement.innerHTML = `<b>Total Price:</b> ${total} €`;
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.cart-info').forEach(cartItem => {
        let updateButton = cartItem.querySelector('.update-cart');
        if (updateButton) {
            let productID = updateButton.getAttribute('data-index');
            updateTotalPrice(productID);
        }
    });

    // Update total price when quantity is changed
    document.querySelectorAll('.form-select').forEach(select => {
        select.addEventListener('change', function () {
            let productID = this.id.replace('select', '');
            updateTotalPrice(productID);
        });
    });
});




// Work in template
// function updateTotalPrice(productID) {
//     let priceElement = document.querySelector(`#select${productID}`).closest('.cart-info').querySelector('.product-price');
//     let quantityElement = document.querySelector(`#select${productID}`);
//     let totalElement = document.querySelector(`#select${productID}`).closest('.cart-info').querySelector('.total-sum-per-product');
//
//     let price = parseFloat(priceElement.textContent.trim());
//     let quantity = parseInt(quantityElement.value);
//
//     let total = (price * quantity).toFixed(2);
//
//     totalElement.innerHTML = `<b>Total Price:</b> ${total} €`;
// }
//
// document.addEventListener("DOMContentLoaded", function () {
//     document.querySelectorAll('.cart-info').forEach(cartItem => {
//         let productID = cartItem.querySelector('.update-cart').getAttribute('data-index');
//         updateTotalPrice(productID);
//     });
// });
//
// // Update total price when quantity is changed
// document.querySelectorAll('.form-select').forEach(select => {
//     select.addEventListener('change', function () {
//         let productID = this.id.replace('select', '');
//         updateTotalPrice(productID);
//     });
// });
