$(document).ready(function (table) {
	get_list();
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

	function up_space(str) {
		return replaceAll(str.toUpperCase(), "_", " ")
	};

	function replaceAll(str, find, replace) {
		return str.replace(new RegExp(find, 'g'), replace);
	};

	function get_current_ID() {
		var cur_ID = $('#detailTable > tbody > tr:first-child > td:last-child').text();
		console.log('** Get current ID **: ' + cur_ID);
		return cur_ID;
	};

	function get_last_ID() {
		var last_ID = $('#listTable > tbody > tr:first-child > td:first-child').text();
		console.log('** Get lastID ** : ' + last_ID);
		return last_ID;
	};

	function clear_detailTable() {
		console.log('** Clearing detailTable **');
		$('#detailTable > tbody').children().remove();
	};

	function clear_listTable() {
		console.log('** Clearing listTable **');
		$('#listTable > tbody').children().remove();
	};

	function get_list() {
		console.log('** Getting Docs List through drafting/list **');
		$.ajax({
			url: '/extractor/list/',
			type: 'get',
			dataType: 'json',
			success: function (data) {
				console.log('## get list SUCCESSED ##');
				console.log(data.docs);
				if (data.docs.length > 0){
					var doc = data.docs[0]
					$('#left_frame').attr('src', '/extractor/pdf/'+ doc.id)
					$('#right_frame').attr('src', '/extractor/preview/'+ doc.id)
				}
				// let rows = '';
				// data.docs.forEach(doc => {
				// 	rows += '\
				//         <tr>\
				//             <td>' + doc.id + '</td>\
				//             <td><a data-type="textarea" class="detail-link"\
				//             id="' + doc.id + '" \
				//             href="#">' + doc.name + '</a></td>\
				//         </tr>';
				// });

				// console.log('## Add to listTable ##');
				// $('#listTable > tbody').append(rows);
				
				// var last_ID = get_last_ID();
				// clear_detailTable();
				// get_detail(last_ID);

				// console.log('## Add hyper-link for listTable items ##');
				// $('.detail-link').each((i, elm) => {
				// 	$(elm).on("click", (el) => {
				// 		console.log('**You\'ve clicked on Doc Name** with ID: ' + elm.id);
				// 		clear_detailTable();
				// 		get_detail(elm.id);
				// 	})
				// });
			},

			error: function (data) {
				console.log('## get list ERROR ##');
				console.log(data);
			},
			complete: function () {
				console.log('## get list call DONE ##');
			},
		});
	};

	function get_detail(DocId) {
		console.log('** List giving ID:' + DocId + ' **');
		$.ajax({
			url: '../detail/' + DocId + '/',
			type: 'get',
			dataType: 'json',
			success: function (data) {
				console.log('** get detail SUCCESSED **');
				let rows = '';
				for (var key in data.doc) {
					let doc = data.doc;
					if (key === 'id') {
						rows += '\
						<tr>\
							<td width="20%"><b>' + up_space(key) + '</b></td>\
							<td id="' + key + '">\
							' + doc[key] + '</td>\
						</tr>';
					} else if (key === 'name') {
						rows += '\
						<tr>\
							<td width="20%"><b> FILE ' + up_space(key) + '</b></td>\
							<td><a id="' + key + '"\
							style="cursor: pointer;"\
							>' + doc[key] + '</a></td>\
						</tr>';
					} else if (doc.hasOwnProperty(key)) {
						rows += '\
						<tr>\
							<td width="20%"><b>' + up_space(key) + '</b></td>\
							<td><a id="' + key + '" data-type="textarea" \
							>' + doc[key] + '</a>\
						</td></tr>';
					};
				};

				console.log('** Add to detailTable **');
				$('#detailTable > tbody').append(rows);

				console.log('** Set to EditAble **');
				// toggle `popup` / `inline` mode
				$.fn.editable.defaults.mode = 'inline';
				for (var key in data.doc) {
					let doc = data.doc;
					if (key === 'id') { // Pass
					} else if (key === 'name') {
						document.getElementById("name").onclick = function () {
							var strWindowFeatures = "location=yes,height=800,width=900,scrollbars=yes,status=yes";
							window.open("/media/" + $("#name").text() + "/", "_blank", strWindowFeatures);
						};
					} else if (doc.hasOwnProperty(key)) {
						$("#" + key).editable({
							type: 'textarea',
							url: '../detail/' + doc.id + '/',
							pk: doc.id,
							name: key,
							success: function (data) {
								console.log(data);
								if (data.status == true) {
									return data
								} else {
									return data.msg
								};
								// msg will be shown in editable form
							},
						});
					};
				};
			},

			error: function (data) {
				console.log('** get detail ERROR **');
				console.log(data);
			},
			complete: function () {
				console.log('** get detail DONE **');
			},
		});
	};

	function uploadData(formdata) {
		console.log("$ File UPLOADING $");
		$.ajax({
			url: '../upload/',
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
			url: '../process/',
			type: 'POST',
			data: {'filename': data.filename},
			dataType: 'json',
			success: function (data) {
				console.log('$ Extracting SUCCESS $');
				console.log(data);
				if (data.hasOwnProperty('temp_num')) {
					// NEED to ANNOTATE
					window.location.href = "/drafting/annotation/" + data.temp_num;
				} else if (data.hasOwnProperty('doc')) {
					// SUCCESS
					$('#left_frame').attr('src', '/drafting/pdf/'+ data.doc.id)
					$('#right_frame').attr('src', '/drafting/preview/'+ data.doc.id)
					toastr.success('SI has been successfully processed', 'SUCCESS');
					clear_listTable();
					get_list();
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
