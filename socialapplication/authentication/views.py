from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, generics
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from .serializer import *
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes,throttle_classes
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication, TokenAuthentication


# Create your views here.
class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: 'Successful response',
            400: 'Bad request',
            401: 'Unauthorized',
            # Add other response codes and descriptions as needed
        }
    )
    def post(self, request):
        
        payload = request.data
        hashed_password = make_password(
            payload['password'])  # Hash the password

        # Update the payload with the hashed password
        payload['password'] = hashed_password

        serializer = UserSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        # Custom validation logic
        email = serializer.validated_data['email']
        if get_user_model().objects.filter(email=email).exists():
            return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # If validation passes, save the user
        user = serializer.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: 'Successful response',
            400: 'Bad request',
            401: 'Unauthorized',
            # Add other response codes and descriptions as needed
        }
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request=self.request,
                            email=email, password=password)

        if user is None:
            return Response({'error': 'No account found for this user.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

        is_active = user.is_active
        if not is_active:
            return Response({'error': 'User account is deactivated'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    


    


class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
  

    @swagger_auto_schema(
        request_body=ProfileSerializer,  # Provide the appropriate serializer class
        responses={
            200: 'Successful response',
            400: 'Bad request',
            401: 'Unauthorized',
            # Add other response codes and descriptions as needed
        }
    )
    def post(self, request):
        try:
            user = request.user
            userobj = User.objects.get(id=user.id)

            # Exclude email and username fields
            excluded_fields = ['email', 'username']

            # Create a dictionary for the fields to update
            payload = {field: value for field, value in request.data.items() if field not in excluded_fields}

            ser = ProfileSerializer(userobj, data=payload, partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()

            data = {
                'user': ser.data,
                'message': 'Updated profile successfully'
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class GetProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
  
    @swagger_auto_schema(
        responses={
            200: 'Successful response',
            400: 'Bad request',
            401: 'Unauthorized',
            # Add other response codes and descriptions as needed
        }
    )
    def get(self, request):
        try:
            user = request.user
            userobj = User.objects.get(id=user.id)
            ser = UserSerializer(userobj)
            
            data = {
                'user': ser.data
            }

            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

