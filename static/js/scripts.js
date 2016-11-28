$(document).ready(function(){
  $(".product-img").click(function() {
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
      "<span class='text-price align-top' id='int-total-price'>" + arreglo[0] +"</span>" +
      "<span class='point-total-price'>.</span>" +
      "<span class='text-price-decimal' id='dec-total-price'>" + arreglo[1] + "</span>"
      );
  });

  //Boton remover unidad
  $(this).on('click', '.remove-icon-li', function () {
    console.log('btn remover');
  });

  //Boton agregar unidad
  $(this).on('click', '.add-icon-li', function () {
    console.log('Btn agregar');
  });

  // Boton para realizar venta
  $("#btn-order").click(function() {
    $('#sales-list-modal').empty();
    $nuevo_li= $("" +
      "<li>" +
      "<span class='name-li-title-modal'>Nombre</span> " +
      "<span class='cost-li-title-modal'>Cost</span>"+
      "<span class='cant-li-title-modal'>Cant</span>"+
      "<span class='total-li-title-modal'>Total</span> " +
      "</li>");

    $nuevo_li.appendTo('#sales-list-modal').fadeTo('slow', 1);

    $('#sales-list li').each(function() {
      let name = $(this).find('.name-li').text();
      let cost_base = $(this).find('.cost-base-li').text();
      let cant = $(this).find('.cant-li').text();
      let total = $(this).find('.total-li').text();
      let id = $(this).attr('id');
      let li_id = (id + '-modal').toString();

      // Acorta el nombre
      name = name.split(' ');
      $.each(name, function(index, item) {
        name[index] = item.substring(0,3);

      });
      name = name.toString().replace(',', ' ').replace(',', ' ');


      $nuevo_li= $("" +
        "<li id='" + li_id + "' class='list-group-item'>" +
        "<span class='name-li-modal text-uppercase'>" + name + "</span> " +
        "<span class='cost-li-modal'>" + '$ ' + cost_base + "</span>"+
        "<span class='cant-li-modal'>" + cant + "</span>"+
        "<span class='total-li-modal'>" + '$ ' + total + "</span> " +
        "</li>");

      $nuevo_li.appendTo('#sales-list-modal').fadeTo('slow', 1);
    });

    let total_ticket = $('#total-price').text();

    $nuevo_li= $("" +
      "<li class='total-ticket-container'>" +
      "<span id='total-ticket'>" + "$ " + total_ticket + "</span> " +
      "</li>");

    $nuevo_li.appendTo('#sales-list-modal').fadeTo('slow', 1);
  });

  $(this).on('click', '.btn-printer', function () {
    //  ---------   | ---------  | ---------------------- | -----------
    //  @mode       | [string]   | (iframe),popup         | printable window is either iframe or browser popup
    //  @popHt      | [number]   | (500)                  | popup window height
    //  @popWd      | [number]   | (400)                  | popup window width
    //  @popX       | [number]   | (500)                  | popup window screen X position
    //  @popY       | [number]   | (500)                  | popup window screen Y position
    //  @popTitle   | [string]   | ('')                   | popup window title element
    //  @popClose   | [boolean]  | (false),true           | popup window close after printing
    //  @extraCss   | [string]   | ('')                   | comma separated list of extra css to include
    //  @retainAttr | [string[]] | ["id","class","style"] | string array of attributes to retain for the containment area. (ie: id, style, class)
    //  @standard   | [string]   | strict, loose, (html5) | Only for popup. For html 4.01, strict or loose document standard, or html 5 standard
    //  @extraHead  | [string]   | ('')                   | comma separated list of extra elements to be appended to the head tag

    let options = { mode: 'iframe', popClose: true,};
    $("#printer").printArea(options);
  });
});