from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import sendOTP, verifyNumber

from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth import login
from django.core.exceptions import ValidationError

def index(request):
    return HttpResponse("hello world")

@api_view(['POST'])
def OTPView(request):
    data = request.data
    countryCode = data["countryCode"]
    phone = data["phone"]
    return Response(sendOTP(f"{countryCode}{phone}"))

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        body = request.data
        country = body['countryCode']
        phone = body['phone']
        otp = body['otp']
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise ValidationError({"error": "user not found"})

        if not verifyNumber(f"{country}{phone}", otp):
            raise ValidationError({"message": "verification failed"})

        token = Token.objects.get_or_create(user=user)
        print(token)

        if user:
            if user.is_active:
                login(request, user)
                data = dict()
                data["message"] = "Log in successfull"
                data["username"] = user.username

                result = {"data" : data, "token" : token[0].key}

                return Response(result)
            else:
                return Response({"error": "Account not active"})
        else:
            return Response({"error": "Account Does not exist"})

class SessionView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = sessionsSerializer
    permission_classes = (IsAuthenticated,)

class MessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = messageSerializer
    permission_classes = (IsAuthenticated,)

class viewMessages(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = messageSerializer

    def get_queryset(self):
        return Session.objects.filter(topic=self.kwargs['topic'])
