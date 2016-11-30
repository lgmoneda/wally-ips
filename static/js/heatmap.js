$(document).ready(function() {
	// var pathname = window.location.pathname;
	// console.log('Path name:' + pathname);
	//window.alert(pathname)


	///Conferir se a aba ativa é o heatmape então posso passar a atualizar
	///dentro de um intervalo
	// $('li[role="presentation"]').each(function( index ) {
	// 	if($(this).children().attr('href') == pathname) {
	// 		if($(this).text() == "Mapa de Calor") {
	// 						if(!$(this).hasclass("active")) {
	// 							$("#floor_1").attr('src', "static/images/floor_1_clean.jpg");
	// 					 		$("#floor_2").attr("src", "static/images/floor_1_clean.jpg");
	// 					}}
 //  		 	}
	// });


	$(document).ready(function() {
	var dt = 0
	setInterval(function() {
	  dt += 1;
	  timer = 30 - (dt % 30)	
	  //$('#clock').text(get_elapsed_time_string(elapsed_seconds));
	  $('#heatTimer').text(pretty_time_string(timer));
	}, 1000);
});



	$( "#genHeatMap" ).click(function() {

		$("#heatTimer").show();
		$("#heatTimer").addClass("active");
		$("#floor_1").attr('src', "static/images/floor_1_clean.png");
		$("#floor_2").attr("src", "static/images/floor_2_clean.png");
		$("#heat_content").show();

	});

});