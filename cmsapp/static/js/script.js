$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				link : $('#link-to-doc').val()
			},
			type : 'POST',
			url : '/dashboard/docs'
		})
		.done(function(data) {

			if (data.error) {
				console.log(data.error)
			}
			else {
				console.log("Noice")
			}

		});

		event.preventDefault();

	});

});