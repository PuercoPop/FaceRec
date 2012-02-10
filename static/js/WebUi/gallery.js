$(document).ready(function(){
    $('input.photo').click(delete_photo);
    $('input.accept-face').click(function(){	
	name_face($('input[type=text][portrait-id=' + $(this).attr('portrait-id') + ']').val(),
		  $(this).attr('portrait-id'));
	/* css magic goes here*/
    });

    $('input.reject-face').click(function(){
	not_face($(this).attr('portrait-id'));
	
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