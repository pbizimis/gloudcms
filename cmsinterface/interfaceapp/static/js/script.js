$(document).ready(function() {
	var csrftoken = Cookies.get("csrf_access_token");

	$('#link-form').on('submit', function(event) {

		$.ajax({
			data : {
				link : $('#link-to-doc').val()
			},
			type : 'POST',
			url : '/dashboard/docs/find',
			headers:{"X-CSRF-TOKEN": csrftoken}
		})
		.done(function(data) {

			if (data.error) {
				$("#error-link").text(data.error).show();
				$("#success-link").hide();
			}
			else {
				$("#success-link").text(data.title).show();
				$("#success-url").text(data.url).show();
				$("#success-apiid").text(data.apiid).show();
				$("#error-link").hide();
			}

		});

		event.preventDefault();

	});

});



$(document).ready(function() {
	var csrftoken = Cookies.get("csrf_access_token");

	$('#create-doc').on('submit', function(event) {

		$.ajax({
			type : 'POST',
			url : '/dashboard/docs/create',
			headers:{"X-CSRF-TOKEN": csrftoken}
		})
		.done(function(data) {

			if (data.error) {
				$("#error-create").text(data.error).show();
				$("#success-create").hide();
			}
			else {
				$("#success-create").text(data.title).show();
				$("#error-create").hide();
			}

		});

		event.preventDefault();

	});

});