from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from farjad.utils.permission_checker import LoginRequired
from loan.models import Loan


class LoanBasePermission(LoginRequired):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        loan_pk = view.kwargs.get('loan_pk', '')
        loan = get_object_or_404(Loan, id=loan_pk)
        request.loan = loan
        return True


class LenderPermission(LoanBasePermission):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        if request.user != request.loan.book.owner:
            raise PermissionDenied
        return True


class BorrowerPermission(LoanBasePermission):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        if request.user != request.loan.borrower:
            raise PermissionDenied
        return True
