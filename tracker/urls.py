from django.urls import path

from . import views
from .views import RegisterView

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]