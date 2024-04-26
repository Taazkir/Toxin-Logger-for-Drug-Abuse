from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('intake/', views.add_drug_intake, name='intake'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html', next_page='home'), name='logout'),
    path('get-updated-bac/', views.get_updated_bac, name='get_updated_bac'),


]