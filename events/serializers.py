from rest_framework import serializers
from .models import Event, Attendance
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_time', 'location', 'capacity', 'organizer', 'created_at']
        read_only_fields = ['organizer', 'created_at']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['event', 'user']
        read_only_fields = ('user',)

        def validate(self, attrs):
            event = attrs.get('event')
            if event.current_attendance() >= event.capacity:
                raise serializers.ValidationError(f"This event has reached its maximum capacity.")
            return attrs

            if Attendance.objects.filter(user=user, event=event).exists():
                raise serializers.ValidationError(f"You are already registered for this event.")
            return attrs
