from django.conf import settings


def get_url(image, location):
    if image and hasattr(image, 'url'):
        return image.url
    else:
        return '{}{}'.format(settings.STATIC_URL, location)
