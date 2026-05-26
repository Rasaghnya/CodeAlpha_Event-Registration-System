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


# --- Simple frontend views (templates) ---
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    """Render homepage with list of events."""
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})

def event_detail(request, pk):
    """Render single event detail page."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})


def signup(request):
    """Simple signup view that creates a User and associated Student."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact_no = request.POST.get('contact_no')
        age = request.POST.get('age')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Student.objects.create(user=user, username=username, email=email, contact_no=contact_no, age=age)
            login(request, user)
            messages.success(request, 'Account created and logged in')
            return render(request, 'index.html', {'events': Event.objects.all()})
    return render(request, 'signup.html')


@login_required
def register_event(request, pk):
    """Register the logged-in user for event `pk` (simple, no capacity checks)."""
    event = get_object_or_404(Event, pk=pk)
    # Prevent duplicate registrations
    reg, created = Registration.objects.get_or_create(user=request.user, event=event)
    if created:
        messages.success(request, 'Registered for event')
    else:
        messages.info(request, 'You are already registered for this event')
    return render(request, 'event_detail.html', {'event': event})


@login_required
def cancel_registration(request, pk):
    """Cancel a registration by its id (pk)."""
    reg = get_object_or_404(Registration, pk=pk, user=request.user)
    reg.delete()
    messages.success(request, 'Registration cancelled')
    return render(request, 'registrations.html', {'registrations': Registration.objects.filter(user=request.user)})


@login_required
def my_registrations(request):
    regs = Registration.objects.filter(user=request.user).select_related('event')
    return render(request, 'registrations.html', {'registrations': regs})