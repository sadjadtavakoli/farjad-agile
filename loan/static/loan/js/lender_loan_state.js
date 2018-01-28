/**
 * Created by sadjad on 28/01/18.
 */



$('document').ready(function () {
    $('.button').on('click', function () {
        var action = $(this).attr('action');
        var chang_state_url = $(this).siblings('.change-state-url').attr('value');
        $.ajax({
            type: 'POST',
            url: chang_state_url,
            data: {
                'action': action
            },
            headers: {
                "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (result) {

            }
        });
    })
});
