from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from management import views as management_views

urlpatterns = [
    path('', management_views.home_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('management/', include('management.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]