$(document).on('click', '.update-cart', function (e) {
    e.preventDefault();

    let productID = $(this).data('index');

    $.ajax({
        type: 'POST',
        url: cartUpdateUrl, // Use the variable set in the template
        data: {
            product_id: productID,
            product_qty: $('#select' + productID + ' option:selected').text(),
            csrfmiddlewaretoken: csrfToken, // Use the CSRF token from the template
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
