from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (('ops', 'Ops'), ('client', 'Client'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)  # For email verification

class FileUpload(models.Model):
    FILE_TYPE_CHOICES = (
        ('pptx', 'PowerPoint'),
        ('docx', 'Word'),
        ('xlsx', 'Excel'),
    )
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey('User', on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    upload_time = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=255)

    def __str__(self):
        return self.original_filename
