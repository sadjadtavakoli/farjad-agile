/**
 * Created by sadjad on 28/01/18.
 */



$('document').ready(function () {
    $('.button').on('click', function () {
        var action = $(this).attr('action');
        var chang_state_url = $(this).parents('.content').find('.change-state-url').attr('value');
        var state = $(this).parents('.content').siblings('.state');
        $.ajax({
            type: 'POST',
            url: chang_state_url,
            data: {
                'action': action
            },
            headers: {
                "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function () {
                location.reload();
            }
        });
    });
});
