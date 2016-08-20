$(document).ready(function() {

	var $feedsElem = $('div.feedsdiv');
	var $pagenoElem = $('p.pageno');
	var $prevElem = $(':button.prev');
	var $nextElem = $(':button.next');

	$nextElem.on("click", function() {		// AJAX call to get the next page's elements

		$feedsElem.empty();
		$pagenoElem.empty();
		$prevElem.empty();
		$nextElem.empty();

		$.ajax({
			url: '/next',
			datatype: 'json',
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
				$pagenoElem.text('Page ' + page_no);
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

		$feedsElem.empty();
		$pagenoElem.empty();
		$prevElem.empty();
		$nextElem.empty();

		$.ajax({
			url: '/previous',
			datatype: 'json',
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
				$pagenoElem.text('Page ' + page_no);
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

	if (!navigator.onLine) {

	}
});


setInterval(function() {		// This AJAX call is set to run every 10 minutes, and update the feeds and take the user back to the first 
								// page of the current cateogry

	var $feedsElem = $('div.feedsdiv');
	var $pagenoElem = $('p.pageno');
	var $prevElem = $(':button.prev');
	var $nextElem = $(':button.next');

	feedno = $('p.feedno').text();
	urlToBeCalled = '/freshfeeds/' + feedno.toString();
	
	$.ajax({
		url: urlToBeCalled,
		datatype: 'json',
		complete: function(jqXHR, textStatus) {
			var response = jQuery.parseJSON(jqXHR.responseText);
			$feedsElem.empty();
			$pagenoElem.empty();
			$prevElem.empty();
			$nextElem.empty();

			for (var i=0, len=response.length; i<len; ++i) {
				var feed = response[i];
				$feedsElem.append('<div class="row">' + 
						'<h3 class="text-center"><b>' + feed.title + '</b></h3>' + 
						'<div class="image"><img src="' + feed.imageurl + '" alt="No picture available"></div>' +
						'<div class="description">' + feed.description + '...<a href="' + feed.url + '">See more</a></div>' + '</div>');
			}

			$pagenoElem.text('Page 1');
			$prevElem.attr("style", "visibility: hidden");
			$nextElem.text('Next →');
			$nextElem.removeAttr("style");
		}
	});

}, 600000);