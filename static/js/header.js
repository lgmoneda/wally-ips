$(document).ready(function() {
	var pathname = window.location.pathname;
	console.log('Path name:' + pathname);
	//window.alert(pathname)

	$('li[role="presentation"]').each(function( index ) {
		if($(this).children().attr('href') == pathname) {
			$(this).addClass("active")
		}
	});

});