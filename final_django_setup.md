Thank you for confirming that everything is working! Below is a comprehensive, step-by-step tutorial to set up your Django AQI Dashboard server from scratch, tailored to your project (`C:\\\\Users\\\\User\\\\Desktop\\\\SMART AIR\\\\Code\\\\RGB Matrix\\\\ESP8266\\\\FINAL\\\\django\\\_second\\\\aqi\\\_project`). This tutorial incorporates all the fixes and improvements we’ve made, including the beautiful Bootstrap-based UI, rate limiting with `django-ratelimit`, SQLite database, and handling of `python-decouple` issues. It’s designed for someone new to Django, like yourself, and serves as a reference for future setups. The project replicates your Flask app’s functionality, including user authentication, customer management, AQI data processing, and CSV exports, with a modern and responsive design.



---



\# Tutorial: Setting Up a Django AQI Dashboard Server from Scratch



This tutorial guides you through creating a Django-based AQI Dashboard server that manages air quality sensor data, allows admin users to log in, add/edit/delete customers, and download customer data as CSV. It uses SQLite for the database, `django-ratelimit` for rate limiting, and Bootstrap 5 for a beautiful UI. The project is set up at `C:\\\\Users\\\\User\\\\Desktop\\\\SMART AIR\\\\Code\\\\RGB Matrix\\\\ESP8266\\\\FINAL\\\\django\\\_second\\\\aqi\\\_project`.



\## Prerequisites

\- \*\*Python\*\*: Install Python 3.12 (or latest stable version) from https://www.python.org/downloads/.

\- \*\*pip\*\*: Ensure `pip` is installed (`python -m ensurepip --upgrade`).

\- \*\*Virtual Environment (Optional)\*\*: Recommended to isolate dependencies.

\- \*\*Text Editor\*\*: Use VS Code or any editor for coding.

\- \*\*Terminal\*\*: Command Prompt or PowerShell on Windows.



\## Step 1: Set Up the Project Directory

1\. \*\*Create the Project Directory\*\*:

   ```bash

   mkdir "C:\\Users\\User\\Desktop\\SMART AIR\\Code\\RGB Matrix\\ESP8266\\FINAL\\django\_second"

   cd "C:\\Users\\User\\Desktop\\SMART AIR\\Code\\RGB Matrix\\ESP8266\\FINAL\\django\_second"

   ```



2\. \*\*Create a Virtual Environment (Optional)\*\*:

   ```bash

   python -m venv venv

   .\\venv\\Scripts\\activate

   ```



   If activated, your prompt should show `(venv)`.



3\. \*\*Install Django and Dependencies\*\*:

   ```bash

   pip install django django-ratelimit python-decouple

   ```



   - `django`: The web framework.

   - `django-ratelimit`: For rate limiting API and login requests.

   - `python-decouple`: For managing environment variables (with a fallback if it fails).



\## Step 2: Create the Django Project

1\. \*\*Start the Project\*\*:

   ```bash

   django-admin startproject aqi\_project .

   ```



   This creates the project structure in `C:\\\\Users\\\\User\\\\Desktop\\\\SMART AIR\\\\Code\\\\RGB Matrix\\\\ESP8266\\\\FINAL\\\\django\\\_second\\\\aqi\\\_project`.



2\. \*\*Create the App\*\*:

   ```bash

   python manage.py startapp aqi\_app

   ```



3\. \*\*Register the App\*\*:

   Open `aqi\_project/settings.py` and add `'aqi\\\_app'` and `rest\_framework` to `INSTALLED\\\_APPS`:



   ```python

   INSTALLED\_APPS = \[

       'django.contrib.admin',

       'django.contrib.auth',

       'django.contrib.contenttypes',

       'django.contrib.sessions',

       'django.contrib.messages',

       'django.contrib.staticfiles',

       'aqi\_app',

   ]

   ```



