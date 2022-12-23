from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import requests
# Create your views here.

def home_view(request):
    # Schedule the task to run in the background
    context = {
        'result': 'msg',
    }
    # Return a response to the client
    return render(request, 'home_view.html', context)
