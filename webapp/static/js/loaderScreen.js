function removeSpinnerDimmed() {
	console.log('$ REMOVING Spin Dimmed Loader $');
	$('.container-fluid').unwrap();
	$('.lds-spinner').remove();
}

function getSpinnerDimmed() {
    console.log('$ GETTING Spin Dimmed Loader $');
    // dimmed blanket
	$('.container-fluid').wrap('<div class="dimmed" style="pointer-events: none;"></div>');
	// loader
	$('.container-fluid').append('<div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
	$('.lds-spinner').css('top', ($(window).height() - $(".lds-spinner").height()) / 2);
	$('.lds-spinner').css('left', ($(window).width() - $(".lds-spinner").width()) /2);
}
