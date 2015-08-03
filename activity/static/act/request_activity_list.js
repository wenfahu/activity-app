$(document).ready(function(){
    $.get('/act/activity/requestAll', function(data){
	_.map(data, function(ele){
	    console.log(ele.fields);
	});
	var $tmpl = $('#tmpl').text();
	var compiled = _.template($tmpl);
	var output = compiled({data : data});
	//var output = _.template($tmpl, data);
	$('#list').html(output);
    })
})
