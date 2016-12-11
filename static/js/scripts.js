$(function() {

	/** 
		Resalta el nombre de los enlaces del navbar de acuerdo a la ubicacion en donde se encuentre
	*/
	let path = $(location).attr('pathname');
	if (path == '/sales/') {
		$('#link-sales').addClass('active')
	}
	else if (path == '/sales/new/') {
		$('#link-new-sale').addClass('active')

	}
	else if (path == '/supplies/') {
		$('#link-supplies').addClass('active')

	}
});