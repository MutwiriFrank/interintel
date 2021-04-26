from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import request
from django.contrib import messages


# Create your views here.


def login_page(request):

    # checks if a client is authenticated,
    username = password = ''  # sets username to null

    if request.user.is_authenticated:
        return redirect('orders')

    else:
        # checks if a POST request has been sent
        if request.POST:

            username = request.POST.get('username')
            password = request.POST.get('password')
            # print(username)
            # print(password)
            # authenticate user if the user exist in db
            user = authenticate(request, username=username, password=password)

            if user is not None: # if the user exist in db a session is
                # created and username is used to identify the session
                if user.is_active:
                    # Get a session value by its key
                    request.session['user'] = username
                    # print(request.session['user'])
                    login(request, user)

                return redirect('orders')

            else:
                # print('am here')

                # return message to the form if username and password dont match
                messages.error(request, "username and password do not match, \n Try again")
                return redirect('login')
        else:
            return render(request, 'account/login.html',)



def logout_page(request):
    logout(request)  # a user is logout
    request.session.flush()  # session is destroyed
    request.user = 'AnonymousUser'
    # print('session deleted')
    return redirect('login')
