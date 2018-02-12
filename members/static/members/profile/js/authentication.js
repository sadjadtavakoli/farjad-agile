/**
 * Created by sadjad on 12/02/18.
 */
$('document').ready(function () {

    $('.submit-phone').on('click', function () {
        var phone = $(this).parent().find('#phone-one').val();
        var url = $('#code-url').val();
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'phone': phone
            },
            headers: {
                "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                console.log(response);
                if (response['is_valid'] == true) {
                    $('#id_phone').attr('value', phone);
                    $('.first-form').attr('hidden', 'hidden');
                    $('.second-form').removeAttr('hidden');
                } else {
                    $('#one-error').html(response['error'])
                }
            }
        });
    })
});