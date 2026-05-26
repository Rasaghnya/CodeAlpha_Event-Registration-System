from django.urls import path
from .views import home, event_detail, signup, register_event, cancel_registration, my_registrations
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register_event/<int:pk>/', register_event, name='register_event'),
    path('registrations/', my_registrations, name='my_registrations'),
    path('registrations/cancel/<int:pk>/', cancel_registration, name='cancel_registration'),
]
