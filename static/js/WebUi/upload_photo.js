$(document).ready(function() {
  // Handler for .ready() called.
  if(window.console){
    console.log("Loading Document");    
  }
    $('input.accept-face').click(function(){
	name_face($('input[type="text"][portrait-id="'+ $(this).attr('portrait-id')+ '"]').val(), $(this).attr('portrait-id')  )
	/*other logic here */
    });
  $('input.reject-face').click(not_face);
  
});

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