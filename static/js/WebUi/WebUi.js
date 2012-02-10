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


function name_face( name, portrait_id )
{
    /*Hay que mandar tanto el path como el identificador de la persona*/
    var data_params = { 
	'portrait_name': name,
	'portrait_id': portrait_id
    };
    
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
};

function not_face(portrait_id)
{
  /* Hay que mandar el filname a borrar y hacer .fadeOut a la div entero. Falta disable el Maru*/
     
    var data_params = { 'portrait_id' : portrait_id};
  
    //$('#portrait_container_'+$(this).attr('num')).fadeTo(1000, 0.3,"linear");
  
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
};