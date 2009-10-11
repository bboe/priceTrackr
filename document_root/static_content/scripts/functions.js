function searchInputClick() {
	input = document.getElementById('searchInput')
	if (input.value == 'search...') input.value = ''
}

function searchInputBlur() {
	input = document.getElementById('searchInput')
	if (input.value == '') input.value = 'search...'
}