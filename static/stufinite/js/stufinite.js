$.ajax({
    url: 'http://login.stufinite.faith/auth/get_username',
    dataType: 'text/plaintext',
    xhrFields: {
        withCredentials: true
    }
}).always(function(xhr, ajaxOptions, thrownError) {
    var data = xhr.responseText;
    if (data == 'None') {
        $('#stufinite-nav-login').html(
            '<a href="http://login.stufinite.faith/accounts/login"><button class="stufinite-btn">Login</button></a>'
        );
    } else {
        $('#stufinite-nav-login').html(
            '<span class="stufinite-nav-user-info">' +
            data +
            '</span>' +
            '<a href="http://login.stufinite.faith/accounts/logout"><button class="stufinite-btn">Logout</button></a>'
        )
    }
});
