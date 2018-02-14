/**
 * Created by sadjad on 13/02/18.
 */

$('document').ready(function () {

    $('.submit').on('click', function () {
        var cm = $('#new-comment').val();
        var url = $('#create-comment-url').val();
        if (cm.trim()) {
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'text': cm
                },
                headers: {
                    "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function () {
                    $('#new-comment').val('');
                    location.reload()
                }
            });
        }

    })
});