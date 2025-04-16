from django.shortcuts import render
from master.models import EmailStorage
from rest_framework.views import APIView
import master_service as service
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from imap_mail_fetch.middleware import APIKeyAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class FetchEmailView(APIView):
    authentication_classes=[APIKeyAuthentication]
    permission_classes=[IsAuthenticated]
    """    Fetches emails from the email server and stores them in the database.
    """
    def get(self, request, *args, **kwargs):
        try:
            all_mail_data_list=service.fetch_emails()
            with transaction.atomic():
                for each_dict in all_mail_data_list: 
                    EmailStorage.objects.create(
                        subject=each_dict['subject'],
                        sender=each_dict['sender'],
                        body=each_dict['body'],
                        date_received=each_dict['date_received']
                    )
        except Exception as e:
            raise e 
        return Response({"status":status.HTTP_200_OK,"msg":"Emails fetched successfully"}, status=status.HTTP_200_OK)       
