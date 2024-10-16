# events/views.py

from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Event, Attendance
from .serializers import UserSerializer, EventSerializer, AttendanceSerializer
from django.contrib.auth.models import User
from rest_framework import generics, permissions, filters
from django_filters import rest_framework as django_filters
from .models import Event
from .serializers import EventSerializer
from rest_framework import generics, permissions, status
from django.utils import timezone
from rest_framework.response import Response
from django.db import IntegrityError

# User registration view
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    date_time = django_filters.DateTimeFromToRangeFilter(field_name='date_time')

    class Meta:
        model = Event
        fields = ['title', 'location', 'date_time']
# Event CRUD views
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = EventFilter
    ordering_fields = '__all__'
    ordering = ['date_time']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            event = super().get_object()
            if event.organizer != self.request.user:
                raise PermissionError("You do not have permission to manage this event.")
            return event
        except Event.DoesNotExist:
            raise NotFound("Event not found.")
    
    def update(self, request, *args, **kwargs):
        event = self.get_object()  # This will raise 404 if not found
        serializer = self.get_serializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()  # This will  raise 404 if not found
        self.perform_destroy(event)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Attendance views
class AttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            # Handle the case where the user is already registered for the event
            return Response(
                {"detail": "You are already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST
            )
        event_id = self.request.data.get('event')
        event = Event.objects.get(id=event_id)
        current_attendance_count = Attendance.objects.filter(event=event).count()
        
        if current_attendance_count >= event.capacity:
            raise serializers.ValidationError(f"This event has reached its maximum capacity.", status=status.HTTP_400_BAD_REQUEST)
                
            
        
        return Response({"message": f"Successfull Registered for the event"}, status=200)
    

class AttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendance.objects.filter(user=self.request.user)

class UpcomingEventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    date_time = django_filters.DateTimeFromToRangeFilter(field_name='date_time')

    class Meta:
        model = Event
        fields = ['title', 'location', 'date_time']

class UpcomingEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = UpcomingEventFilter

    def get_queryset(self):
        # Only return upcoming events
        return Event.objects.filter(date_time__gte=timezone.now()).order_by('date_time')