from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('apply/', views.apply_view, name='apply'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]
