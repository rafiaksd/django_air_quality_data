import secrets
import string
import csv
from io import StringIO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django_ratelimit.decorators import ratelimit

from .models import Customer
from .utils import (
    pm25_to_aqi,
    aqi_to_cigars_per_day,
    aqi_to_health_label,
    get_sensor_type_from_url,
    extract_pm25_from_url,
)

def generate_alphanum(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@ratelimit(key='ip', rate='15/m', method='POST')
def login_view(request):
    if getattr(request, 'limited', False):
        return render(request, 'login.html', {'error': 'Rate limit exceeded. Try again later.'}, status=429)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    password_plain = None
    if request.method == 'POST':
        name = request.POST.get('name')
        api_url = request.POST.get('api_url')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        sensor_location = request.POST.get('sensor_location')
        notes = request.POST.get('notes')
        password_plain = generate_alphanum()
        sensor_name = get_sensor_type_from_url(api_url)

        customer = Customer(
            name=name,
            password=password_plain,
            api_url=api_url,
            email=email,
            phone_number=phone_number,
            sensor_location=sensor_location,
            notes=notes,
            sensor_name=sensor_name
        )
        customer.save()

    customers = Customer.objects.all()
    return render(request, 'dashboard.html', {'customers': customers, 'new_password': password_plain})

@login_required
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        customer.name = request.POST.get('name', customer.name)
        new_api_url = request.POST.get('api_url', customer.api_url)
        customer.email = request.POST.get('email', customer.email)
        customer.phone_number = request.POST.get('phone_number', customer.phone_number)
        customer.sensor_location = request.POST.get('sensor_location', customer.sensor_location)
        customer.notes = request.POST.get('notes', customer.notes)

        if new_api_url != customer.api_url:
            customer.api_url = new_api_url
            customer.sensor_name = get_sensor_type_from_url(new_api_url)

        customer.save()
        return redirect('dashboard')

    return render(request, 'edit_customer.html', {'customer': customer})

@login_required
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('dashboard')

@ratelimit(key='ip', rate='5/m')
def sensor_data(request):
    if getattr(request, 'limited', False):
        return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)

    customer_password = request.GET.get('customer_password')
    if not customer_password:
        return JsonResponse({'aqi': -3})

    customer = Customer.objects.filter(password=customer_password).first()
    if not customer:
        return JsonResponse({'aqi': -2})

    pm25 = extract_pm25_from_url(customer.api_url)
    if pm25 is None or pm25 < 0:
        return JsonResponse({'aqi': -1})

    aqi = pm25_to_aqi(pm25)
    if aqi == 0:
        aqi = 1

    cigars = aqi_to_cigars_per_day(aqi)
    health_label = aqi_to_health_label(aqi)
    sensor_name = customer.sensor_name or get_sensor_type_from_url(customer.api_url)

    return JsonResponse({
        'customer_id': customer.id,
        'aqi': aqi,
        'sensor_name': sensor_name,
        'cigars': cigars,
        'health_label': health_label,
    })

@login_required
def download_customers(request):
    customers = Customer.objects.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Customer ID', 'Name', 'Password', 'API URL', 'Email', 'Phone Number', 'Sensor Location', 'Sensor Name', 'Notes'])

    for customer in customers:
        writer.writerow([
            customer.id,
            customer.name,
            customer.password,
            customer.api_url,
            customer.email,
            customer.phone_number,
            customer.sensor_location,
            customer.sensor_name,
            customer.notes
        ])

    response = HttpResponse(
        content=output.getvalue(),
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=customers.csv'}
    )
    return response

@login_required
def test_rate_limit(request):
    if getattr(request, 'limited', False):
        return HttpResponse("Rate limit exceeded", status=429)
    return HttpResponse("Success")
