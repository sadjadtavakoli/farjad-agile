# Create your views here.
from django.views.generic.list import ListView
from django_fsm import TransitionNotAllowed
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired
from loan.models import Loan, LoanState
from loan.permissions import LenderPermission, BorrowerPermission
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


class ChangeLoanStateView(PermissionCheckerMixin, APIView):
    response = {}
    action_map = {}

    def get_buttons(self):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        action = self.request.data.get('action')
        try:
            action_method = self.action_map[action]
            action_method(request.order.state)

        except (TransitionNotAllowed, KeyError):
            raise ValidationError("این کار شما مجاز نیست . ")
        return self.get_response()

    def get_response(self):
        buttons = self.get_buttons()
        self.response['buttons'] = buttons
        self.response['state'] = self.request.loan.state.state
        return Response(self.response)


class LenderChangeLoanStateView(ChangeLoanStateView):
    permission_classes = [LenderPermission]
    action_map = LoanState.lender_action_map

    def get_buttons(self):
        return self.request.loan.state.lender_buttons


class BorrowerChangeLoanStateView(ChangeLoanStateView):
    action_map = LoanState.borrower_action_map
    permission_classes = [BorrowerPermission]

    def get_buttons(self):
        return self.request.loan.state.borrower_buttons
