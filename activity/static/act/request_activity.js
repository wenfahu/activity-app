$(document).ready(function(){
    //semantic.button.ready();
    $('button#follow').
	state({
	    text:{
		inactive : 'Join',
		active: 'Joined'
	    }
    });
    var $vote_status = $('#vote_status').text();
    if($vote_status == 'True'){
	var $vote_toggle = true;
    }
    else{
	$vote_toggle = false;
    }
    var $status = $('#user_status').text();
    if($status == 'True'){
	var $toggle = true;
    }
    else{
	$toggle = false;
    }
    var $sid = $('#sid').text();
    $('button#follow').click(function(){
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
    });
    $('i#vote').click(function(){
	var unvote_url = '/act/activity/' + $sid + '/cancel_vote';
	var vote_url = '/act/activity/' + $sid + '/vote';
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
	if($vote_toggle){
	    $.post(unvote_url, function(data){
		console.log(data);
		console.log(data.vote);
		$('#vote').removeClass('red').addClass('empty');
		$('#votes').html(data.vote);
	    });
	}
	else{
	    $.post(vote_url, function(data){
		console.log(data);
		$('#vote').removeClass('empty').addClass('red');
		console.log(data.vote);
		$('#votes').html(data.vote);
	    });
	}
	$vote_toggle = !$vote_toggle;
    });
})
