toastr.options = {
	"closeButton": true,
	"debug": false,
	"newestOnTop": true,
	"progressBar": false,
	"positionClass": "toast-top-center",
	"preventDuplicates": false,
	"onclick": null,
	"showDuration": "700",
	"hideDuration": "1000",
	"timeOut": "5000",
	"extendedTimeOut": "1000",
	"showEasing": "swing",
	"hideEasing": "linear",
	"showMethod": "fadeIn",
	"hideMethod": "fadeOut",
}

$.fn.fitInText = function () {
	this.each(function () {
		let textbox = $(this);
		let textboxNode = this;
		let mutationCallback = function (mutationsList, observer) {
			if (observer) {observer.disconnect()};
			textbox.css('font-size', 1);
			let desiredHeight = textbox.css('height');
			let desiredWidth = textbox.css('width');

			for (i = 5; i < 12; i++) {
				textbox.css('font-size', i);
				let heightCss = textbox.css('height');
				let widthCss = textbox.css('width');
				if (parseFloat(heightCss) > parseFloat(desiredHeight) || parseFloat(widthCss) > parseFloat(desiredWidth)) {
					textbox.css('font-size', i - 1);
					break;
				}
			};
			var config = {
				attributes: true,
				childList: true,
				subtree: true,
				characterData: true
			};
			let newobserver = new MutationObserver(mutationCallback);
			newobserver.observe(textboxNode, config);
		};
		mutationCallback();
	});
}

// $('#bkg_no').fitInText();
// $('#bl_no').fitInText();
$('#shipper').fitInText();
$('#consignee').fitInText();
$('#notify').fitInText();
$('#also_notify').fitInText();

$('#place_of_receipt').fitInText();
$('#port_of_loading').fitInText();
$('#port_of_discharge').fitInText();
$('#place_of_delivery').fitInText();
$('#vessel').fitInText();
$('#forwarding').fitInText();

// $('#description_of_goods').fitInText();
// $('#marks').fitInText();

$('#freight_payable_at').fitInText();
$('#freight_term').fitInText();
$('#original_requirements').fitInText();
$('#place_of_issue').fitInText();
$('#etd_date_laden_onboard').fitInText();
$('#release_seaway_bill').fitInText();


var id = $("#doc_id").text()
var url = '../../detail/' + id + '/'
array = [
	'bkg_no', 'bl_no', 'shipper', 'consignee', 'notify', 'place_of_receipt',
	'port_of_loading', 'port_of_discharge', 'place_of_delivery', 'marks',
	'description', 'forwarding', 'vessel', 'total_gross_weight', 'total_measurement',
	'freight_payable_at', 'freight_term', 'original_requirements', 'place_of_issue',
	'etd_date_laden_onboard', 'release_seaway_bill'
]

// array.forEach(key => {
// 	$("#" + key).editable({
// 		type: 'textarea',
// 		url: url,
// 		showbuttons: 'bottom',
// 		pk: id,
// 		emptyclass: 'emptyclass',
// 		emptytext: '',
// 		name: key,
// 		success: function (data) {
// 			console.log(data);
// 			if (data.status == true) {
// 				return data
// 			} else {
// 				return data.msg
// 			};
// 		},
// 	});
// });

var descrip_1 = $('#cont_details_description_1');
var descrip_2 = $('#cont_details_description_2');
var conts_details = $('.containers_detail');
var conts_description = $('.description');
var payment_remarks = $('.payment_remarks');


console.log(conts_details.height());
console.log(conts_description.height());
console.log(descrip_1.height());

if (conts_details.height() + conts_description.height() + 25 > descrip_1.height()) {
  console.log('OVERFLOW ::::: conts_description');
  // descrip_2.children().remove();
  // descrip_2.append($('.description').nextAll().addBack());
  $('.description').nextAll().addBack().insertBefore(descrip_2.children());
} else if (conts_details.height() + conts_description.height() + payment_remarks.height() + 25 > descrip_1.height()) {
  console.log('OVERFLOW ::::: payment_remarks');
  // descrip_2.children().remove();
  // descrip_2.append($('.payment_remarks').nextAll().addBack());
  $('.payment_remarks').nextAll().addBack().insertBefore(descrip_2.children());
} else {
  $('.pages_sign').remove();
}
