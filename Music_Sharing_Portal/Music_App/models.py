from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email



class Song(models.Model):
    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected'),
    )
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()  # duration in seconds
    mp3_file = models.FileField(upload_to='uploads/')
    cover_image = models.ImageField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')

    def __str__(self):
        return self.name


class ProtectedSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.song.name} (Shared by: {self.shared_by.username})"
    
    def is_protected(self):
        return hasattr(self, 'protectedsong')
    
class ProtectedPlayList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.CharField(max_length=255)

class PrivatePlayList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.CharField(max_length=255)

# class PrivatePlayList(models.Model):
#     PRIVACY_CHOICES = (
#         ('public', 'Public'),
#         ('private', 'Private'),
#         ('protected', 'Protected'),
#     )
#     name = models.CharField(max_length=255)
#     artist = models.CharField(max_length=255)
#     duration = models.PositiveIntegerField()  # duration in seconds
#     mp3_file = models.FileField(upload_to='uploads/')
#     cover_image = models.ImageField(upload_to='uploads/')
#     uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='protected')
#     allowed_emails = models.TextField(blank=True, validators=[validate_email], default='Enter comma-separated email addresses.')
#     shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_songs')


class ShareRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)