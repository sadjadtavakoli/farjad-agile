from django.conf import settings


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
