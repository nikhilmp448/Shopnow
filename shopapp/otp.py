from django.conf import settings
from twilio.rest import Client

def sendOTP(mobile):
    
    number = '+91'+ str(mobile)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    verification = client.verify \
                     .services(settings.TWILIO_SERVICE) \
                     .verifications \
                     .create(to= number, channel='sms')

    print(verification.status)

def verifyOTP(mobile,otp):

    number = '+91'+ str(mobile)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    verification_check = client.verify \
                           .services(settings.TWILIO_SERVICE) \
                           .verification_checks \
                           .create(to= number, code= otp)

    print(verification_check.status)

    if verification_check.status == 'approved':
        print('verification confirmed')
        return True
    else:
        return False