$(document).ready(function () {
    /**LiveReloaded Plugin */
    // document.write('<script src="http://' + (location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1"></' + 'script>')

    $(".product-img").click(function () {
        let name = $(this).siblings('.product-name').text();
        let cost_base = parseFloat($(this).siblings('.content-price').children('.product-cost').text());
        let cost = cost_base;
        let id = $(this).parent().attr('id');
        let li_id = ('li-' + id).toString();
        let cant = $('ul#sales-list').find('#' + li_id + ' .cant-li').text();
        let total = 0;


        if ($('#' + li_id + '').length != 0) {
            cant++;
            let new_cost = cost * cant;
            console.log(new_cost)
            if (new_cost % 2 != 0) {
                new_cost = new_cost.toFixed(2);
            }
            else
                new_cost += '.00';

            $('ul#sales-list').find('#' + li_id + ' .cant-li').text(cant);
            $('ul#sales-list').find('#' + li_id + ' .total-li').text(new_cost);
        }
        else {
            if (cost % 2 != 0)
                cost = cost.toFixed(2);
            else
                cost += '.00';
            if (cost_base % 2 != 0)
                cost_base = cost_base.toFixed(2);
            else
                cost_base += '.00';

            $nuevo_li= $("" +
                "<li id='" + li_id + "' class='list-group-item'>" +
                "<span class='name-li text-uppercase'>" + name + "</span> " +
                "<span class='cost-base-li'>" + cost_base + "</span>"+
                "<span class='remove-icon-li'><i class='material-icons'>remove</i></span>" +
                "<span class='cant-li'>1</span>"+
                "<span class='add-icon-li'><i class='material-icons'>add</i></span>" +
                "<span class='font-weight-bold s-li'>$ </span>" +
                "<span class='total-li font-weight-bold'>" + cost + "</span> " +
                "</li>");
            $nuevo_li.appendTo('#sales-list').fadeTo('slow', 1);
        }

        // Modificacion del total general
        $('ul li').find('.total-li').each(function(){
            re = $(this).text()
            total += parseFloat(re)
        });
        var arreglo = total.toFixed(2).split('.')

        $('#total-price').html("" +
            "<span class='text-price align-top' id='int-total-price'>"+ arreglo[0] +"</span> " +
            "<span class='point-total-price'>.</span> " +
            "<span class='text-price-decimal' id='dec-total-price'>" + arreglo[1] + "</span>"
        );
    });

//Boton remover
    $(this).on('click', '.remove-icon-li', function () {
        console.log('btn remover');
    });

//Boton agregar
    $(this).on('click', '.add-icon-li', function () {
        console.log('Btn agregar');
    });

// Boton de venta
    $("#btn-order").click(function () {
        
    });


});