4\. \*\*Configure Static Files and Cache\*\*:

   In `aqi\\\_project/settings.py`, add or verify:



   ```python

   import os

   from pathlib import Path



   BASE\_DIR = Path(\_\_file\_\_).resolve().parent.parent



   STATIC\_URL = '/static/'

   STATICFILES\_DIRS = \[BASE\_DIR / 'static']

   STATIC\_ROOT = BASE\_DIR / 'staticfiles'



   CACHES = {

       'default': {

           'BACKEND': 'django.core.cache.backends.db.DatabaseCache',

           'LOCATION': 'ratelimit\_cache',

       }

   }



   SECRET\_KEY = os.environ.get('SECRET\_KEY', 'fallback-secret-key-1234567890')  # Fallback for python-decouple issues

   DEBUG = True

   ALLOWED\_HOSTS = \['127.0.0.1', 'localhost']

   ```



   - \*\*Note\*\*: The `SECRET\\\_KEY` fallback avoids `python-decouple` issues. Optionally, create a `.env` file with `SECRET\\\_KEY=your-super-secret-key-here` and use:



     ```python

     from decouple import config

     SECRET\_KEY = config('SECRET\_KEY')

     ```



\## Step 3: Set Up the Database

1\. \*\*Define the Model\*\*:

   Open `aqi\\\_app/models.py` and add:



   ```python

   from django.db import models



   class Customer(models.Model):

       name = models.CharField(max\_length=255)

       password = models.CharField(max\_length=255)

       api\_url = models.URLField(max\_length=500)

       email = models.EmailField(blank=True, null=True)

       phone\_number = models.CharField(max\_length=20, blank=True, null=True)

       sensor\_location = models.CharField(max\_length=255, blank=True, null=True)

       sensor\_name = models.CharField(max\_length=255, blank=True, null=True)

       notes = models.TextField(blank=True, null=True)



       def \_\_str\_\_(self):

           return self.name

   ```



2\. \*\*Create Migrations\*\*:

   ```bash

   python manage.py makemigrations

   python manage.py migrate

   ```



3\. \*\*Create the Cache Table\*\*:

   For `django-ratelimit`:

   ```bash

   python manage.py createcachetable

   ```



4\. \*\*Create a Superuser\*\*:

   ```bash

   python manage.py createsuperuser

   ```



   Follow prompts to set a username, email, and password for admin access.



\## Step 4: Create Utility Functions

Create `aqi\\\_app/utils.py` for AQI calculations (based on your Flask app):



```python

import requests



def pm25\\\_to\\\_aqi(pm25):

\&nbsp;   # Simplified AQI calculation (replace with your actual logic)

\&nbsp;   if pm25 < 0:

\&nbsp;       return 0

\&nbsp;   elif pm25 <= 12:

\&nbsp;       return int((50 / 12) \\\* pm25)

\&nbsp;   elif pm25 <= 35.4:

\&nbsp;       return int(((100 - 51) / (35.4 - 12.1)) \\\* (pm25 - 12.1) + 51)

\&nbsp;   else:

\&nbsp;       return 100  # Extend as needed



def aqi\\\_to\\\_cigars\\\_per\\\_day(aqi):

\&nbsp;   # Simplified conversion (replace with your actual logic)

\&nbsp;   return aqi / 50  # Example: 1 cigarette per 50 AQI points



def aqi\\\_to\\\_health\\\_label(aqi):

\&nbsp;   if aqi <= 50:

\&nbsp;       return "good"

\&nbsp;   elif aqi <= 100:

\&nbsp;       return "moderate"

\&nbsp;   else:

\&nbsp;       return "unhealthy"



def get\\\_sensor\\\_type\\\_from\\\_url(url):

\&nbsp;   if "purpleair" in url.lower():

\&nbsp;       return "PurpleAir"

\&nbsp;   return "Unknown"



def extract\\\_pm25\\\_from\\\_url(url):

\&nbsp;   try:

\&nbsp;       response = requests.get(url)

\&nbsp;       response.raise\\\_for\\\_status()

\&nbsp;       data = response.json()

\&nbsp;       # Replace with actual JSON parsing based on your sensor API

\&nbsp;       return float(data.get('pm25', -1))

\&nbsp;   except:

\&nbsp;       return -1

```



\## Step 5: Create Views

Replace `aqi\\\_app/views.py` with:



