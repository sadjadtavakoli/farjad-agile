from django.db import models

# Create your models here.
from django_fsm import FSMField, transition


class Loan(models.Model):
    book = models.ManyToManyField('books.Books', related_name="loans")
    borrower = models.ManyToManyField('members.Member', related_name='loans')

    state = models.OneToOneField('loan.LoanState', related_name="+", on_delete='CASCADE')


class LoanState(models.Model):
    STATE_NEW = 'NEW'
    STATE_QUEUE = 'QUEUE'
    STATE_REJECTED = 'REJECTED'
    STATE_READY_TO_PAY = 'READY_TO_PAY'
    STATE_BORROWED = 'BORROWED'
    STATE_CANCELED_BY_BORROWER = 'CANCELED-BY-BORROWER'
    STATE_CANCELED_BY_LENDER = 'CANCELED-BY-LENDER'
    STATE_PAYED = 'PAYED'

    state = FSMField(protected=True, default=STATE_NEW)

    @transition(field=state, source=STATE_NEW,
                target=STATE_QUEUE)
    def marked_as_seen(self):
        pass

    @transition(field=state, source=[STATE_QUEUE, STATE_NEW], target=STATE_REJECTED)
    def rejected(self):
        pass

    @transition(field=state, source=[STATE_QUEUE, STATE_NEW], target=STATE_READY_TO_PAY)
    def ready_for_pay(self):
        pass

    @transition(field=state, source=STATE_READY_TO_PAY, target=STATE_CANCELED_BY_LENDER)
    def canceled_by_lender(self):
        pass

    @transition(field=state, source=[STATE_READY_TO_PAY, STATE_QUEUE, STATE_NEW],
                target=STATE_CANCELED_BY_BORROWER)
    def canceled_by_borrower(self):
        pass

    @transition(field=state, source=STATE_PAYED, target=STATE_BORROWED)
    def borrowed(self):
        pass

    @transition(field=state, source=STATE_READY_TO_PAY, target=STATE_PAYED)
    def payed(self):
        pass

    @property
    def borrower_buttons(self):
        buttons = {
            LoanState.STATE_NEW: [{'label': 'لغو درخواست', 'action': 'borrower-cancel'}],
            LoanState.STATE_QUEUE: [{'label': 'لغو درخواست', 'action': 'borrower-cancel'}],
            LoanState.STATE_REJECTED: [],
            LoanState.STATE_READY_TO_PAY: [{'label': 'لغو درخواست', 'action': 'borrower-cancel'},
                                           {'label': 'پرداخت', 'action': 'borrower-payed'}],
            LoanState.STATE_BORROWED: [],
            LoanState.STATE_CANCELED_BY_BORROWER: [],
            LoanState.STATE_CANCELED_BY_LENDER: [],
            LoanState.STATE_PAYED: [],
        }
        return buttons.get(self.state)

    buyer_action_map = {'borrower-cancel': canceled_by_borrower,
                        'borrower-payed': payed}

    @property
    def lender_buttons(self):
        buttons = {
            LoanState.STATE_NEW: [{'label': 'دیده شده',
                                   'action': 'mark-as-seen'},
                                  {'label': 'قبول کردن', 'action': 'lender-accept'},
                                  {'label': 'رد کردن', 'action': 'lender-reject'}],
            LoanState.STATE_QUEUE: [{'label': 'قبول کردن', 'action': 'lender-accept'},
                                    {'label': 'رد کردن', 'action': 'lender-reject'}],
            LoanState.STATE_REJECTED: [],
            LoanState.STATE_PAYED: [],
            LoanState.STATE_READY_TO_PAY: [{'label': 'لغو درخواست', 'action': 'lender-cancel'}],
            LoanState.STATE_BORROWED: [],
            LoanState.STATE_CANCELED_BY_BORROWER: [],
            LoanState.STATE_CANCELED_BY_LENDER: [],
        }
        return buttons.get(self.state)

    seller_action_map = {
        'mark-as-seen': marked_as_seen,
        'lender-accept': ready_for_pay,
        'lender-reject': rejected,
        'lender-cancel': canceled_by_lender,
    }
