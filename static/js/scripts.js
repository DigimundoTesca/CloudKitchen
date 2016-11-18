$(document).ready(function () {
    /**LiveReloaded Plugin */
    // document.write('<script src="http://' + (location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1"></' + 'script>')

    $(".product-img").click(function () {
        name = $(this).siblings('.product-name').text()
        cost = $(this).siblings('.content-price').children('.product-cost').text();
        id = $(this).parent().attr('id');
        li_id = ('li-' + id).toString();

        if ( $('#' + li_id + '').length == 0) {
            $nuevo_li = $("" +
                "<li id='" + li_id + "' class='list-group-item'>" +
                "<span class='name-li text-uppercase'>"
                + name +
                "</span> " +
                "<span class='cant-li'>1</span>" +
                "<span class='total-li'>" +
                "<strong>"
                + cost +
                "</strong>" +
                "</span> " +
                "</li>");
            $nuevo_li.appendTo('#sales-list').fadeTo('fast', 1);
        } else {
            new_cant = $( 'ul#sales-list' ).find('#'+ li_id +' .cant-li').text();
            new_cant++;

            $( 'ul#sales-list' ).find('#'+ li_id +' .cant-li').text(new_cant);




        }
    });
});