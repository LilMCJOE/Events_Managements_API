from django.urls import path
from .views import (
    UserRegistrationView,
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    AttendanceCreateView,
    UpcomingEventListView,
    AttendanceListView,
    TokenObtainPairView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('attendances/', AttendanceCreateView.as_view(), name='attendance-create'),
    path('my-attendances/', AttendanceListView.as_view(), name='my-attendances'),
    path('upcoming-events/', UpcomingEventListView.as_view(), name='upcoming-events'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
