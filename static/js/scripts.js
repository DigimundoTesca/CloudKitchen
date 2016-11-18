$(document).ready(function () {
    /**LiveReloaded Plugin */
    // document.write('<script src="http://' + (location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1"></' + 'script>')

    $(".product-img").click(function () {
        name = $(this).siblings('.product-name').text()
        cost = parseFloat($(this).siblings('.content-price').children('.product-cost').text());
        id = $(this).parent().attr('id');
        li_id = ('li-' + id).toString();


        if ($('#' + li_id + '').length != 0) {
            cant = $('ul#sales-list').find('#' + li_id + ' .cant-li').text();
            cant++;
            $('ul#sales-list').find('#' + li_id + ' .cant-li').text(cant);

            new_cost = cost * cant;
            if (new_cost % 2 != 0)
                cost.toFixed(2)

            new_cost += '.00'

            $('ul#sales-list').find('#' + li_id + ' .total-li').text(new_cost);

        } else {
            if (cost % 2 != 0)
                cost.toFixed(2)
            cost += '.00';
            console.log(typeof (cost))

            $nuevo_li = $("" +
                "<li id='" + li_id + "' class='list-group-item'>" +
                "<span class='name-li text-uppercase'>" + name + "</span> " +
                "<span class='cant-li'>1</span>"+
                "<span class='font-weight-bold s-li'>$ </span>" +
                "<span class='total-li font-weight-bold'>" + cost + "</span> " +
                "</li>");
            $nuevo_li.appendTo('#sales-list').fadeTo('fast', 1);
        }
    });
});