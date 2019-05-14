$(document).ready(function () {
	// preventing page from redirecting
	$("html").on("dragover", function (e) {
		e.preventDefault();
		e.stopPropagation();
		$("h1.DragDrop").text("Drag here");
		console.log('Dragging');
	});

	$("html").on("drop", function (e) {
		e.preventDefault();
		e.stopPropagation();
	});

	// Drag enter
	$('.upload-area').on('dragenter', function (e) {
		e.stopPropagation();
		e.preventDefault();
		$("h1.DragDrop").text("Drop");
		console.log('Drag entering');
	});

	// Drag over
	$('.upload-area').on('dragover', function (e) {
		e.stopPropagation();
		e.preventDefault();
		$("h1.DragDrop").text("Drop");
		console.log('on Drag zone');
	});

	// Drop
	$('.upload-area').on('drop', function (e) {
		e.stopPropagation();
		e.preventDefault();
		
		console.log('File uploading via Drag and Drop');
		processUploading();
		
		var file = e.originalEvent.dataTransfer.files;
		var fd = new FormData();
		fd.append('file', file[0]);

		// Upload file via AJAX request
		uploadData(fd)
});

	// Open file selector on div click
	$("#uploadfile").click(function () {
		$("#file").click();
	});

	// file selected
	$("#file").change(function () {
		console.log('File uploading via Browse clicking');
		processUploading();

		var files = $('#file')[0].files[0];
		var fd = new FormData();
		fd.append('file', files);		

		// Upload file via AJAX request
		uploadData(fd)
	});
});

function processUploading() {
	console.log('$ GETTING Spin Dimmed Loader $');
	$("h1.DragDrop").text("Processing");
	$('.container').css('pointer-events', 'none');
	$('#uploadfile').append('<div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
	$('.lds-spinner').css('margin', '40px 0px 0px -30px');
}

function uploadData(formdata) {
	console.log('$ File UPLOADING $');
	$.ajax({
		url: '/upload/',
		type: 'POST',
		data: formdata,
		contentType: false,
		processData: false,
		success: function (data) {
			// console.clear();
			console.log('$ UPLOAD SUCCESS $');
			console.log(data);
			// forward uploaded filename to Extracting
			detailExtract(data);
		},

		error: function (data) {
			console.log("$ UPLOAD FALSE $");
			console.log(data);
			// pop up message
			if (data.hasOwnProperty('responseJSON')) {
				toastr.warning(data.responseJSON.error + '. Please upload another SI file.', 'ERROR');
			}

			$("h1.DragDrop").text('')
			$("h1.DragDrop").append("Drag and Drop file here<br>Or<br>Click to select file");

			console.log('$ Removing spin loader $');
			$('.container').css('pointer-events', '');
			$('.container').css('cursor', 'progress');
			$('.lds-spinner').remove();
		},
	});
}


function detailExtract(data) {
	console.log('$ forwarding to Extracting $');
	$.ajax({
		url: 'extractor/process/',
		type: 'POST',
		data: {'filename': data.filename},
		dataType: 'json',
		success: function (data) {
			console.log('$ Extracting SUCCESS $');
			console.log(data);
			if (data.hasOwnProperty('temp_num')) {
				// NEED to ANNOTATE
				window.location.href = "/annotation/process/" + data.temp_num;
			} else if (data.hasOwnProperty('doc')) {
				// SUCCESS
				window.location.href = "/extractor/main_panel/";
			}
		},

		error: function (data) {
			console.log('$ Extracting FALSE $');
			console.log(data);
		},

		complete: function () {
			console.log('$ Extracting COMPLETE $');
			console.log('$ Removing spin loader $');
			$('.lds-spinner').remove();
		},
	});
}
