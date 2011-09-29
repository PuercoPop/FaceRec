$(document).ready(function() {
  // Handler for .ready() called.
  if(window.console){
    console.log("Cargando  Texto, maru length of " + $('.maru').length );
    
  }
  $('.maru').click(click_maru);
  $('.batsu').click(click_batsu);
  

  
});

function click_maru()
{

    var Id_Texto =  '#text_' + $(this).attr('num');
    var data_params = {
        'TXT_INPUT': $(Id_Texto).val()       
    };
    alert( Id_Texto);
    
    $.ajax({
      type: "POST",
      url: "portrait_chosen",
      data: data_params,
      success: function(msg){
        alert( "Data Saved: " + msg );
      },
      error: function(jqXHR, textStatus, errorThrown){
        alert("Fallo Post");        
      }
    });  
  
}



function click_batsu()
{
  /* Hay que mandar el filname a borrar y hacer .fadeOut a la div entero. Falta disable el Maru*/
     
  var data_params = { 'portrait_id' : $('#portrait_' + $(this).attr('num')).attr('src') };
  
  $('#portrait_container_'+$(this).attr('num')).fadeTo(2000, 0.3,"linear");
  $(this).prop('disabled', true);
  
  
  $.ajax({
      type: "POST",
      url: "portrait_rejected",
      data: data_params,
      success: function(msg){
        alert( "Data Saved: " + msg );
      },
      error: function(jqXHR, textStatus, errorThrown){
        alert("Fallo Post");        
      }
    });  
}