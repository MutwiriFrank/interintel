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



## Designing

![All designs](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/all%20designs.PNG)

First started by designing the layout of the login page on a mobile phone and a desktop using figma.
 
The first design is how the login should appear on a mobile phone.

![mobile login page design](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/mobile%20logn%20design.PNG)

The second design is how the login page should appear on a desktop.
![Desktop login page design](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/desktop%20login%20design.PNG)

The third design is the success page which also  has a search and result functionality.
![Search and result page design](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/orders_home.PNG)

#### Project Tree

![cms](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/full%20tree.PNG)


## Login
The login frontend is coded using HTML and css, with actual input  and displaying of errors
taking place in the form. The data is sent to django using POST method.
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
###### Backend



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
![redirect to home](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/home%20page.PNG)

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

If a user does not exist or key in wrong details an error message is sent to the login page.
```
else:


    # return message to the form if username and password dont match
    messages.error(request, "username and password do not match, \n Try again")
    return redirect('login')
        
```

![wrong password](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/wrong%20password.PNG)

Finally if no POST request was made and the user is not authenticated the login page is rendered.
```
else:
    return render(request, 'account/login.html',)
```

## Search 

Tree of our Django app with search functionality

![Tree](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/CMS.PNG)

First we create our models in models.py
```
class Category(models.Model):
    category = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category


class Product(models.Model):

    STATUS_CHOICES = (
        ('Available', 'item ready to be purchased'),
        ('sold', 'item sold'),
        ('restocking', 'item restocking in few days'))

    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available', blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('OnTransit', 'OnTransit'),
        ('Delivered', 'Delivered')
    )

    customer = models.CharField(max_length=100, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    issue_quantity = models.IntegerField(default=0, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.customer )


```

We then create a search form in forms.py 
```
class SearchForm(forms.Form):
    q = forms.CharField()

```

In views.py we create a orders function which recieve a request function.

The sesiion is then used to identify the user

```
def orders(request):

    if 'user' in request.session:
        current_user = request.session['user']
```

search form is then used to create a form object  which is rendered to the HTML page. 
other variables to be rendered to html are also initialized
```
<form action="{% url 'orders' %}" method="get">
  <input type="search" placeholder="Search for order.." name="q">
  <button type="submit"><i class="fa fa-search"></i></button>
</form>

```

In the HTML we give our input a name q so which we will use to access data sent by GET request method
 in the views. 
 In the views we check if there is a GET request, and puth the data in a form variable. 
 The form is then validated and we extract  "q" which is the data input in the form.
 
 
We then utilize PostgreSQL’s full text search engine by using SearchVector, enable search on 
different fields in a model, and searchquery which By default, all the words the user provides are passed through the
 stemming algorithms, and then it looks for matches for all of the resulting terms.
 
 we need to add     'django.contrib.postgres', to installed apps to use this feature
 
 
```
 INSTALLED_APPS = [
  
    'django.contrib.postgres',
  
]

```


```
 if 'q' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            orders = Order.objects.annotate(search=SearchVector('customer', 'product', 'status', 'note'),
            ).filter(search=SearchQuery(q))
```
**Search results for orders whose status is pending**

![pending status result](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/status%20search.PNG)

**Search results for orders when 'mutugi' a customer name**

![customer name search results](https://raw.githubusercontent.com/MutwiriFrank/interintel/master/images/search%20customer.PNG)

if no search has been made all orders should ve rendered
```
else:
    orders = Order.objects.all().order_by('id')
```
At the top of the page we have 4 divs which display the count of all orders' status

##Database 
For this project a postgreSQL database was used, which has to be configured in the settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'interinteldb',
        'USER': 'postgres',
        'PASSWORD': '<enter your postgress password>',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
And 