```python

import secrets

import string

import csv

from io import StringIO

from django.shortcuts import render, redirect, get\\\_object\\\_or\\\_404

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login\\\_required

from django.http import JsonResponse, HttpResponse

from django\\\_ratelimit.decorators import ratelimit

from .models import Customer

from .utils import pm25\\\_to\\\_aqi, aqi\\\_to\\\_cigars\\\_per\\\_day, aqi\\\_to\\\_health\\\_label, get\\\_sensor\\\_type\\\_from\\\_url, extract\\\_pm25\\\_from\\\_url



def generate\\\_alphanum(length=10):

\&nbsp;   alphabet = string.ascii\\\_letters + string.digits

\&nbsp;   return ''.join(secrets.choice(alphabet) for \\\_ in range(length))



@ratelimit(key='ip', rate='15/m', method='POST')

def login\\\_view(request):

\&nbsp;   if getattr(request, 'limited', False):

\&nbsp;       return render(request, 'login.html', {'error': 'Rate limit exceeded. Try again later.'}, status=429)

\&nbsp;   if request.method == 'POST':

\&nbsp;       username = request.POST.get('username')

\&nbsp;       password = request.POST.get('password')

\&nbsp;       user = authenticate(request, username=username, password=password)

\&nbsp;       if user is not None:

\&nbsp;           login(request, user)

\&nbsp;           return redirect('dashboard')

\&nbsp;       return render(request, 'login.html', {'error': 'Invalid credentials'})

\&nbsp;   return render(request, 'login.html')



@login\\\_required

def logout\\\_view(request):

\&nbsp;   logout(request)

\&nbsp;   return redirect('login')



@login\\\_required

def dashboard(request):

\&nbsp;   password\\\_plain = None

\&nbsp;   if request.method == 'POST':

\&nbsp;       name = request.POST.get('name')

\&nbsp;       api\\\_url = request.POST.get('api\\\_url')

\&nbsp;       email = request.POST.get('email')

\&nbsp;       phone\\\_number = request.POST.get('phone\\\_number')

\&nbsp;       sensor\\\_location = request.POST.get('sensor\\\_location')

\&nbsp;       notes = request.POST.get('notes')

\&nbsp;       password\\\_plain = generate\\\_alphanum()

\&nbsp;       sensor\\\_name = get\\\_sensor\\\_type\\\_from\\\_url(api\\\_url)

\&nbsp;       customer = Customer(

\&nbsp;           name=name,

\&nbsp;           password=password\\\_plain,

\&nbsp;           api\\\_url=api\\\_url,

\&nbsp;           email=email,

\&nbsp;           phone\\\_number=phone\\\_number,

\&nbsp;           sensor\\\_location=sensor\\\_location,

\&nbsp;           notes=notes,

\&nbsp;           sensor\\\_name=sensor\\\_name

\&nbsp;       )

\&nbsp;       customer.save()

\&nbsp;   customers = Customer.objects.all()

\&nbsp;   return render(request, 'dashboard.html', {'customers': customers, 'new\\\_password': password\\\_plain})



@login\\\_required

def edit\\\_customer(request, id):

\&nbsp;   customer = get\\\_object\\\_or\\\_404(Customer, id=id)

\&nbsp;   if request.method == 'POST':

\&nbsp;       customer.name = request.POST.get('name', customer.name)

\&nbsp;       new\\\_api\\\_url = request.POST.get('api\\\_url', customer.api\\\_url)

\&nbsp;       customer.email = request.POST.get('email', customer.email)

\&nbsp;       customer.phone\\\_number = request.POST.get('phone\\\_number', customer.phone\\\_number)

\&nbsp;       customer.sensor\\\_location = request.POST.get('sensor\\\_location', customer.sensor\\\_location)

\&nbsp;       customer.notes = request.POST.get('notes', customer.notes)

\&nbsp;       if new\\\_api\\\_url != customer.api\\\_url:

\&nbsp;           customer.api\\\_url = new\\\_api\\\_url

\&nbsp;           customer.sensor\\\_name = get\\\_sensor\\\_type\\\_from\\\_url(new\\\_api\\\_url)

\&nbsp;       customer.save()

\&nbsp;       return redirect('dashboard')

\&nbsp;   return render(request, 'edit\\\_customer.html', {'customer': customer})



@login\\\_required

def delete\\\_customer(request, id):

\&nbsp;   customer = get\\\_object\\\_or\\\_404(Customer, id=id)

\&nbsp;   customer.delete()

\&nbsp;   return redirect('dashboard')



@ratelimit(key='ip', rate='5/m')

def sensor\\\_data(request):

\&nbsp;   if getattr(request, 'limited', False):

\&nbsp;       return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)

\&nbsp;   customer\\\_password = request.GET.get('customer\\\_password')

\&nbsp;   if not customer\\\_password:

\&nbsp;       return JsonResponse({'aqi': -3})

\&nbsp;   customer = Customer.objects.filter(password=customer\\\_password).first()

\&nbsp;   if not customer:

\&nbsp;       return JsonResponse({'aqi': -2})

\&nbsp;   pm25 = extract\\\_pm25\\\_from\\\_url(customer.api\\\_url)

\&nbsp;   if pm25 is None or pm25 < 0:

\&nbsp;       return JsonResponse({'aqi': -1})

\&nbsp;   aqi = pm25\\\_to\\\_aqi(pm25)

\&nbsp;   if aqi == 0:

\&nbsp;       aqi = 1

\&nbsp;   cigars = aqi\\\_to\\\_cigars\\\_per\\\_day(aqi)

\&nbsp;   health\\\_label = aqi\\\_to\\\_health\\\_label(aqi)

\&nbsp;   sensor\\\_name = customer.sensor\\\_name or get\\\_sensor\\\_type\\\_from\\\_url(customer.api\\\_url)

\&nbsp;   return JsonResponse({

\&nbsp;       'customer\\\_id': customer.id,

\&nbsp;       'aqi': aqi,

\&nbsp;       'sensor\\\_name': sensor\\\_name,

\&nbsp;       'cigars': cigars,

\&nbsp;       'health\\\_label': health\\\_label,

\&nbsp;   })



@login\\\_required

def download\\\_customers(request):

\&nbsp;   customers = Customer.objects.all()

\&nbsp;   output = StringIO()

\&nbsp;   writer = csv.writer(output)

\&nbsp;   writer.writerow(\\\['Customer ID', 'Name', 'Password', 'API URL', 'Email', 'Phone Number', 'Sensor Location', 'Sensor Name', 'Notes'])

\&nbsp;   for customer in customers:

\&nbsp;       writer.writerow(\\\[

\&nbsp;           customer.id, customer.name, customer.password, customer.api\\\_url,

\&nbsp;           customer.email, customer.phone\\\_number, customer.sensor\\\_location,

\&nbsp;           customer.sensor\\\_name, customer.notes

\&nbsp;       ])

\&nbsp;   response = HttpResponse(

\&nbsp;       content=output.getvalue(),

\&nbsp;       content\\\_type='text/csv',

\&nbsp;       headers={'Content-Disposition': 'attachment; filename=customers.csv'}

\&nbsp;   )

\&nbsp;   return response



@login\\\_required

def test\\\_rate\\\_limit(request):

\&nbsp;   if getattr(request, 'limited', False):

\&nbsp;       return HttpResponse("Rate limit exceeded", status=429)

\&nbsp;   return HttpResponse("Success")

```



