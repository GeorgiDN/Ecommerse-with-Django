$(document).on("click", ".delete-product", function (e) {
    e.preventDefault();

    let productKey = $(this).data("index");

    $.ajax({
        type: "POST",
        url: cartDeleteUrl,
        data: {
            product_id: productKey,
            csrfmiddlewaretoken: csrfToken,
            action: "post"
        },
        success: function (json) {
            // Optionally show feedback before reload
            console.log(`Product ${json.product} deleted`);
            location.reload();
        },
        error: function (xhr, errmsg, err) {
            console.error("Delete Error:", xhr.responseText);
        }
    });
});





// document.addEventListener("DOMContentLoaded", function () {
//     $(document).on("click", ".delete-product", function (e) {
//         e.preventDefault();
//
//         // Use item.key as the unique identifier for the cart item
//         let productKey = $(this).data("index");
//
//         $.ajax({
//             type: "POST",
//             url: cartDeleteUrl,  // Using globally defined variable from template
//             data: {
//                 product_id: productKey,  // Pass item.key instead of product ID
//                 csrfmiddlewaretoken: csrfToken, // Using global CSRF token
//                 action: "post"
//             },
//             success: function (json) {
//                 location.reload();  // Reload to reflect changes
//             },
//             error: function (xhr, errmsg, err) {
//                 console.log("Error:", xhr.responseText);
//             }
//         });
//     });
// });




// document.addEventListener("DOMContentLoaded", function () {
//     $(document).on("click", ".delete-product", function (e) {
//         e.preventDefault();
//
//         let productID = $(this).data("index");
//
//         $.ajax({
//             type: "POST",
//             url: cartDeleteUrl,  // Using globally defined variable from template
//             data: {
//                 product_id: productID,
//                 csrfmiddlewaretoken: csrfToken, // Using global CSRF token
//                 action: "post"
//             },
//             success: function (json) {
//                 location.reload();
//             },
//             error: function (xhr, errmsg, err) {
//                 console.log("Error:", xhr.responseText);
//             }
//         });
//     });
// });





// Work in template
// // Delete
// $(document).on('click', '.delete-product', function (e) {
//     e.preventDefault();
//
//     let productID = $(this).data('index');
//
//     $.ajax({
//         type: 'POST',
//         url: "{% url 'cart_delete' %}",
//         data: {
//             product_id: productID,
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
