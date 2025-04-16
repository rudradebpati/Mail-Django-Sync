from django.urls import path
from .views import *

urlpatterns = [
    path('fetch_new_emails/', FetchEmailView.as_view(), name='email_storage'),
    
]