\## Step 6: Set Up URLs

Replace `aqi\\\_project/urls.py` with:



```python

from django.contrib import admin

from django.urls import path

from aqi\\\_app import views



urlpatterns = \\\[

\&nbsp;   path('admin/', admin.site.urls),

\&nbsp;   path('login/', views.login\\\_view, name='login'),

\&nbsp;   path('logout/', views.logout\\\_view, name='logout'),

\&nbsp;   path('dashboard/', views.dashboard, name='dashboard'),

\&nbsp;   path('edit\\\_customer/<int:id>/', views.edit\\\_customer, name='edit\\\_customer'),

\&nbsp;   path('delete\\\_customer/<int:id>/', views.delete\\\_customer, name='delete\\\_customer'),

\&nbsp;   path('sensor-data/', views.sensor\\\_data, name='sensor\\\_data'),

\&nbsp;   path('download-customers/', views.download\\\_customers, name='download\\\_customers'),

\&nbsp;   path('test-rate-limit/', views.test\\\_rate\\\_limit, name='test\\\_rate\\\_limit'),

]

```



\## Step 7: Create Templates



in aqi\_projects/settings.py, add

```py

TEMPLATES = \\\[

\&nbsp;   {

\&nbsp;       'BACKEND': 'django.template.backends.django.DjangoTemplates',

\&nbsp;       'DIRS': \\\[BASE\\\_DIR / 'templates'],

\&nbsp;       'APP\\\_DIRS': True,

\&nbsp;       'OPTIONS': {

\&nbsp;           'context\\\_processors': \\\[

\&nbsp;               'django.template.context\\\_processors.debug',

\&nbsp;               'django.template.context\\\_processors.request',

\&nbsp;               'django.contrib.auth.context\\\_processors.auth',

\&nbsp;               'django.contrib.messages.context\\\_processors.messages',

\&nbsp;           ],

\&nbsp;       },

\&nbsp;   },

]

```



