from django.urls import path
from .views import index, registerUser, checkUser, getUsers, logOut, toggleSubscriptions

urlpatterns = [
    path('', index),
    path('register', registerUser, name='register'),
    path('login', checkUser, name='login'),
    path('user', getUsers, name='user'),
    path('logout', logOut, name='logout'),
    path('toggle-subscription/<int:id>/', toggleSubscriptions,
         name='toggle-subscription'
         ),
]
