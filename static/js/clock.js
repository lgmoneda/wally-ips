  function pretty_time_string(num) {
  	if (num < 10)
  		return "0" + num
  	else
  		return num
    return ( num < 10 ? "0" : "" ) + num;
  }

function get_elapsed_time_string(total_seconds) {
  function pretty_time_string(num) {
  	if (num < 10)
  		return "0" + num
  	else
  		return num
    return ( num < 10 ? "0" : "" ) + num;
  }

  var hours = Math.floor(total_seconds / 3600);
  total_seconds = total_seconds % 3600;

  var minutes = Math.floor(total_seconds / 60);
  total_seconds = total_seconds % 60;

  var seconds = Math.floor(total_seconds);

  // Pad the minutes and seconds with leading zeros, if required
  hours = pretty_time_string(hours);
  minutes = pretty_time_string(minutes);
  seconds = pretty_time_string(seconds);

  // Compose the string for display
  if (seconds < 10) {
  	var currentTimeString = hours + ":" + minutes + ":0" + seconds;
  }
  else {
  	var currentTimeString = hours + ":" + minutes + ":" + seconds;
  }
  

  return currentTimeString;
}

$(document).ready(function() {
	var dt = new Date(Date.now());
	setInterval(function() {
	  dt = new Date(Date.now());	
	  //$('#clock').text(get_elapsed_time_string(elapsed_seconds));
	  $('#clock').text(dt.getDate() + "/" + (dt.getMonth()+1) + "/" +  dt.getFullYear() + " - " + dt.getHours() + ":" + pretty_time_string(dt.getMinutes()) + ":" + pretty_time_string(dt.getSeconds()));
	}, 1000);
});