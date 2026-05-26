from django.shortcuts import render

# Create your views here.


from rest_framework import generics,permissions
from .models import Student,Event,Registration
from .serializers import StudentSerializer,EventSerializer,RegistrationSerializer

#view all users
class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

#view specific user details
class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

#view all events
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

#view single event details
class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

# #register for an event   
# class RegistrationCreateView(generics.CreateAPIView):
#     queryset = Registration.objects.all()
#     serializer_class = RegistrationSerializer
    
# #view all registrations
# class RegistrationListView(generics.ListAPIView):
#     queryset = Registration.objects.all()
#     serializer_class = RegistrationSerializer
    
# #cancel registration 
# class RegistrationDeleteView(generics.DestroyAPIView):
#     queryset = Registration.objects.all()
#     serializer_class = RegistrationSerializer

# REGISTER FOR EVENT
class RegistrationCreateView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# VIEW MY REGISTRATIONS
class RegistrationListView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)


# CANCEL MY REGISTRATION
class RegistrationDeleteView(generics.DestroyAPIView):
    serializer_class = RegistrationSerializer
    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)