$(function() {
  /**
   * It records the records of "Ticket Details" and eliminates the id's of repeated tickets.
   * Color the "Ticket Details" records associated with the same ticket.
   */
  function format_tables() {
    const objects = $('tr');
    let list_id = [];
    let list_aux = [];
    let color = [];
    let a = 0;
    let b = 0;
    let count = -1;

    /**
     * Format lists so that they only contain integers and ignores the head.
     */
    objects.each(function(index, element) {
      let id_element = parseInt($(element).find('th.id_kitchen_table').text().trim());
      if (!isNaN(id_element)) {
        list_id.push(id_element);
        list_aux.push(id_element);
      }
    });

    /**
     * Associates a color with each item in the list.
     */
    for (let j=0; j<list_id.length; j++){
      a = j;
      b = j+1;
      if (list_aux[a] ===  list_id[b]){
        list_id[b] = " ";
      }
      if (list_aux[a] % 2 == 0){
        color.push('#FFB74D');
      } else {
        color.push('#F4F4ED');
      }
    }

    /**
     * Applies the new color to items in the list.
     */
    objects.each(function(index, element) {
      let id_element = parseInt($(element).find('th.id_kitchen_table').text(list_id[count]));
      id_element = parseInt($(element).css('background',color[count]));
      count++;
    });
  }

  /**
   * Reload the page every time
   */
  function rel(){
    location.reload();
  }

  format_tables();
  setTimeout(rel, 15000);
});