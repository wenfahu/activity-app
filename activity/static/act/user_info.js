$(document).ready(function(){
    var username = $('#username').text();
    console.log(username);
    var url = '/act/user/' + username + '/request';
    console.log(url);
    $.get(url, function(data){
	var tmpl = $('#tmpl').text();
	var compiled = _.template(tmpl);
	var content = compiled({data: data});
	$('#content').html(content);
    });
})
