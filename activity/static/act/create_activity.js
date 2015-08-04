$(document).ready(function(){
    $('.datepicker').datepicker({dateFormat: 'yy-mm-dd'});
    $('form#activity').submit(function(event){
	event.preventDefault();
	$.ajax({
	    url:'act/activity/create',
	    type: 'post',
	    dataType: 'json',
	    data: $('#activity').serialize(),
	    success: function(data){
		console.log(data);
	    }
	})
    })
})
