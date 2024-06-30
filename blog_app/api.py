import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer, BlogPostSerializer
from django.contrib.auth import authenticate
from .utils import validate_user_data
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework import generics
from .models import BlogPost
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        logger.debug(f"Received signup data: {data}")

        if not data:
            logger.error("Signup failed: No data provided.")
            return Response({"details": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

        validation_error = validate_user_data(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            confirm_password=data.get('confirm_password')
        )

        if validation_error:
            logger.error(f"Signup failed: {validation_error}")
            return Response({"details": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = serializer.instance
                token, created = Token.objects.get_or_create(user=user)
                logger.info(f"User {user.username} signed up successfully.")
                return Response({"user": serializer.data, "token": token.key}, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Signup failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"An error occurred during signup: {str(e)}")
            return Response({f"details": "An error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class LoginAPIView(APIView):
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST'))
    def post(self, request, format=None):
        data = request.data
        logger.debug(f"Received signup data: {data}")

        if not data:
            logger.error("Signup failed: No data provided.")
            return Response({"details": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        username = data.get('username')
        password = data.get('password')

        try:
            if not User.objects.filter(username=username).exists():
                logger.error("Login failed: Username does not exist.")
                return Response({"details": "Username does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(username=username, password=password)
            if user:
                serializer = UserSerializer(user)
                token, created = Token.objects.get_or_create(user=user)
                logger.info(f"User {user.username} logged in successfully.")
                return Response({"user": serializer.data, "token": token.key}, status=status.HTTP_200_OK)
            else:
                logger.error("Login failed: Incorrect password.")
                return Response({"details": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"An error occurred during login: {str(e)}")
            return Response({"details": f"An error occurred during login: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def post(self, request, format=None):
        try:
            token = request.auth
            if token:
                token.delete()
                logger.info(f"User {request.user.username} logged out successfully.")
                return Response({"details": "Logged out successfully."}, status=status.HTTP_200_OK)
            else:
                logger.error("Logout failed: No token found.")
                return Response({"details": "No token found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"An error occurred during logout.{str(e)}")
            return Response({"details": "An error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BlogPostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000
    
class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-id')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    pagination_class = BlogPostPagination

class BlogPostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

class BlogPostUpdateView(generics.UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

class BlogPostDeleteView(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]