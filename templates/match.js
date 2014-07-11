function clearExistingData() {
    $('#redirects_table tr[id!="header_row"]').each(
	function(i, el) { 
	    $(el).remove();
	});
}

function showMatchLoading() {
    $('#redirects_table').progressbar({disabled: false, value: false});
}

function stopMatchLoading() {
    $('#redirects_table').progressbar('destroy');
}

var matchAjax;

function invokeMatch(e) {
    matchAjax = $.ajax({
	url: '{{Constants.Path.MATCH_PATH}}',
	dataMatch: function(data, type) {
	    return data.substring('{{Constants.JSON_PREFIX}}'.length);
	},
	data: {'{{Constants.Param.MATCH}}': $('#matchphrase').val()},
	dataType: 'json',
	success: processMatchResult,
	error: processMatchFailure,
    });
    showMatchLoading();
    e.preventDefault();
}

function processMatchResult(data, textStatus, jqXHR){
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
    stopMatchLoading();
    $('#redirects_table tr[id="header_row"]').after(dataHtml.join('\n'));
}

function processMatchFailure(jqXHR, textStatus, errorThrown) {
    alert("Failed to fetch data");
}

$('#matchform').submit(invokeMatch);
$('#matchform').submit();
