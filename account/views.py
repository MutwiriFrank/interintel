from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import request
from django.contrib import messages


# Create your views here.


def login_page(request):
    username = password = ''

    if request.user.is_authenticated:
        return redirect('orders')

    else:

        if request.POST:

            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    # Get a session value by its key
                    request.session['user'] = username
                    print(request.session['user'])
                    login(request, user)

                return redirect('orders')

            else:
                print('am here')

                messages.error(request, "username and password do not match, \n Try again")
                return redirect('login')
        else:

            return render(request, 'account/login.html',)


def logout_page(request):
    logout(request)
    request.session.flush()
    request.user = 'AnonymousUser'
    # print('session deleted')
    return redirect('login')
