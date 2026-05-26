from django.urls import path
from .views import(
    StudentDetailView,
    StudentListView,
    EventListView,
    EventDetailView,
    RegistrationCreateView,
    RegistrationListView,
    RegistrationDeleteView,
)

urlpatterns = [
    path('Student/',StudentListView.as_view()),
    path('Student/<int:pk>/',StudentDetailView.as_view()),
    path('events/',EventListView.as_view()),
    path('events/<int:pk>/',EventDetailView.as_view()),
    path('register/',RegistrationCreateView.as_view()),
    path('registrations/',RegistrationListView.as_view()),
    path('cancel/<int:pk>/',RegistrationDeleteView.as_view()),
]