Create a `templates` folder at `C:\\\\Users\\\\User\\\\Desktop\\\\SMART AIR\\\\Code\\\\RGB Matrix\\\\ESP8266\\\\FINAL\\\\django\\\_second\\\\aqi\\\_project\\\\templates`.



1\. \*\*base.html\*\*:

   ```html

   {% load static %}

   <!DOCTYPE html>

   <html lang="en">

   <head>

       <meta charset="UTF-8">

       <meta name="viewport" content="width=device-width, initial-scale=1.0">

       <title>AQI Dashboard</title>

       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

       <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700\\\&display=swap" rel="stylesheet">

       <link rel="stylesheet" href="{% static 'css/styles.css' %}">

   </head>

   <body>

       <nav class="navbar navbar-expand-lg">

           <div class="container-fluid">

               <a class="navbar-brand" href="{% url 'dashboard' %}">AQI Dashboard</a>

               <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

                   <span class="navbar-toggler-icon"></span>

               </button>

               <div class="collapse navbar-collapse" id="navbarNav">

                   <ul class="navbar-nav ms-auto">

                       {% if user.is\_authenticated %}

                           <li class="nav-item">

                               <a class="nav-link" href="{% url 'logout' %}">Logout</a>

                           </li>

                       {% else %}

                           <li class="nav-item">

                               <a class="nav-link" href="{% url 'login' %}">Login</a>

                           </li>

                       {% endif %}

                   </ul>

               </div>

           </div>

       </nav>

       <div class="container">

           {% block content %}

           {% endblock %}

       </div>

       <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

   </body>

   </html>

   ```



2\. \*\*login.html\*\*:

   ```html

   {% extends 'base.html' %}

   {% block content %}

   <div class="row justify-content-center mt-5">

       <div class="col-md-6">

           <div class="card">

               <div class="card-body">

                   <h2 class="card-title text-center mb-4">Login to AQI Dashboard</h2>

                   {% if error %}

                       <p class="error-message text-center">{{ error }}</p>

                   {% endif %}

                   <form method="post">

                       {% csrf\_token %}

                       <div class="mb-3">

                           <label for="username" class="form-label">Username</label>

                           <input type="text" class="form-control" id="username" name="username" required>

                       </div>

                       <div class="mb-3">

                           <label for="password" class="form-label">Password</label>

                           <input type="password" class="form-control" id="password" name="password" required>

                       </div>

                       <div class="d-grid">

                           <button type="submit" class="btn btn-primary">Login</button>

                       </div>

                   </form>

               </div>

           </div>

       </div>

   </div>

   {% endblock %}

   ```



