/**
 * Created by sadjad on 12/02/18.
 */
$('document').ready(function () {

    $('.submit-phone').on('click', function () {
        var phone = $(this).siblings('.field').find('#id_phone').val();
        var url = $('#code-url').val();
        $.ajax({
            type: 'GET',
            url: url,
            data: {
                'phone': phone
            },
            success: function (response) {
                if (response['is_valid'] = 'True') {
                    $('#id_phone').attr('value', phone);
                    $('.first-form').attr('hidden', 'hidden');
                    $('.second-form').removeAttr('hidden');
                } else {
                    console.log('an')
                }
            }
        });
    })
});