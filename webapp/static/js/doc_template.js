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
				if (heightCss > desiredHeight || widthCss > desiredWidth) {
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

$('#description').fitInText();
$('#shipper').fitInText();
$('#consignee').fitInText();
$('#notify').fitInText();
$('#place_of_receipt').fitInText();
$('#port_of_loading').fitInText();
$('#port_of_discharge').fitInText();
$('#place_of_delivery').fitInText();
$('#marks').fitInText();
$('#forwarding').fitInText();
$('#vessel').fitInText();
$('#booking_no').fitInText();
$('#freight_payable_at').fitInText();
$('#freight_term').fitInText();
$('#original_requirements').fitInText();
$('#place_of_issue').fitInText();
$('#etd_date_laden_onboard').fitInText();
$('#release_seaway_bill').fitInText();

var id = $("#doc_id").text()
var url = '../../detail/'+id+'/'
array = ['shipper','consignee', 'notify', 'place_of_receipt','port_of_loading','port_of_discharge',
		   'place_of_delivery', 'marks', 'description', 'forwarding', 'vessel', 'total_gross_weight','total_measurement','booking_no', 'freight_payable_at', 'freight_term', 'original_requirements', 'place_of_issue', 'etd_date_laden_onboard', 'release_seaway_bill']
array.forEach(key => {
	$("#" + key ).editable(
	{
			type: 'textarea',
			url: url,
			showbuttons:'bottom',
			pk: id,
			emptyclass:'emptyclass',
			emptytext:'',
			name: key,
			success: function (data) {
				console.log(data);
				if (data.status == true) {
					return data
				} else {
					return data.msg
				};
			},
		}
);
});
