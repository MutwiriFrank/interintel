# Simple Django Login and Search

This is a example of Django project with design of pages using figma,  login,
 maintain sessions, and search using postgres full text search.



###Contents

- **Designing Layouts**
>
- **Login**

- **Sessions**
 
-  **Logout**

- **Search**

- **Results**

- **Database configuration**


##Installing

**Clone the project**

git clone https://github.com/MutwiriFrank/interintel.git

**Install dependencies**
pip install -r requirements.txt



##Designing

![All designs](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/interIntel_interview_UI%20Kit%20all%20designs.pdf)

First started by designing the layout of the login page on a mobile phone and a desktop using figma.
 
The first design is how the login should appear on a mobile phone.

![mobile login page design](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/mobile%20logn%20design.PNG)

The second design is how the login page should appear on a desktop.
![Desktop login page design](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/desktop%20login%20design.PNG)

The third design is the success page which also  has a search and result functionality.
![Search and result page design](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/orders_home.PNG)

####Tree

#### Login
The login frontend is coded using HTML and css, with actual login
taking place in the form.
```
<form  class="login-form" name="LoginForm" action="{% url 'login' %}" method="post">
    {% csrf_token %}
    
    <input class="email" id="username" name='username'  placeholder="username">
    <input class="password" placeholder="PASSWORD" type="password" id="password" name='password'>
    <div class="form-check">
      <input class="form-check-input" type="checkbox" value="" id="defaultCheck1">
      <label class="form-check-label" for="defaultCheck1">
        <p id="checkbox">Remember me</p>
          {% for message in messages %}
          <li class="{{ message.tags }}">{{ message }}</li>
        {% endfor %}
    
      </label>
    
    </div>
    <input type="submit" class="button Input-button" value="Login">
    <div class="new_to_signup">
        {{ message.errors }}
        <p class="new_to_signup_p">New to Intertel?<a href="">  Sign up</a> </p>
    
    
    </div>
    
</form>

```
######Backend



A login_page function is used to login users.  First username and password is set to null, then  Django checks if user 
is authenticated. if user is authenticated, the user is redirected to our home page.
```
def login_page(request):

    # checks if a client is authenticated,
    username = password = ''  # sets username to null

    if request.user.is_authenticated:
        return redirect('orders')

``` 
Django then checks if there is a post request made, if there is  a POST request, we extracts username and password,
as they are set in the html

```
if request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate user if the user exist in db
        user = authenticate(request, username=username, password=password)

```

html
```
<input class="email" id="username" name='username'  placeholder="username">
<input class="password" placeholder="PASSWORD" type="password" id="password" name='password'>

```

If the user exist in the database a session is gotten and  is used to identify the session and 
helps maintain user state and data all over the application. The user is then logged in and redirected to home page.
```
if user is not None: # if the user exist in db a session is
    # created and username is used to identify the session
    if user.is_active:
        # Get a session value by its key
        request.session['user'] = username
        login(request, user)
    return redirect('orders')
```

To use these sessions, configurations have to be in project's INSTALLED_APPS and MIDDLEWARE sections in settings.py

```
INSTALLED_APPS = [
    ...
    'django.contrib.sessions',
    ....

MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    ....

```

If a user does not exist or key in wrong details an error message is sent to the user.
```
else:
    # print('am here')

    # return message to the form if username and password dont match
    messages.error(request, "username and password do not match, \n Try again")
    return redirect('login')
        
```

Finally if no POST request was made and the user is not authenticated the login page is rendered.
```
else:
    return render(request, 'account/login.html',)
```