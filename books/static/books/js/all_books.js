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
            success: function () {
                button.siblings('.cancel-request').css('display', 'flex');
                button.css('display', 'none');
            }
        });
    });

    $('.cancel-request').on('click', function () {
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'book': $(this).siblings('.book-id').val()
            },
            headers: {
                "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
            }
        });
    })
});