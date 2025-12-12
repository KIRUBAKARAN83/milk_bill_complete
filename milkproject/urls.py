from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts app URLs (only once)
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # Auth views
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Optionally, set your homepage to accounts views
    # path('', include(('accounts.urls', 'accounts'), namespace='home')),  # use a different namespace if needed
]
