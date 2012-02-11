$(document).ready(function(){
    $('input.photo').click(delete_photo);
    $('input.accept-face').live( "click", function(){	
	name_face($('input[type=text][portrait-id=' + $(this).attr('portrait-id') + ']').val(),
		  $(this).attr('portrait-id'));
	/* css magic goes here */
	$('ul[portrait-id=' + $(this).attr('portrait-id') + '] > li.portrait-name').html(
	    '<label>' + $('input[type=text][portrait-id=' + $(this).attr('portrait-id') + ']').val() + '</label>'
	);
	$('ul[portrait-id=' + $(this).attr('portrait-id') + '] > li.portrait-input').html(
	    '<input portrait-id="' + $(this).attr('portrait-id') + '" class="reject-face" type="button" value="No es un Rostro">'
	);
    });

    $('input.reject-face').live( "click", function(){
	not_face($(this).attr('portrait-id'));
	$('ul[portrait-id=' + $(this).attr('portrait-id') + '] > li.portrait-name').html(
	    '<input portrait-id="' + $(this).attr('portrait-id') +'" type="text">'
	);
	$('ul[portrait-id=' + $(this).attr('portrait-id') + '] > li.portrait-input').html(
	    '<input portrait-id="' + $(this).attr('portrait-id') +'" class="accept-face" type="button" value="Nombrar Rostro">'
	);
    });

});

function delete_photo()
{

    
    $.ajax({
	type: "POST",
	headers: {"X-CSRFToken": getCookie("csrftoken")},
	url: "delete_photo",
	data: {'photo_id': $(this).attr('photo_id') },
	success: function(msg){
            if(window.console)
            {
		console.log("Sucess Delete Photo");
            }
	},
	error: function(jqXHR, textStatus, errorThrown)
	{
            if(window.console)
            {
		console.log("Fail Delete Photo");
            }
	}
    });
}