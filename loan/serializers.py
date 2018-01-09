from rest_framework.serializers import ModelSerializer

from loan.models import Loan


class LoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = ('book', 'borrower', 'pk', 'date')
