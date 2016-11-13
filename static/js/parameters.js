$(document).ready(function() {
	var pathname = window.location.pathname;
	console.log('Path name:' + pathname);
	//window.alert(pathname)

	$( "#genRealTime" ).click(function() {
	  texto = $('select#realTimeStores').val().join()

	  alert(texto);  
	  $.post( "/", { selected_stores: texto, time: "2pm" });

      $('img').fadeOut('');
      //$('img').attr('src', $('img').attr('src') + '?' + Math.random());

      $('img').each(function(){
      		$(this).attr('src', $(this).attr('src') + '?' + Math.random());
    	});
      $('img').fadeIn(500);
	});
});