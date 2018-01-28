from django.views.generic import ListView

from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired
from loan.models import Loan, LoanState
from loan.permissions import LenderPermission
from loan.views.loan_views import ChangeLoanStateView
from members.views.area_setter import PanelAreaSetter


class LenderLoansRequestList(PanelAreaSetter, PermissionCheckerMixin, ListView):
    model = Loan
    admin_area = 'lender_requests'
    permission_classes = [LoginRequired]
    context_object_name = 'loans'
    template_name = 'lender_loans_list.html'

    def get_queryset(self):
        query = Loan.objects.get_requests().filter(book__owner=self.request.user)
        for item in query:
            item.state.update_state()
        for item in self.request.user.new_loan_requests:
            item.state.marked_as_seen()
        return query


class LoanedBooksList(PanelAreaSetter, PermissionCheckerMixin, ListView):
    model = Loan
    admin_area = 'leaned_books_list'
    permission_classes = [LoginRequired]
    context_object_name = 'loans'
    template_name = 'loaned_books_list.html'

    def get_queryset(self):
        return Loan.objects.get_borrowed_books().filter(book__owner=self.request.user)


class LenderChangeLoanStateView(ChangeLoanStateView):
    permission_classes = [LenderPermission]
    action_map = LoanState.lender_action_map

    def get_buttons(self):
        return self.request.loan.state.lender_buttons
