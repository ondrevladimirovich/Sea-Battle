$(document).ready(function() {
    
    $('#start_new_game').on('click', function(e){
    	e.preventDefault();

	    $.ajax({
	    	url: "/create_new_game/",
	    	data: {},
	    	success: function(response) {
	        	window.location = "/game/" + response;
	    	},
	    	error: function() {
	        
	    	}
		});
    });
});