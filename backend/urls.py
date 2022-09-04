from django.urls import path
from . import views

app_name = "backend"

urlpatterns = [
    path('', views.index, name="index"),
    path('otp/', views.OTPView, name="OTPView"),
    path('users/register', views.RegisterView.as_view(), name="register"),
    path('users/login', views.LoginView.as_view(), name="login"),
    path('sessions/create', views.SessionView.as_view(), name="session"),
    path('message/send', views.MessageView.as_view(), name="message"),
    path('messages/<str:topic>', views.viewMessages.as_view(), name="room"),
]
