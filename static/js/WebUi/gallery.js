$(document).ready(function(){
    $('input.photo').click(delete_photo);

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