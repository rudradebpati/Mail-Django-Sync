from django.shortcuts import render
from master.models import Email
from rest_framework.views import APIView
import master_service as service
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class FetchEmailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            all_mail_data_list=service.fetch_emails()
            with transaction.atomic():
                for each_dict in all_mail_data_list: 
                    Email.objects.create(
                        subject=each_dict['subject'],
                        sender=each_dict['sender'],
                        body=each_dict['body'],
                        date_received=each_dict['date_received']
                    )
        except Exception as e:
            raise e 
        return Response({"status":status.HTTP_200_OK,"message":"Emails fetched successfully"})       
