from django.db import models
from django.contrib.auth.models import User

class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100)
    application_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    membership_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='basic')

    def __str__(self):
        return f"{self.user.username} - {self.membership_type}"

