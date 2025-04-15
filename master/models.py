from django.db import models

# Create your models here.

class Email(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    body_preview = models.TextField()
    date_received = models.DateTimeField()

    def __str__(self):
        return self.id
