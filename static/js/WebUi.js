function getCookie(c_name)
    {
        if (document.cookie.length > 0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1)
            {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    };


$(document).ready(function() {
  // Handler for .ready() called.
  if(window.console){
    console.log("Loading Document");    
  }
  $('.maru').click(click_maru);
  $('.batsu').click(click_batsu);
  
  $( "div.portrait-container").each( function( index,ele) { $(this).css('top', 90*(index+1) + 'px') } );
  
  
  
});

function click_maru()
{
    /*Hay que mandar tanto el path como el identificador de la persona*/
    var data_params = { 'portrait_path' : $('#portrait_' + $(this).attr('num')).attr('path') , 'portrait_name': $('#text_' + $(this).attr('num')).val(),'parent_photo':$('#main_photo').attr('path') };
    
    $.ajax({
	type: "POST",
	headers: {"X-CSRFToken": getCookie("csrftoken")},
	url: "portrait_chosen",
	data: data_params,
	success: function(msg){
            if(window.console)
            {
		console.log("Sucess Maru");
            }
	},
	error: function(jqXHR, textStatus, errorThrown)
	{
            if(window.console)
            {
		console.log("Fail Maru");
            }
	}
    });
    
    $(this).css('color','#1FF507');
    $(this).prop('disabled',true);
  
}



function click_batsu()
{
  /* Hay que mandar el filname a borrar y hacer .fadeOut a la div entero. Falta disable el Maru*/
     
  var data_params = { 'portrait_id' : $('#portrait_' + $(this).attr('num')).attr('path') };
  
  $('#portrait_container_'+$(this).attr('num')).fadeTo(1000, 0.3,"linear");
  $(this).prop('disabled', true);
  $(this).css('color','#CC0000');
  
  $.ajax({
      type: "POST",
      headers: {"X-CSRFToken": getCookie("csrftoken")},
      url: "portrait_rejected",
      data: data_params,
      success: function(msg){
         if(window.console)
         {
           console.log("Sucess Batsu");
         }
      },
      error: function(jqXHR, textStatus, errorThrown){
        if(window.console)
         {
           console.log("Fail Batsu");
         }
      }
    });  
}