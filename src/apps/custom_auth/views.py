from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class UserInfoView(APIView):
    """
    View to retrieve user information
    """
    authentication_classes = [BasicAuthentication]
    
    def get(self, request):
        """
        Return user information for authenticated user
        """
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
        })


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    View to handle login via Basic Auth
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle login with username and password
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Attempt to authenticate the user
        user = authenticate(username=username, password=password)
        
        if user:
            # User exists and credentials are correct
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
            })
        else:
            # Invalid credentials
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )