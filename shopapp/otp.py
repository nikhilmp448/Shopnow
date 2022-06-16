
from twilio.rest import Client

def sendOTP(mobile):
    
    number = '+91'+ str(mobile)
    account_sid = 'AC543c3b3b75793125803248d128347b3c'
    auth_token = '3ff9bc196234f5f78fe1c4b12159c309'
    client = Client(account_sid, auth_token)

    verification = client.verify \
                     .services('VA025e2b12cacc22da015ffd55355787be') \
                     .verifications \
                     .create(to= number, channel='sms')

    print(verification.status)

def verifyOTP(mobile,otp):

    number = '+91'+ str(mobile)
    account_sid = 'AC543c3b3b75793125803248d128347b3c'
    auth_token = '3ff9bc196234f5f78fe1c4b12159c309'
    client = Client(account_sid, auth_token)

    verification_check = client.verify \
                           .services('VA025e2b12cacc22da015ffd55355787be') \
                           .verification_checks \
                           .create(to= number, code= otp)

    print(verification_check.status)

    if verification_check.status == 'approved':
        print('verification confirmed')
        return True
    else:
        return False