$(document).ready(function() {
  // Handler for .ready() called.
  if(window.console){
    console.log("Loading Document");    
  }
    $('input.accept-face').click(function(){
	name_face($('input[type="text"][portrait-id="'+ $(this).attr('portrait-id')+ '"]').val(), $(this).attr('portrait-id')  )
	/*other logic here */
	$('ul[portrait-id=' + $(this).attr('portrait-id') + '] > li.portrait-name').html(
	    '<label>' + $('input[type=text][portrait-id=' + $(this).attr('portrait-id') + ']').val() + '</label>'
	);
	$('ul[portrait-id=' + $(this).attr('portrait-id') + '] > li.portrait-input').html(
	    '<input portrait-id="' + $(this).attr('portrait-id') + '" class="reject-face" type="button" value="No es un Rostro">'
	);
	$('img[portrait-id="' + $(this).attr('portrait-id') + '"]').removeClass('not-face');

    });
    $('input.reject-face').click(function(){
	not_face($(this).attr('portrait-id'));
	$('ul[portrait-id=' + $(this).attr('portrait-id') + '] > li.portrait-name').html(
	    '<input portrait-id="' + $(this).attr('portrait-id') +'" type="text">'
	);
	$('ul[portrait-id=' + $(this).attr('portrait-id') + '] > li.portrait-input').html(
	    '<input portrait-id=" ' + $(this).attr('portrait-id') +' " class="accept-face" type="button" value="Nombrar Rostro">'
	);
	$('img[portrait-id="' + $(this).attr('portrait-id') +'"]').addClass('not-face')
    });
  
});

