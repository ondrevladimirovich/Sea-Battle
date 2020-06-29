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
	
	$('.enemy_cell').on('click', function(e) {
		e.preventDefault();

		let position = $(this).data('cell');
		let url = $(location).attr('href');
		let segments = url.split( '/' );
		let game_id = segments[4];

		$.ajax({
			type: "POST",
	    	url: "/fire/",
	    	data: {
				game_id: game_id, 
				game_type: 1, //TODO: singleplayer game
				position: position
			},
	    	success: function(response) {
				//redraw changed cells of field
				$.each(response, function(i, cell) {
					$("#field2 td[data-cell='" + i + "']").text(cell);
					if(cell != ' ') {
						$("#field2 td[data-cell='" + i + "']").removeClass("enemy_cell");
						$("#field2 td[data-cell='" + i + "']").unbind('click');
					}
				});
	    	},
	    	error: function() {
	        
	    	}
		});
	});
});