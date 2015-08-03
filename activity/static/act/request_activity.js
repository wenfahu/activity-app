$(document).ready(function(){
    semantic.button.ready();
    $('button#follow').click(function(){
	var $sid = $('#sid').text();
	console.log($sid);
	var $url = '/act/activity/' + $sid + '/join';
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
	$.post($url, function(data){
	    console.log(data);
	})
    })
})

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



