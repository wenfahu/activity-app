$(function(){
    $.get('http://localhost:8000/act/user/requestAll', function(data){
	var $tmpl = $('#user_list').text();
	var $complied = _.template($tmpl);
	var $html = $complied({data: data});
	$('#users').html($html);
    });
})
