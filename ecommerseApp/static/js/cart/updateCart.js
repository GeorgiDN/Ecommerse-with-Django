$(document).on('click', '.update-cart', function (e) {
    e.preventDefault();

    let productKey = $(this).data('index');
    let optionValueIds = [];

    $('.option-select[data-product-id="' + productKey + '"]').each(function () {
        optionValueIds.push($(this).val());
    });

    let productQty = $(this).siblings('input[type="number"]').val();
    // let productQty = $(this).prev('input[type="number"]').val();

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
