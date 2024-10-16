from django.conf import settings
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if not self.title:
            raise ValidationError('Title is required.')
        if not self.date_time:
            raise ValidationError('Date and Time is required.')
        if not self.location:
            raise ValidationError('Location is required.')
        if self.date_time < timezone.now():
            raise ValidationError('Event date and time must be in the future.')

    def __str__(self):
        return self.title

    def current_attendance(self):
        return self.attendance_set.count()

class Attendance(models.Model):
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user} attending {self.event}"
