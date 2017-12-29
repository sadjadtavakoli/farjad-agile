from django.contrib import admin

from loan.models import Loan, LoanState

admin.site.register(Loan)
admin.site.register(LoanState)
