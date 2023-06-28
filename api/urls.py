from django.urls import path
from .views import index, register_user, check_user, get_users, logOut, toggle_subscriptions

urlpatterns = [
    path('', index),
    path('register', register_user, name='register'),
    path('login', check_user, name='login'),
    path('user', get_users, name='user'),
    path('logout', logOut, name='logout'),
    path('toggle-subscription/<int:id>/', toggle_subscriptions,
         name='toggle-subscription'
         ),
]
