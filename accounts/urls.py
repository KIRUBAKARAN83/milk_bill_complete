from django.urls import path
from . import views
from . import api_views

app_name = 'accounts'

urlpatterns = [
    # WEB
    path('', views.home, name='home'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('entry/add/', views.add_entry, name='add_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('customers/<int:customer_id>/chart/', views.chart_data, name='chart_data'),
    path('customers/<int:customer_id>/bill/', views.bill_pdf, name='bill_pdf'),

    # API
    path('api/entries/', api_views.create_entry, name='api_create_entry'),
    path('api/entries/<int:entry_id>/', api_views.delete_entry, name='api_delete_entry'),
]
