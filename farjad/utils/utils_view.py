import random
import string

from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException


def get_url(image, location):
    if image and hasattr(image, 'url'):
        return image.url
    else:
        return '{}{}'.format(settings.STATIC_URL, location)


def auto_save(func):
    def autosave(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        self.save()
        return res

    return autosave


def get_random(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def sms_sending(mobile_number, code):
    try:
        api = KavenegarAPI('5532514D484F77647533444F3762464863476D564B566C64712B412B575A354A')
        params = {
            'sender': '',  # optional
            'receptor': mobile_number,
            'message': 'سلام, کد ورود شما به سیستم'+code+'می‌باشد.',

        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
