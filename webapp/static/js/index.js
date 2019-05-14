$(document).ready(function (table) {
	get_last_doc();
	document.getElementById("bl_submit").onclick = function () {
		// var cur_ID = get_current_ID().split(' ').join('');
		// console.log('preview doc ID: ' + cur_ID);
		toastr.success("Submit successfully", 'SUCCESS');
		// var strWindowFeatures = "location=yes,height=800,width=900,scrollbars=yes,status=yes";
		// window.open("/drafting/preview/" + cur_ID + "/", "_blank", strWindowFeatures);
	};

	$('#file-upload').on('change', function () {
		getSpinnerDimmed();
		var formData = new FormData();
		formData.append('file', $('#file-upload')[0].files[0]);
		//formData.append("CustomField", "This is some extra data");
		console.log("% UPLOADING %");
		uploadData(formData);
	});

	function removeSpinnerDimmed() {
		console.log('$ Removing spin loader $');
		$('.container-fluid').unwrap();
		$('.lds-spinner').remove();
	};

	function getSpinnerDimmed() {
		// dimmed blanket
		$('.container-fluid').wrap('<div class="dimmed" style="pointer-events: none;"></div>');
		// loader
		$('.container-fluid').append('<div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
		$('.lds-spinner').css('top', ($(window).height() - $(".lds-spinner").height()) / 2);
		$('.lds-spinner').css('left', ($(window).width() - $(".lds-spinner").width()) /2);
	};

	function get_last_doc() {
		console.log('** Getting Docs List through drafting/list **');
		$.ajax({
			url: '/extractor/list/',
			type: 'get',
			dataType: 'json',
			success: function (data) {
				console.log('## get Doc SUCCESSED ##');
				console.log(data.doc);
				var doc = data.doc;
				$('#left_frame').attr('src', '/extractor/pdf/'+ doc.id);
				$('#right_frame').attr('src', '/extractor/preview/'+ doc.id);				
				document.getElementById("annotate").onclick = function () {
					console.log('TEMPLATE:' + doc.template);
					window.location.href = "/annotation/process/" + doc.template;
				};
			},

			error: function (data) {
				console.log('## get Doc ERROR ##');
				console.log(data);
			},
			complete: function () {
				console.log('## get Doc call DONE ##');
			},
		});
	};


	function uploadData(formdata) {
		console.log("$ File UPLOADING $");
		$.ajax({
			url: '/upload/',
			type: 'POST',
			data: formdata,
			contentType: false,
			processData: false,
			success: function (data) {
				console.log('## UPLOAD SUCCESS ##');
				console.log(data);
				// forward uploaded filename to Extracting
				detailExtract(data);
			},
			error: function (data) {
				console.log('## UPLOAD FALSE ##');
				console.log(data);
				// pop up message and unwrap dimmed blanket
				if (data.hasOwnProperty('responseJSON')) {
					toastr.warning(data.responseJSON.error + '. Please upload another SI file.', 'ERROR');
				};
				removeSpinnerDimmed();
			},
		});
	};


	function detailExtract(data) {
		console.log('$ forwarding to Extracting $');
		$.ajax({
			url: '/extractor/process/',
			type: 'POST',
			data: {'filename': data.filename},
			dataType: 'json',
			success: function (data) {
				console.log('$ Extracting SUCCESS $');
				console.log(data);
				if (data['is_verified'] == false){
					toastr.error('We could not extract the containers detail in this SI correctly, please send to manual checking');
					$('#left_frame').attr('src', '/extractor/pdf/'+ data.doc.id);
					$('#right_frame').attr('src', '/extractor/preview/'+ data.doc.id);
					get_last_doc();
				} else if (data.hasOwnProperty('temp_num')) {
					// NEED to ANNOTATE

					toastr.options = {  
						"newestOnTop": true,
						"progressBar": true,
						"positionClass": "toast-top-center",
						"preventDuplicates": false,
						"onclick": null,
						"showDuration": "10000",
						"hideDuration": "10000",
						"timeOut": "10000",
						"extendedTimeOut": "10000",
						"showEasing": "swing",
						"hideEasing": "linear",
						"showMethod": "fadeIn",
						"hideMethod": "fadeOut",
					};

					toastr.warning(
						'This SI template is a new type. Please click the button to annotate  or just ignore and upload another SI. \
						<button id="toAnnotate" class="btn-info";> ANNOTATE </button>'
					);
					$('button#toAnnotate').click(function(){
						window.location.href = "/annotation/process/" + data.temp_num;
					})
				} else if (data.hasOwnProperty('doc')) {
					// SUCCESS
					$('#left_frame').attr('src', '/extractor/pdf/'+ data.doc.id);
					$('#right_frame').attr('src', '/extractor/preview/'+ data.doc.id);
					get_last_doc();
					toastr.success('SI has been successfully processed', 'SUCCESS');
					get_last_doc();
				}
			},

			error: function (data) {
				console.log('$ Extracting FALSE $');
				console.log(data);
			},

			complete: function () {
				console.log('$ Extracting COMPLETE $');
				removeSpinnerDimmed();
			},
		});
	};
})
