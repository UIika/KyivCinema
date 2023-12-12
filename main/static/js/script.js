const outputElement = document.getElementById('liveSearchResults')

jQuery(document).ready(function ($) {
	$('.live-search-list li').each(function () {
		$(this).attr('data-search-term', $(this).text().toLowerCase())
	})

	$('.live-search-box').on('keyup', function () {
		var searchTerm = $(this).val().toLowerCase()
		var visibleItems = 0

		$('.live-search-list li').each(function () {
			var text = $(this).attr('data-search-term')
			if (text.indexOf(searchTerm) !== -1 || searchTerm.length < 1) {
				outputElement.hidden = false
				if (visibleItems < 5) {
					$(this).show()
					visibleItems++
				} else {
					$(this).hide()
				}
			} else {
				$(this).hide()
			}
		})
		$('#liveSearchResults').each(function () {
			if (searchTerm.length < 1) {
				outputElement.hidden = true
			}
		})
	})
})