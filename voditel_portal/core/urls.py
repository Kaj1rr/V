from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_application, name='create_application'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('logout/', views.logout_view, name='logout'),
]