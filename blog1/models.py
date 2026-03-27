from django.db import models

# A simple User model to store the sign-up information
class Signup(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255)  # Use hashed password
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.username
