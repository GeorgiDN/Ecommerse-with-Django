document.addEventListener("DOMContentLoaded", function () {
    $(document).on("click", ".delete-product", function (e) {
        e.preventDefault();

        let productID = $(this).data("index");

        $.ajax({
            type: "POST",
            url: cartDeleteUrl,  // Using globally defined variable from template
            data: {
                product_id: productID,
                csrfmiddlewaretoken: csrfToken, // Using global CSRF token
                action: "post"
            },
            success: function (json) {
                location.reload();
            },
            error: function (xhr, errmsg, err) {
                console.log("Error:", xhr.responseText);
            }
        });
    });
});





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
