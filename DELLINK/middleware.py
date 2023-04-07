from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
class AuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != '/members/login_user' and request.path != '/':
            request.session['next'] = request.path
            return redirect('login_user')
        response = self.get_response(request)
        return response