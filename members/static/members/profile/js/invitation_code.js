/**
 * Created by sadjad on 30/01/18.
 */


$('document').ready(function () {
    $('#code-visibility').on('click', function () {
        $(this).css('display', 'none');
        $('#invitation-code').css('display', 'flex');
    })
});