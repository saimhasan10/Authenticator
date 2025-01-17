
from django.urls import path
from .views import UserRegistrationView, UserLoginView, user_logout, UserAccountUpdateView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(), name='register'),
    path('login/',UserLoginView.as_view(), name='login'),
    path('logout/',user_logout, name='logout'),
    path('profile/',UserAccountUpdateView.as_view(), name='profile'),
]
