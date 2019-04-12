$(document).ready(function () {
	$('#main-content').unwrap();
	sizingWrapper();
	
	$(window).resize(function(){
		sizingWrapper()
	});
	
});

function sizingWrapper() {	
	var screen_w = window.screen.width;  
	$('#canWrap').css('width', screen_w * 0.75);
	$('#rightBar').css('width', screen_w * 0.25);
}
