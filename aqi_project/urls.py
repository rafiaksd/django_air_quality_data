from django.contrib import admin
from django.urls import path
from aqi_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_customer/<int:id>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:id>/', views.delete_customer, name='delete_customer'),
    path('sensor-data/', views.sensor_data, name='sensor_data'),
    path('download-customers/', views.download_customers, name='download_customers'),
    path('test-rate-limit/', views.test_rate_limit, name='test_rate_limit'),
]
