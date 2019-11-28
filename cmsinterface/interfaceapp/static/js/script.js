$(document).ready(function() {
	var csrftoken = Cookies.get("csrf_access_token");

	$('#link-form').on('submit', function(event) {

		$.ajax({
			data : {
				link : $('#link-to-doc').val()
			},
			type : 'POST',
			url : '/dashboard/docs/find',
			headers:{"X-CSRF-TOKEN": csrftoken},
			beforeSend: function() {
				$("#error-link").text("loading...").show();
				$("#success-link").hide();
				$("#success-url").hide();
			},
			error: function() {
				location.reload();
			},
			timeout: 4000
		})
		.done(function(data) {

			if (data.error) {
				$("#error-link").text(data.error).show();
				$("#success-link").hide();
				$("#success-url").hide();
			}
			else {
				$("#success-link").text(data.title).show();
				$("#success-url").text(data.url).show();
				$("#error-link").hide();
			}

		});

		event.preventDefault();

	});

});


$(document).ready(function() {
	var csrftoken = Cookies.get("csrf_access_token");

	$('#url-form').on('submit', function(event) {

		$.ajax({
			data : {
				url : $('#url-to-doc').val()
			},
			type : 'POST',
			url : '/dashboard/docs/delete',
			headers:{"X-CSRF-TOKEN": csrftoken},
			beforeSend: function() {
				$("#error-aurl").text("loading...").show();
				$("#success-aurl").hide();
			},
			error: function() {
				location.reload();
			},
			timeout: 4000
		})
		.done(function(data) {

			if (data.error) {
				$("#error-aurl").text(data.error).show();
				$("#success-aurl").hide();
			}
			else {
				$("#success-aurl").text(data.title).show();
				$("#error-aurl").hide();
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
			headers:{"X-CSRF-TOKEN": csrftoken},
			error: function() {
				location.reload();
			},
			timeout: 4000
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