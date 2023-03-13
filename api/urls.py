from django.urls import path
from .views import index, registerUser, checkUser, getUsers, logOut, toggleSubscriptions

urlpatterns = [
    path('', index),
    path('register', registerUser),
    path('login', checkUser),
    path('user', getUsers),
    path('logout', logOut),
    path('toggle-subscription/<int:id>/', toggleSubscriptions),
]
