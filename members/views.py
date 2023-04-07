from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', '/')
            if  next_page == '/members/login_user':
            # Redirect to a success page.
                return redirect('home_view')
            else:
                return redirect(next_page)
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("Username or password is not correct, Please try again!"))
            return redirect('login_user')
    else:
        return render(request, 'authentication/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out!"))
    return redirect('login_user')