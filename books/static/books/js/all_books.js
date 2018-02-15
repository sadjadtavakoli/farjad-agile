/**
 * Created by sadjad on 31/01/18.
 */


$('document').ready(function () {
    var url = $('#create-loan-url').attr('value');
    $('.loan-request').on('click', function () {
        var button = $(this);

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'book': button.siblings('.book-id').val()
            },
            headers: {
                "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                if (response['error']) {
                    alert(response['error'])
                } else {
                    console.log(button.siblings('.loan-state'));
                    button.siblings('.loan-state').css('display', 'flex');
                    button.css('display', 'none');
                    button.siblings('.loan-state').text(response['state']);
                }

            }
        });
    });
});