$(document).on('click', '.update-cart', function (e) {
    e.preventDefault();

    let productKey = $(this).data('index');
    let optionValueIds = [];

    $('.option-select[data-product-id="' + productKey + '"]').each(function () {
        optionValueIds.push($(this).val());
    });

    // ✅ safest way to get the selected quantity
    let productQty = $('select[id="select' + productKey + '"] option:selected').text();

    $.ajax({
        type: 'POST',
        url: cartUpdateUrl,
        data: {
            product_id: productKey,
            product_qty: productQty,
            option_value_ids: optionValueIds,
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: function (json) {
            location.reload();
        },
        error: function (xhr, errmsg, err) {
            console.log("Error:", xhr.responseText);
        }
    });
});


//  not work
// $(document).on('click', '.update-cart', function (e) {
//     e.preventDefault();
//
//     let productKey = $(this).data('index');
//     let optionValueIds = [];  // Default to an empty array if no options selected
//     debugger
//     // Collect the selected option values for this product (if any)
//     $('.option-select[data-product-id="' + productKey + '"]').each(function() {
//         optionValueIds.push($(this).val());
//     });
//
//     $.ajax({
//         type: 'POST',
//         url: cartUpdateUrl,  // Use the variable set in the template
//         data: {
//             product_id: productKey,  // Pass item.key as the product ID
//             product_qty: $('#select' + productKey + ' option:selected').text(),
//             option_value_ids: optionValueIds,  // Include the selected option values
//             csrfmiddlewaretoken: csrfToken, // Use the CSRF token from the template
//             action: 'post'
//         },
//         success: function (json) {
//             location.reload();  // Reload to reflect changes
//         },
//         error: function (xhr, errmsg, err) {
//             console.log("Error:", xhr.responseText);
//         }
//     });
// });





// $(document).on('click', '.update-cart', function (e) {
//     e.preventDefault();
//
//     // Use item.key as the unique identifier for the cart item
//     let productKey = $(this).data('index');
//     $.ajax({
//         type: 'POST',
//         url: cartUpdateUrl,  // Use the variable set in the template
//         data: {
//             product_id: productKey,  // Pass item.key instead of product ID
//             product_qty: $('#select' + productKey + ' option:selected').text(),
//             csrfmiddlewaretoken: csrfToken, // Use the CSRF token from the template
//             action: 'post'
//         },
//         success: function (json) {
//             location.reload();  // Reload to reflect changes
//         },
//         error: function (xhr, errmsg, err) {
//             console.log("Error:", xhr.responseText);
//         }
//     });
// });



// $(document).on('click', '.update-cart', function (e) {
//     e.preventDefault();
//
//     let productID = $(this).data('index');
//
//     $.ajax({
//         type: 'POST',
//         url: cartUpdateUrl, // Use the variable set in the template
//         data: {
//             product_id: productID,
//             product_qty: $('#select' + productID + ' option:selected').text(),
//             csrfmiddlewaretoken: csrfToken, // Use the CSRF token from the template
//             action: 'post'
//         },
//         success: function (json) {
//             location.reload();
//         },
//         error: function (xhr, errmsg, err) {
//             console.log("Error:", xhr.responseText);
//         }
//     });
// });


// Work in template
// // Update
// $(document).on('click', '.update-cart', function (e) {
//     e.preventDefault();
//
//     let productID = $(this).data('index');
//
//     $.ajax({
//         type: 'POST',
//         url: "{% url 'cart_update' %}",
//         data: {
//             product_id: productID,
//             product_qty: $('#select' + productID + ' option:selected').text(),
//             csrfmiddlewaretoken: '{{ csrf_token }}',
//             action: 'post'
//         },
//
//         success: function (json) {
//             location.reload();
//         },
//
//         error: function (xhr, errmsg, err) {
//             console.log("Error:", xhr.responseText);
//         }
//     });
// });