3\. \*\*dashboard.html\*\*:

   ```html

   {% extends 'base.html' %}

   {% block content %}

   <div class="mt-5">

       <h2 class="mb-4">Customer Dashboard</h2>

       <div class="card mb-4">

           <div class="card-body">

               <h3 class="card-title">Add New Customer</h3>

               <form method="post">

                   {% csrf\_token %}

                   <div class="row">

                       <div class="col-md-6 mb-3">

                           <label for="name" class="form-label">Name</label>

                           <input type="text" class="form-control" id="name" name="name" required>

                       </div>

                       <div class="col-md-6 mb-3">

                           <label for="api\\\_url" class="form-label">API URL</label>

                           <input type="text" class="form-control" id="api\\\_url" name="api\\\_url" required>

                       </div>

                   </div>

                   <div class="row">

                       <div class="col-md-6 mb-3">

                           <label for="email" class="form-label">Email</label>

                           <input type="email" class="form-control" id="email" name="email">

                       </div>

                       <div class="col-md-6 mb-3">

                           <label for="phone\\\_number" class="form-label">Phone Number</label>

                           <input type="text" class="form-control" id="phone\\\_number" name="phone\\\_number">

                       </div>

                   </div>

                   <div class="mb-3">

                       <label for="sensor\\\_location" class="form-label">Sensor Location</label>

                       <input type="text" class="form-control" id="sensor\\\_location" name="sensor\\\_location">

                   </div>

                   <div class="mb-3">

                       <label for="notes" class="form-label">Notes</label>

                       <textarea class="form-control" id="notes" name="notes" rows="4"></textarea>

                   </div>

                   <div class="d-grid">

                       <button type="submit" class="btn btn-primary">Add Customer</button>

                   </div>

               </form>

               {% if new\_password %}

                   <p class="success-message mt-3">New Customer Password: {{ new\_password }}</p>

               {% endif %}

           </div>

       </div>

       <h3 class="mb-3">Customers</h3>

       <div class="table-responsive">

           <table class="table table-striped">

               <thead>

                   <tr>

                       <th>ID</th>

                       <th>Name</th>

                       <th>Password</th>

                       <th>API URL</th>

                       <th>Email</th>

                       <th>Phone Number</th>

                       <th>Sensor Location</th>

                       <th>Sensor Name</th>

                       <th>Notes</th>

                       <th>Actions</th>

                   </tr>

               </thead>

               <tbody>

                   {% for customer in customers %}

                   <tr>

                       <td>{{ customer.id }}</td>

                       <td>{{ customer.name }}</td>

                       <td>{{ customer.password }}</td>

                       <td>{{ customer.api\_url }}</td>

                       <td>{{ customer.email }}</td>

                       <td>{{ customer.phone\_number }}</td>

                       <td>{{ customer.sensor\_location }}</td>

                       <td>{{ customer.sensor\_name }}</td>

                       <td>{{ customer.notes }}</td>

                       <td>

                           <a href="{% url 'edit\\\_customer' customer.id %}" class="btn btn-primary btn-sm">Update</a>

                           <a href="{% url 'delete\\\_customer' customer.id %}" class="btn btn-danger btn-sm" onclick="return confirm('Are you sure you want to delete this customer?')">Delete</a>

                       </td>

                   </tr>

                   {% endfor %}

               </tbody>

           </table>

       </div>

       <a href="{% url 'download\\\_customers' %}" class="btn btn-primary mt-3">Download Customers CSV</a>

   </div>

   {% endblock %}

   ```



4\. \*\*edit\_customer.html\*\*:

   ```html

   {% extends 'base.html' %}

   {% block content %}

   <div class="row justify-content-center mt-5">

       <div class="col-md-6">

           <div class="card">

               <div class="card-body">

                   <h2 class="card-title text-center mb-4">Edit Customer</h2>

                   <form method="post" action="{% url 'edit\\\_customer' customer.id %}">

                       {% csrf\_token %}

                       <div class="mb-3">

                           <label for="name" class="form-label">Name</label>

                           <input type="text" class="form-control" id="name" name="name" value="{{ customer.name }}" required>

                       </div>

                       <div class="mb-3">

                           <label for="api\\\_url" class="form-label">API URL</label>

                           <input type="text" class="form-control" id="api\\\_url" name="api\\\_url" value="{{ customer.api\\\_url }}" required>

                       </div>

                       <div class="mb-3">

                           <label for="email" class="form-label">Email</label>

                           <input type="email" class="form-control" id="email" name="email" value="{{ customer.email }}">

                       </div>

                       <div class="mb-3">

                           <label for="phone\\\_number" class="form-label">Phone Number</label>

                           <input type="text" class="form-control" id="phone\\\_number" name="phone\\\_number" value="{{ customer.phone\\\_number }}">

                       </div>

                       <div class="mb-3">

                           <label for="sensor\\\_location" class="form-label">Sensor Location</label>

                           <input type="text" class="form-control" id="sensor\\\_location" name="sensor\\\_location" value="{{ customer.sensor\\\_location }}">

                       </div>

                       <div class="mb-3">

                           <label for="notes" class="form-label">Notes</label>

                           <textarea class="form-control" id="notes" name="notes" rows="4">{{ customer.notes }}</textarea>

                       </div>

                       <div class="d-grid gap-2">

                           <button type="submit" class="btn btn-primary">Update Customer</button>

                           <a href="{% url 'dashboard' %}" class="btn btn-secondary">Cancel</a>

                       </div>

                   </form>

               </div>

           </div>

       </div>

   </div>

   {% endblock %}

   ```



