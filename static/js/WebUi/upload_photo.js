$(document).ready(function() {
  // Handler for .ready() called.
  if(window.console){
    console.log("Loading Document");    
  }
    $('input.accept-face').click(function(){
	name_face($('input[type="text"][portrait-id="'+ $(this).attr('portrait-id')+ '"]').val(), $(this).attr('portrait-id')  )
	/*other logic here */
    });
    $('input.reject-face').click(function(){
	not_face($(this).attr('portrait-id'));
    });
  
});

