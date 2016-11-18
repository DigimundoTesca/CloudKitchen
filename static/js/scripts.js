$(document).ready(function () {
    /**LiveReloaded Plugin */
    // document.write('<script src="http://' + (location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1"></' + 'script>')

    $(".product-img").click(function () {
        $name = $(this).siblings('.product-name').text()

        $nuevo_li = $("" +
            "<li class='list-group-item'>" +
            "<span class='name-li text-uppercase'>"
            + $name +
            "</span> " +
            "<span class='cant-li'>2</span>" +
            "<span class='total-li'>" +
            "<strong>9.00</strong>" +
            "</span> " +
            "</li>");
        $nuevo_li.appendTo('#sales-list').fadeTo('fast', 1)
    });
});