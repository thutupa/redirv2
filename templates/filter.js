function clearExistingData() {
    $('#redirects_table tr[id!="header_row"]').each(
	function(i, el) { 
	    $(el).remove();
	});
}

function showFilterLoading() {
    $('#redirects_table').progressbar({disabled: false, value: false});
}

function stopFilterLoading() {
    $('#redirects_table').progressbar('destroy');
}

var filterAjax;

function invokeFilter(e) {
    filterAjax = $.ajax({
	url: '{{Constants.Path.MATCH_PATH}}',
	dataFilter: function(data, type) {
	    return data.substring('{{Constants.JSON_PREFIX}}'.length);
	},
	data: {'{{Constants.Param.MATCH}}': $('#filterphrase').val()},
	dataType: 'json',
	success: processFilterResult,
	error: processFilterFailure,
    });
    showFilterLoading();
    e.preventDefault();
}

function processFilterResult(data, textStatus, jqXHR){
    var dataHtml = [];
    for (var i=0; i < data.length; i++) {
	var el = data[i];
	var elHtml = '<tr>' +
	    '<td><a href="' +  el.link + '">' + el.phrase + '</a></td>' +
	    '<td>' + el.created + '</td>'
	    '<td><button>edit</button></td>'
	    '<td><button>delete</button></td>' +
	    '</tr>';
	dataHtml.push(elHtml);
    }
    if (data.length == 0) {
	dataHtml = ['<tr><td colspan="4">No results to show, use the form below to add</td></tr>'];
    }
    stopFilterLoading();
    $('#redirects_table tr[id="header_row"]').after(dataHtml.join('\n'));
}

function processFilterFailure(jqXHR, textStatus, errorThrown) {
    alert("Failed to fetch data");
}

$('#filterform').submit(invokeFilter);
$('#filterform').submit();
