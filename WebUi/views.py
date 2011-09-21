# Create your views here.

from django.shortcuts import render_to_response

def MainPage(request):
  return render_to_response( 'mainpage.html', locals() )
