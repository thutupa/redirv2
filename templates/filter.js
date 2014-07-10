function clearExistingData() {
    $('#redirect_data').html('');
}

function showFilterLoading() {
    $('#redirects_table').progressbar({disabled: false, value: false});
}

function stopFilterLoading() {
    $('#redirects_table').progressbar({disabled: false});
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
    $('#redirect_data').html(dataHtml.join('\n'));
}

function processFilterFailure(jqXHR, textStatus, errorThrown) {
    alert("Failed to fetch data");
}

$('#filterform').submit(invokeFilter);
$('#filterform').submit();
