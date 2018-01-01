/**
 * Created by sadjad on 01/01/18.
 */


$('document').ready(function () {
    var item = document.getElementById("id_password_visibility");
    item.addEventListener("click", function () {

        if (item.classList.contains("eye")) {
            $('#id_password').attr('type', 'password');
            item.classList.remove('eye');
            item.classList.add('hide')
        } else {
            $('#id_password').attr('type', 'text');
            item.classList.remove('hide');
            item.classList.add('eye')
        }

    });

});