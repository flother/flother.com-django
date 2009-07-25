jQuery(function() {
	jQuery('textarea').wymeditor({
		logoHtml: '',
		iframeBasePath: '/wymeditor/iframe/',
		toolsItems: [
			{'name': 'Bold', 'title': 'Strong', 'css': 'wym_tools_strong'}, 
			{'name': 'Italic', 'title': 'Emphasis', 'css': 'wym_tools_emphasis'},
			{'name': 'Paste', 'title': 'Paste_From_Word', 'css': 'wym_tools_paste'},
			{'name': 'Undo', 'title': 'Undo', 'css': 'wym_tools_undo'},
			{'name': 'Redo', 'title': 'Redo', 'css': 'wym_tools_redo'},
			{'name': 'InsertOrderedList', 'title': 'Ordered_List', 'css': 'wym_tools_ordered_list'},
			{'name': 'InsertUnorderedList', 'title': 'Unordered_List', 'css': 'wym_tools_unordered_list'},
			{'name': 'Indent', 'title': 'Indent', 'css': 'wym_tools_indent'},
			{'name': 'Outdent', 'title': 'Outdent', 'css': 'wym_tools_outdent'},
			{'name': 'CreateLink', 'title': 'Link', 'css': 'wym_tools_link'},
			{'name': 'Unlink', 'title': 'Unlink', 'css': 'wym_tools_unlink'},
			{'name': 'InsertImage', 'title': 'Image', 'css': 'wym_tools_image'},
			{'name': 'InsertTable', 'title': 'Table', 'css': 'wym_tools_table'},
			{'name': 'ToggleHtml', 'title': 'HTML', 'css': 'wym_tools_html'}
		],
		classesItems: [
			{'name': 'illustration', 'title': 'PARA: Illustration', 'expr': 'p'},
			{'name': 'figure', 'title': 'PARA: Figure', 'expr': 'p'}
		]
	});
});
