$(function() {

	/**  Resalta el nombre de los enlaces del navbar de acuerdo a la ubicacion en donde se encuentre */
	let path = $(location).attr('pathname');
	if (path == '/sales/') {
		$('#link-sales').addClass('active');
	}
	else if (path == '/sales/new/') {
		$('#link-new-sale').addClass('active');
	}
	else if (path == '/supplies/' || path == '/supplies/new/') {
		$('#link-supplies').addClass('active');
	}
	else if (path == '/cartridges/' || path == '/cartridges/new/') {
		$('#link-cartridges').addClass('active');
	}
	else if (path == '/customers/register/list/') {
		$('#link-customers').addClass('active');
	}
});
