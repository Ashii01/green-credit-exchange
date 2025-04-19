from django.shortcuts import render
from rest_framework import generics
from .models import PartialUser, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from .serializers import RegisterStep1Serializer, RegisterStep2Serializer, RegisterStep3Serializer, LoginSerializer

class RegisterStep1View(APIView):
    def post(self, request):
        serializer = RegisterStep1Serializer(data=request.data)
        
        if serializer.is_valid():
            partial = serializer.save()
            return Response({"session_id": str(partial.session_id)}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterStep2View(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        
        try:
            partial = PartialUser.objects.get(session_id=session_id)
        except PartialUser.DoesNotExist:
            return Response({"error": "Invalid session."}, status=400)

        serializer = RegisterStep2Serializer(partial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True})
        
        return Response(serializer.errors, status=400)


class RegisterStep3View(APIView):
    def post(self, request):
        serializer = RegisterStep3Serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        session_id = serializer.validated_data['session_id']
        password = serializer.validated_data['password']

        try:
            partial = PartialUser.objects.get(session_id=session_id)
        except PartialUser.DoesNotExist:
            return Response({"error": "Invalid session."}, status=400)

        # Create the final user
        user = User.objects.create_user(
            full_name=partial.full_name,
            email=partial.email,
            phone_number=partial.phone_number,
            pan_card=partial.pan_card,
            aadhaar_card=partial.aadhaar_card,
            dob=partial.dob,
            password=password
        )
        
        # Log the user in immediately after registration
        login(request, user)

        # Optionally delete the partial entry
        partial.delete()

        return Response({"message": "Registration complete", "user_id": user.id}, status=201)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def login_view(request):
    return render(request, "authentication.html")

def dash_view(request):
    return render(request, "dashboard.html")