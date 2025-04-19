from django.urls import path
from .views import RegisterStep1View, RegisterStep2View, RegisterStep3View, LoginView
from . import views

urlpatterns = [
    path('register/step1/', RegisterStep1View.as_view(), name='register_step1'),
    path('register/step2/', RegisterStep2View.as_view(), name='register_step2'),
    path('register/step3/', RegisterStep3View.as_view(), name='register_step3'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', views.login_view, name = 'account'),
    path('dash/', views.dash_view, name = 'dash'),
]
