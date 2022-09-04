from typing import Dict
from twilio.rest import Client
from decouple import config

from django.contrib.auth.backends import BaseBackend

from .models import User

account_sid = config('account_sid')
auth_token = config('auth_token')
OTP_token = config('OTP_token')

client = Client(account_sid, auth_token)
verify = client.verify.services(OTP_token)

def sendOTP(phone: str) -> Dict:
    """
    Sends a one time password to the given number
    """
    try:
        verify.verifications.create(to=phone, channel='sms')
        return {
            "message": "OTP sent"
        }
    except:
        return {
            "message": "Invalid number"
        }

def verifyNumber(phone: str, otp: str) -> bool:
    """
    verifies the otp for a given number
    """
    try:
        res = verify.verification_checks.create(to=phone, code=otp)
        return res.status == 'approved'
    except:
        return False

class userBackend(BaseBackend):
    def authenticate(self, request, phone, countryCode, otp, password = None, superUser = True):
        if superUser:
            try:
                user = User.objects.get(phone=email)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        else:
            verify = verifyNumber(f"{countryCode}{phone}", otp)
            if verify:
                try:
                    user = User.objects.get(phone=phone)
                except User.DoesNotExist:
                    return None
                return user
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
