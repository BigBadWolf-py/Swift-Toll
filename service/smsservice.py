import requests


class SMSService(object):
    __URL = 'http://103.16.142.107:55/api/mt/SendSMS?user=rawat&password=rawat&senderid=SWFTOL&channel=Trans&DCS=0&' \
            'flashsms=0&number={phone_number}&text={message}&route=01'

    @classmethod
    def sendSMS(cls, msg, phone_number, cc='91'):
        response = requests.get(cls.__URL.format(phone_number=cc+str(phone_number), message=msg))
        if response.status_code == 200:
            return True
        else:
            return False
