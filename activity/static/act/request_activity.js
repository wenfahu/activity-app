$(document).ready(function(){
    //semantic.button.ready();
    $('button#follow').
	state({
	    text:{
		inactive : 'Join',
		active: 'Joined'
	    }
    });
    var $status = $('#user_status').text();
    if($status == 'True'){
	var $toggle = true;
    }
    else{
	$toggle = false;
    }
    $('button#follow').click(function(){
	var $sid = $('#sid').text();
	console.log($sid);
	var $joinUrl = '/act/activity/' + $sid + '/join';
	var $quitUrl = '/act/activity/' + $sid + '/quit';
	var csrftoken = $.cookie('csrftoken');
	function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	    }
	});
	if($toggle){
	    $.post($quitUrl, function(data){
		console.log(data);
	    })
	}
	else {
	    $.post($joinUrl, function(data){
		console.log(data);
	    })
	}
	$toggle = !$toggle;
    })
})

/*
var semantic.button = {};
var semantic.button.ready = function(){
    var 
    $button = $('.ui.buttons .button'),
    $toggle = $('.main .ui.toggle.button'),
    $button = $('.ui.button').not($buttons).not($toggle),
    handler = {
	activate: function(){
	    $(this)
		.addClass('active')
		.siblings()
		.removeClass('active');
	}
    }
    $buttons.on('click', handler.activate);
    $toggle.state({
	text: {
	    inactive: 'join',
	    active: 'joined'
	}
    });
};

*/


