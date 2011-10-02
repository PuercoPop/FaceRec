$(document).ready(function() {
  // Handler for .ready() called.
  if(window.console){
    console.log("Loading Document");    
  }
  $('.maru').click(click_maru);
  $('.batsu').click(click_batsu);
  
  
});

function click_maru()
{
    /*Hay que mandar tanto el path como el identificador de la persona*/
    var data_params = { 'portrait_path' : $('#portrait_' + $(this).attr('num')).attr('src') , 'portrait_name': $('#text_' + $(this).attr('num')).val(),'parent_photo':$('#main_photo').attr('src') };
    
    $.ajax({
      type: "POST",
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
  
}



function click_batsu()
{
  /* Hay que mandar el filname a borrar y hacer .fadeOut a la div entero. Falta disable el Maru*/
     
  var data_params = { 'portrait_id' : $('#portrait_' + $(this).attr('num')).attr('src') };
  
  $('#portrait_container_'+$(this).attr('num')).fadeTo(1000, 0.3,"linear");
  $(this).prop('disabled', true);
  
  
  $.ajax({
      type: "POST",
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