\## Step 8: Set Up Static Files

1\. \*\*Create Static Folder\*\*:

   Create `C:\\\\Users\\\\User\\\\Desktop\\\\SMART AIR\\\\Code\\\\RGB Matrix\\\\ESP8266\\\\FINAL\\\\django\\\_second\\\\aqi\\\_project\\\\static\\\\css`.



2\. \*\*Add `styles.css`\*\*:

   Create `static/css/styles.css`:



   ```css

   body {

       font-family: 'Roboto', sans-serif;

       background-color: #f0f4f8;

       color: #333;

   }



   .navbar {

       background-color: #007bff;

       box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

   }



   .navbar-brand, .nav-link {

       color: #fff !important;

   }



   .container {

       max-width: 1200px;

       margin-top: 20px;

   }



   .card {

       border: none;

       border-radius: 10px;

       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

       transition: transform 0.2s;

   }



   .card:hover {

       transform: translateY(-5px);

   }



   .form-control {

       border-radius: 5px;

       margin-bottom: 15px;

   }



   .btn-primary {

       background-color: #007bff;

       border: none;

       border-radius: 5px;

       padding: 10px 20px;

       transition: background-color 0.3s;

   }



   .btn-primary:hover {

       background-color: #0056b3;

   }



   .btn-danger {

       border-radius: 5px;

   }



   table {

       width: 100%;

       border-collapse: separate;

       border-spacing: 0;

       border-radius: 10px;

       overflow: hidden;

       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

   }



   th, td {

       padding: 12px;

       text-align: left;

   }



   th {

       background-color: #007bff;

       color: #fff;

   }



   tr:nth-child(even) {

       background-color: #f8f9fa;

   }



   .error-message {

       color: #dc3545;

       font-weight: bold;

   }



   .success-message {

       color: #28a745;

       font-weight: bold;

   }



   @media (max-width: 768px) {

       .form-control, .btn {

           font-size: 0.9rem;

       }

       table {

           font-size: 0.85rem;

       }

   }

   ```



3\. \*\*Test Static Files\*\*:

   ```bash

   python manage.py collectstatic --dry-run

   ```



   Ensure `css/styles.css` appears in the output.



\### Step 9: FINAL File Structure

└── aqi\_project/

    ├── aqi\_app/

    │   ├── migrations/

    │   │   ├── \_\_init\_\_.py

    │   │   └── (migration files, e.g., 0001\_initial.py)

    │   ├── \_\_init\_\_.py

    │   ├── admin.py

    │   ├── apps.py

    │   ├── models.py

    │   ├── tests.py

    │   ├── utils.py

    │   ├── views.py

    ├── static/

    │   ├── css/

    │   │   ├── styles.css

    ├── templates/

    │   ├── base.html

    │   ├── dashboard.html

    │   ├── edit\_customer.html

    │   ├── login.html

    ├── staticfiles/ (created after collectstatic, for production)

    ├── db.sqlite3

    ├── manage.py

    ├── aqi\_project/

    │   ├── \_\_init\_\_.py

    │   ├── settings.py

    │   ├── urls.py

    │   ├── wsgi.py

    ├── .env



\## Step 10: Test the Application

1\. \*\*Run the Server\*\*:

   ```bash

   python manage.py runserver

   ```



2\. \*\*Test Features\*\*:

   - \*\*Login\*\*: Visit `http://127.0.0.1:8000/login/`. Log in with the superuser credentials.

   - \*\*Dashboard\*\*: Go to `http://127.0.0.1:8000/dashboard/`. Add a customer, verify the generated password appears.

   - \*\*Edit Customer\*\*: Click "Update" for a customer, edit fields, and submit. Confirm changes in the dashboard.

   - \*\*Delete Customer\*\*: Click "Delete" and confirm the prompt works.

   - \*\*Sensor Data\*\*: Test with:

     ```bash

     for i in {1..6}; do curl -s "http://127.0.0.1:8000/sensor-data/?customer\_password=your\_password" \& done; wait

     ```

     Expect 5 successes and a 429 error on the 6th request.

   - \*\*CSV Download\*\*: Click "Download Customers CSV" to verify the file downloads.

   - \*\*UI\*\*: Ensure the navbar, forms, and table are styled (blue buttons, responsive layout).



