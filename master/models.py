from django.db import models

# Create your models here.

class EmailStorage(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    body_preview = models.TextField()
    date_received = models.DateTimeField()

    def __str__(self):
        return self.id
    class Meta:
        db_table='email_storage'
        ordering = ['-date_received']
        verbose_name = 'Email Storage'
        verbose_name_plural = 'Emails Storage'