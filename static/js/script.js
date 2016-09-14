$(document).ready(function() {

	var $feedsElem = $('#feedsdiv');
	var $pagenoElem = $('#pageno');
	var $prevElem = $(':button.prev');
	var $nextElem = $(':button.next');
	
	$nextElem.on("click", function() {		// AJAX call to get the next page's elements

		var curr_page = $pagenoElem.text();

		$feedsElem.empty();
		$pagenoElem.empty();
		$prevElem.empty();
		$nextElem.empty();

		$.ajax({
			url: '/next',
			datatype: 'json',
			data: {page: curr_page},
			complete: function(jqXHR, textStatus) {
				var response = jQuery.parseJSON(jqXHR.responseText);
				var is_this_last = response.pop();
				var page_no = response.pop();
				for (var i=0, len=response.length; i<len; ++i) {
					var feed = response[i];
					$feedsElem.append('<div class="row">' + 
						'<h3 class="text-center"><b>' + feed.title + '</b></h3>' + 
						'<div class="image"><img src="' + feed.imageurl + '" alt="No picture available"></div>' +
						'<div class="description">' + feed.description + '...<a href="' + feed.url + '">See more</a></div>' + '</div>');
				}
				$pagenoElem.text(page_no);
				if (page_no != 1) {
					$prevElem.text('← PREVIOUS');
					$prevElem.removeAttr('style');
				}
				else {
					$prevElem.attr("style", "visibility: hidden");
				}
				if (is_this_last == false) {
					$nextElem.text('Next →');
					$nextElem.removeAttr('style');
				}
				else {
					$nextElem.attr("style", "visibility: hidden");
				}

			}
		});
	});

	$prevElem.on("click", function() {		// AJAX call to get the previous page's elements

		var curr_page = $pagenoElem.text();
		
		$feedsElem.empty();
		$pagenoElem.empty();
		$prevElem.empty();
		$nextElem.empty();

		$.ajax({
			url: '/previous',
			datatype: 'json',
			data: {page: curr_page},
			complete: function(jqXHR, textStatus) {
				var response = jQuery.parseJSON(jqXHR.responseText);
				var is_this_last = response.pop();
				var page_no = response.pop();
				for (var i=0, len=response.length; i<len; ++i) {
					var feed = response[i];
					$feedsElem.append('<div class="row">' + 
						'<h3 class="text-center"><b>' + feed.title + '</b></h3>' + 
						'<div class="image"><img src="' + feed.imageurl + '" alt="No picture available"></div>' +
						'<div class="description">' + feed.description + '...<a href="' + feed.url + '">See more</a></div>' + '</div>');
				}
				$pagenoElem.text(page_no);
				if (page_no != 1) {
					$prevElem.text('← Previous');
					$prevElem.removeAttr('style');
				}
				else {
					$prevElem.attr("style", "visibility: hidden");
				}
				if (is_this_last == false) {
					$nextElem.text('Next →');
					$nextElem.removeAttr('style');
				}
				else {
					$nextElem.attr("style", "visibility: hidden");
				}
			}
		});
	});

});

var refresh = function() {
	document.location.reload(true);
}

var periodicRefresh = setInterval(refresh, 600000);

window.addEventListener("offline", function(e) {
    clearInterval(periodicRefresh);
}, false);

window.addEventListener("online", function(e) {
    setInterval(periodicRefresh, 600000);
}, false);