3\. \*\*Test Admin\*\*:

   Visit `http://127.0.0.1:8000/admin/` to manage customers via Django’s admin interface.



\## Step 10: Production Setup

1\. \*\*Set Environment Variables\*\*:

   Create `.env` at `C:\\\\Users\\\\User\\\\Desktop\\\\SMART AIR\\\\Code\\\\RGB Matrix\\\\ESP8266\\\\FINAL\\\\django\\\_second\\\\aqi\\\_project`:

   ```

   SECRET\_KEY=your-super-secret-key-here

   ```



2\. \*\*Update `settings.py`\*\*:

   ```python

   DEBUG = False

   ALLOWED\_HOSTS = \['your-domain.com', '127.0.0.1', 'localhost']

   ```



3\. \*\*Collect Static Files\*\*:

   ```bash

   python manage.py collectstatic

   ```



4\. \*\*Deploy with Gunicorn and Nginx\*\*:

   - Install Gunicorn:

     ```bash

     pip install gunicorn

     ```

   - Run Gunicorn:

     ```bash

     gunicorn --bind 0.0.0.0:8000 aqi\_project.wsgi

     ```

   - Configure Nginx to serve `staticfiles/` and proxy to Gunicorn (see Nginx documentation).



\## Step 11: Troubleshooting

\- \*\*Template Errors\*\*: Ensure `{% load static %}` is at the top of templates using static files.

\- \*\*Rate Limiting Fails\*\*: Verify `CACHES` in `settings.py` and run `createcachetable`.

\- \*\*ModuleNotFoundError\*\*: Check `pip show django-ratelimit python-decouple`. Reinstall if needed:

  ```bash

  pip install django-ratelimit python-decouple --force-reinstall

  ```

\- \*\*Static Files Not Loading\*\*: Confirm `STATICFILES\\\_DIRS` and `DEBUG = True` for development.

\- \*\*Database Issues\*\*: Run `python manage.py migrate` to apply migrations.



\## Project Structure

After setup, your directory should look like:



```

C:\\\\Users\\\\User\\\\Desktop\\\\SMART AIR\\\\Code\\\\RGB Matrix\\\\ESP8266\\\\FINAL\\\\django\\\_second\\\\

└── aqi\\\_project/

\&nbsp;   ├── aqi\\\_app/

\&nbsp;   │   ├── migrations/

\&nbsp;   │   ├── \\\_\\\_init\\\_\\\_.py

\&nbsp;   │   ├── admin.py

\&nbsp;   │   ├── apps.py

\&nbsp;   │   ├── models.py

\&nbsp;   │   ├── tests.py

\&nbsp;   │   ├── utils.py

\&nbsp;   │   ├── views.py

\&nbsp;   ├── static/

\&nbsp;   │   ├── css/

\&nbsp;   │   │   ├── styles.css

\&nbsp;   ├── templates/

\&nbsp;   │   ├── base.html

\&nbsp;   │   ├── login.html

\&nbsp;   │   ├── dashboard.html

\&nbsp;   │   ├── edit\\\_customer.html

\&nbsp;   ├── db.sqlite3

\&nbsp;   ├── manage.py

\&nbsp;   ├── aqi\\\_project/

\&nbsp;   │   ├── \\\_\\\_init\\\_\\\_.py

\&nbsp;   │   ├── settings.py

\&nbsp;   │   ├── urls.py

\&nbsp;   │   ├── wsgi.py

\&nbsp;   ├── .env

```



\## Summary

This tutorial sets up a Django AQI Dashboard with user authentication, customer management, AQI data API, and CSV exports. It uses SQLite for simplicity, `django-ratelimit` for rate limiting (15/min for login, 5/min for sensor data), and Bootstrap 5 for a beautiful, responsive UI. Save this guide for future reference, and test all features to ensure they work as expected. If you encounter issues, revisit the troubleshooting section or share error details for further assistance.



---



Let me know if you need additional features (e.g., more advanced AQI calculations, additional UI tweaks) or help with deployment!

