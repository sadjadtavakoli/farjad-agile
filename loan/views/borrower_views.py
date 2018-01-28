from django.views.generic import ListView

from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired
from loan.models import Loan, LoanState
from loan.permissions import BorrowerPermission
from loan.views.loan_views import ChangeLoanStateView
from members.views.area_setter import PanelAreaSetter


class BorrowerLoansRequestList(PanelAreaSetter, PermissionCheckerMixin, ListView):
    model = Loan
    admin_area = 'borrower_requests'
    permission_classes = [LoginRequired]
    context_object_name = 'loans'
    template_name = 'borrower_loans_list.html'

    def get_queryset(self):
        return Loan.objects.get_requests().filter(borrower=self.request.user)


class BorrowedBooksList(PanelAreaSetter, PermissionCheckerMixin, ListView):
    model = Loan
    admin_area = 'borrowed_book_list'
    permission_classes = [LoginRequired]
    context_object_name = 'loans'
    template_name = 'borrowed_books_list.html'

    def get_queryset(self):
        return Loan.objects.get_borrowed_books().filter(borrower=self.request.user)


class BorrowerChangeLoanStateView(ChangeLoanStateView):
    action_map = LoanState.borrower_action_map
    permission_classes = [BorrowerPermission]

    def get_buttons(self):
        return self.request.loan.state.borrower_buttons
