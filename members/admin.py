from django.contrib import admin

# Register your models here.
from members.models import Member, PhoneCodeMapper

admin.site.register(Member)
admin.site.register(PhoneCodeMapper)
