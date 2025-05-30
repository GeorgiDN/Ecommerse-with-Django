$(document).on('click', '.update-cart', function (e) {
    e.preventDefault();

    let productKey = $(this).data('index');
    let inputElement = $('#input' + productKey);
    let optionValueIds = [];

    // $('.option-select[data-product-id="' + productKey + '"]').each(function () {
    //     optionValueIds.push($(this).val());
    // });

    $(`select.option-select[data-product-id="${productKey}"]`).each(function() {
        optionValueIds.push($(this).val());
    });

    let productQty = $(this).siblings('input[type="number"]').val();
    // let productQty = $(this).prev('input[type="number"]').val();

    if (productQty % 1 !== 0) {
        alert('Please enter a whole number for quantity');
        inputElement.focus();
        return false;
    }

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
            if (json.error) {
                location.reload();
                alert(json.error);
            } else {
                location.reload();
            }
        },
        error: function (xhr, errmsg, err) {
            console.log("Error:", xhr.responseText);
        }
    });
});
