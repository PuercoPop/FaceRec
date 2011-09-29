$(document).ready(function() {
  // Handler for .ready() called.
  if(window.console){
    console.log("Cargando  Texto, maru length of " + $('.maru').length );
    
  }
  $('.maru').click(click_maru);
  $('.batsu').click(click_batsu);
  

  
});




function on_submit()
{
  /*Se llama a la función de python*/
}

function post_submit()
{
 /*Una vez que ya se subio la foto y se grabaron los potenciales retratos se les tiene que incorpoar en la página*/ 
}

function click_maru()
{

    var Id_Texto =  '#text_' + $(this).attr('num');
    var data_params = {
        'TXT_INPUT': $(Id_Texto).val()       
    };

    
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