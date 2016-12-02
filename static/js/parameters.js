$(document).ready(function() {
	var pathname = window.location.pathname;
	console.log('Path name:' + pathname);

    $( function() {
    	$( "#start_date" ).datepicker();
    	$( "#end_date" ).datepicker();
  	} );
	//window.alert(pathname)

	$( "#genRealTime" ).click(function() {
	  texto = $('select#realTimeStores').val().join()
	  time = $('select#realTimePeriod').val()

	  //alert(texto);  
	  //var resp = $.post( "/", { selected_stores: texto, time: time});
	  //var obj = $.post( "/realtime", { selected_stores: texto, time: time});
	  //alert(obj)

	  $.post("/realtime", { selected_stores: texto, time: time}, function(response) {
	  		
	  		if(!response.valid) {
	  			alert("Consulta sem retorno!");
		      $('img').fadeOut(150);
			  $('#tab1').find('img').each(function(){
			  		$(this).attr('src', "static/images/wally.jpg");
				});
			  $('img').fadeIn(150);
	  		}
	  		else {
	  				//alert(response.descriptive_dict.max)
		  		   $("#realTimeGraph1").attr('src', response.graph1);
	  		 	   $("#realTimeGraph2").attr('src', response.graph2);
	  		 	   $("#max").text(response.descriptive_dict.max);
	  		 	   $("#max_time").text(response.descriptive_dict.max_time);
	  		 	   $("#unique_guests").text(response.descriptive_dict.unique_guests);

	  		 	   /*
	  			   $('img').fadeOut(800, function(){
      					$(this).attr('src', $(this).attr('src') + '?' + Math.random()).bind('onreadystatechange load', function(){
         					if (this.complete) $(this).fadeIn(800);
     					 });
   					});
	  			
	  			alert(response.graph2)
	  			$('img').fadeOut(1500);
	  			$("#realTimeGraph1").attr('src', response.graph1);
	  			$("#realTimeGraph2").attr('src', response.graph2);
	  			$('img').fadeIn(1000);
	  			
	  			$(this).attr('src', "static/images/wally.jpg");	
	  			*/

		      //$('img').fadeOut(1500);
			  $('#tab1').find('img').each(function(){
			  	$(this).fadeOut(150, function(){
      					$(this).attr('src', $(this).attr('src') + '?' + Math.random()).bind('onreadystatechange load', function(){
         					if (this.complete) $(this).fadeIn(800);
     					 });
   					});
			  		//$(this).fadeOut(200);
			  		//$(this).attr('src', $(this).attr('src') + '?' + Math.random());
					//$(this).fadeIn(1000);
				});
			  //$('img').fadeIn(1000);
			  
				
	  		}
    	// Do something with the request
		}, 'json');

	  /*
      $('img').fadeOut(1500);
      $('#tab1').find('img').each(function(){
      		$(this).attr('src', $(this).attr('src') + '?' + Math.random());
    	});
      $('img').fadeIn(1000);
		*/

      //$("#tab1").toggle().toggle();
      //$("#tab1_content").load(document.URL + " #tab1_content");
      //$("#tab1_content").html("/#tab1_content");


	});


	function getSelectedTabIndex() { 
    	return $("#TabList").tabs('option', 'selected');
	}

	// $( "#tab2" ).click(function() {
	// 	//$.post( "/historico", { selected_stores: texto, time: "2pm" });

	// });

	// $("#tab2").on("click", function() {
	// 	aqui = getSelectedTabIndex()
 // 		alert(aqui);
	// 	});



	// $( "#genHistTime" ).click(function() {
	//   texto = $('select#histTimeStores').val().join()
	//   time = $('select#histTime').text()
	//   alert("eu vou a luta"); 
	//   alert(texto);  
	//   alert(time);    
	//   $.post( "/historico", { selected_stores: texto, time: time });

 //     $('#tab2').find('img').fadeOut(1000);
 //      //$('img').attr('src', $('img').attr('src') + '?' + Math.random());

 //      $('#tab2').find('img').each(function(){
 //      		$(this).attr('src', $(this).attr('src') + '?' + Math.random());
 //    	});
 //      $('#tab2').find('img').fadeIn(1000);
	// });


	$( "#genHistTime" ).click(function() {
	  texto = $('select#histTimeStores').val().join()
	  start = $('#start_date').val()
	  end = $('#end_date').val()

	  $.post("/historical", { selected_stores: texto, start_date: start, end_date: end}, function(response) {
 		
  		if(!response.valid_hist) {
  			alert("Consulta sem retorno!");
	      $('img').fadeOut(150);
		  $('#tab3').find('img').each(function(){
		  		$(this).attr('src', "static/images/wally.jpg");
			});
		  $('img').fadeIn(150);
  		}
  		else {

	  		   $("#histTimeGraph1").attr('src', response.graph1_hist);
  		 	   $("#histTimeGraph2").attr('src', response.graph2_hist);
  		 	   $("#histTimeGraph3").attr('src', response.graph3_hist);
  		 	   $("#max_hist").text(response.descriptive_dict_hist.max);
  		 	   $("#max_time_hist").text(response.descriptive_dict_hist.max_time);
  		 	   $("#unique_guests_hist").text(response.descriptive_dict_hist.unique_guests);

  		 	   if(!$("#tab3_content").is(":visible")) 
  		 	   		$("#tab3_content").show()


		  $('#tab3').find('img').each(function(){
		  	$(this).fadeOut(150, function(){
  					$(this).attr('src', $(this).attr('src') + '?' + Math.random()).bind('onreadystatechange load', function(){
     					if (this.complete) $(this).fadeIn(800);
 					 });
					});
			});
  		}
	}, 'json');



	});

	$( "#genSimilarStores" ).click(function() {

		$.post("/similarstores", { selected_stores: texto, start_date: start, end_date: end}, function(response) {
	 	   if(!$("#similar_content").is(":visible")) 
	 	   		$("#similar_content").show()

	 	   	$("#stores").attr('src', response.heatmap_file);

		  $('#tab5').find('img').each(function(){
		  	$(this).fadeOut(150, function(){
  					$(this).attr('src', $(this).attr('src') + '?' + Math.random()).bind('onreadystatechange load', function(){
     					if (this.complete) $(this).fadeIn(800);
 					 });
					});
			});
		}, 'json');

		// $("#heatTimer").show();
		// $("#heatTimer").addClass("active");
		// $("#floor_1").attr('src', "static/images/floor_1_clean.png");
		// $("#floor_2").attr("src", "static/images/floor_2_clean.png");
		// $("#heat_content").show();

	});


		$( "#genRecommender" ).click(function() {
			texto = $('select#recommender').val().join()
			$.post("/recommender", { selected_stores: texto, start_date: start, end_date: end}, function(response) {
		 	   if(!$("#tab6_content").is(":visible")) 
		 	   		$("#tab6_content").show()

			$('#tab6').find('img').each(function(){
		  		$(this).fadeOut(150) 
		  		$(this).remove()
			});

			var i;
			for (i = 0; i < response.stores.length; ++i) {
			    var img = $('<img id="dynamic" width="20px">'); //Equivalent: $(document.createElement('img'))
				img.attr('src', response.stores[i]);
				img.attr('width', "70px");
				img.appendTo('#storesdiv');
				$("#storesdiv").append("   ");
			}

	});
		});

});