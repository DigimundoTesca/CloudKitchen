$(function() {
  function rel(){
    location.reload();          
  }
  setTimeout(rel, 15000);
});

$(function() {
  var objetos = $('tr');
  var lista_id = [];
  var lista_2 = [];
  var color = [];
  var a = 0;
  var b = 0;
  var count = -1; 
  objetos.each(function(index, element) {
    id_element = parseInt($(element).find('th.id_kitchen_table').text().trim())
    if (!isNaN(id_element)) {
      lista_id.push(id_element);
      lista_2.push(id_element);
    }
  });
  for (var j=0; j<lista_id.length; j++){
    a=j;
    b = j+1;
    if (lista_2[a] ===  lista_id[b]){
      lista_id[b] = " ";
    }
    if (lista_2[a]%2==0){
      color.push('#FFB74D');
    } else {
      color.push('#F4F4ED');
    }
  }
  objetos.each(function(index, element) {
    id_element = parseInt($(element).find('th.id_kitchen_table').text(lista_id[count]));
    id_element = parseInt($(element).css('background',color[count]));
    count++;
  });
});
