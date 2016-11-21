$(document).ready(function () {
    /**LiveReloaded Plugin */
    // document.write('<script src="http://' + (location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1"></' + 'script>')

    $(".product-img").click(function () {
        name = $(this).siblings('.product-name').text();
        cost = parseFloat($(this).siblings('.content-price').children('.product-cost').text());
        id = $(this).parent().attr('id');
        li_id = ('li-' + id).toString();

        if ($('#' + li_id + '').length != 0) {
            cant = $('ul#sales-list').find('#' + li_id + ' .cant-li').text();
            cant++;
            $('ul#sales-list').find('#' + li_id + ' .cant-li').text(cant);

            new_cost = cost * cant;
            if (new_cost % 2 != 0)
                cost.toFixed(2);

            new_cost += '.00';

            $('ul#sales-list').find('#' + li_id + ' .total-li').text(new_cost);

        } else {
            if (cost % 2 != 0)
                cost.toFixed(2);

            cost += '.00';

            $nuevo_li = $("" +
                "<li id='" + li_id + "' class='list-group-item'>" +
                    "<span class='name-li text-uppercase'>" + name + "</span> " +
                    "<span class='remove-icon-li'><i class='material-icons'>remove</i></span>" +
                    "<span class='cant-li'>1</span>"+
                    "<span class='add-icon-li'><i class='material-icons'>add</i></span>" +
                    "<span class='font-weight-bold s-li'>$ </span>" +
                    "<span class='total-li font-weight-bold'>" + cost + "</span> " +
                "</li>");
            $nuevo_li.appendTo('#sales-list').fadeTo('slow', 1);
        }

        // Modificacion del total general

        var total = 0

        $('ul li').find('.total-li').each(function(){
            re = $(this).text()
            total += parseFloat(re)
        });
        var arreglo = total.toFixed(2).split('.')
        console.log(arreglo)

        $('#total-price').html("" +
            "<span class='text-price align-top' id='int-total-price'>"+ arreglo[0] +"</span> " +
            "<span class='point-total-price'>.</span> " +
            "<span class='text-price-decimal' id='dec-total-price'>" + arreglo[1] + "</span>"
        );
    });

    // Boton de venta
    $(".product-img").click(function () {
    });
});