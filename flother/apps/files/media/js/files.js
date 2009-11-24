if (typeof(flother) === 'undefined') flother = {};
if (typeof(flother.apps) === 'undefined') flother.apps = {};

flother.apps.files = {
	chosenTextArea: null,

	init: function () {
		$.getJSON('/admin/files/json/', flother.apps.files.appendFilesList);
		var linkPara = $('<p class="help"><a class="add_file" href="#files_list_wrapper">Insert file</a></p>');
		linkPara.find('a').click(function () {
			flother.apps.files.chosenTextArea = $(this).parent().prev('textarea');
		}).fancyZoom({
			directory: 'http://media.flother.com/apps/files/js/fancyzoom/images',
			height: 400,
			width: 555
		});
		$('textarea').after(linkPara);
	},

	appendFilesList: function (data) {
		var filesList = '<div id="files_list_wrapper"><ul id="files_list">';
		for (var fileIndex in data) {
			var file = data[fileIndex];
			filesList += '<li ' + (fileIndex % 4 == 0 ? 'class="rowstart" ' : '') +
				'id="file_' + file['id'] + '" title="' + file['url'] + '">' +
				'<a onclick="return flother.apps.files.addFileToTextArea(this);" href="#">' +
				file['thumbnail_html'] + file['title'] + '</a></li>';
		}
		filesList += '</ul></div>';
		filesList = $(filesList);
		filesList.find('li').click(flother.apps.files.addFileToTextArea);
		$('#footer').before(filesList);
	},

	addFileToTextArea: function (el) {
		var link = $(el);
		var url = link.parent().attr('title');
		var title = link.text();
		var markdownSyntax = '![' + title + '](' + url + ')';
		flother.apps.files.chosenTextArea.replaceSelection(markdownSyntax, true);
		$('#zoom_close').click();
		return false;
	}
};

$(flother.apps.files.init);
