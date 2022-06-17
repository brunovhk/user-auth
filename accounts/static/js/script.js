// Remove o alert após 5s
window.setTimeout(function () {
    $(".alert").fadeTo(400, 0).slideUp(400, function () {
        $(this).remove();
    });
}, 3000);
