from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import UserDetails
from django.conf import settings
import base_service as base_s


class APIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication class to authenticate UserDetailss using API key.
    """
    def authenticate(self, request):
        # Get the API key from the request headers
        api_key = request.headers.get('X_API_KEY')
        
        if api_key:
            admin_user=self.verify_api_key(api_key)
        return (admin_user, None)
    
    def verify_api_key(self, api_key):
        # Implement your logic to retrieve the UserDetails based on the API key
        hashed_api_key=base_s.hash_sha256(api_key)
        if hashed_api_key!= settings.API_KEY:
            raise AuthenticationFailed('Invalid API key')
        return UserDetails.objects.get(id=1)