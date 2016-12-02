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
	 //  if (timer == 15) {
		// $.post("/heatmap")
		// $("#floor_1").attr('src', "static/images/floor_1.png");
		// $("#floor_2").attr("src", "static/images/floor_2.png");
	 //  }
	 //  if (timer == 0) {
	 //  	$("#floor_1").attr('src', "static/images/floor_1.png");
		// $("#floor_2").attr("src", "static/images/floor_2.png");
	 //    $('#tab2').find('img').each(function(){
		//   	$(this).fadeOut(150, function(){
		// 		$(this).attr('src', $(this).attr('src') + '?' + Math.random()).bind('onreadystatechange load', function(){
		// 			if (this.complete) $(this).fadeIn(800);
		// 		 });
		// 	});
		// });

	 //  }
	  //$('#clock').text(get_elapsed_time_string(elapsed_seconds));
	  $('#heatTimer').text(pretty_time_string(timer));
	}, 1000);

		setInterval(function() {
		if($("#heat_content").is(":visible")) {
			//$.post("/heatmap")
		
	
	 //    $('#tab2').find('img').each(function(){
		//   	$(this).fadeOut(150, function(){
		// 		$(this).attr('src', $(this).attr('src') + '?' + Math.random()).bind('onreadystatechange load', function(){
		// 			if (this.complete) $(this).fadeIn(800);
		// 		 });
		// 	});
		// });
	}
	// 		var my_heat = 1
	// 		$.post("/heatmap", { heatmap: my_heat}, function(response) {
 			
	// 		$("#floor_1").attr('src', "static/images/floor_1.png");
	// 		$("#floor_2").attr("src", "static/images/floor_2.png");

	// 	    $('#tab2').find('img').each(function(){
	// 		  	$(this).fadeOut(150, function(){
	//   					$(this).attr('src', $(this).attr('src') + '?' + Math.random()).bind('onreadystatechange load', function(){
	//      					if (this.complete) $(this).fadeIn(800);
	//  					 });
	// 					});
	// 		});

	// }, 'json');



	}, 45000);
});



	$( "#genHeatMap" ).click(function() {

		//$("#heatTimer").show();
		//$("#heatTimer").addClass("active");
		//$("#floor_1").attr('src', "static/images/floor_1_clean.png");
		//$("#floor_2").attr("src", "static/images/floor_2_clean.png");
		//$("#heat_content").show();

		var my_heat = 1
		$.post("/heatmap", { heatmap: my_heat}, function(response) {
 			$("#floor_1").attr('src', "static/images/floor_1.png");
			$("#floor_2").attr("src", "static/images/floor_2.png");
			

		    $('#tab2').find('img').each(function(){
			  	$(this).fadeOut(150, function(){
	  					$(this).attr('src', $(this).attr('src') + '?' + Math.random()).bind('onreadystatechange load', function(){
	     					if (this.complete) $(this).fadeIn(800);
	 					 });
						});
			});
			

	}, 'json');





	});

});