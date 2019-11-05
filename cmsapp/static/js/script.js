$(document).ready(function() {
	var csrftoken = Cookies.get("csrf_access_token");

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				link : $('#link-to-doc').val()
			},
			type : 'POST',
			url : '/dashboard/docs',
			headers:{"X-CSRF-TOKEN":csrftoken}
		})
		.done(function(data) {

			if (data.error) {
				$("#error").text(data.error).show();
				$("#success").hide();
			}
			else {
				$("#success").text(data.title).show();
				$("#error").hide();
			}

		});

		event.preventDefault();

	});

});