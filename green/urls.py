from django.urls import path
from .views import RegisterUserView, LoginView
from . import views

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', views.login_view, name = 'account'),
    path('dash/', views.dash_view, name = 'dash'),
]
