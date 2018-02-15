from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Manager
from django_fsm import FSMField, transition

from farjad.utils.utils_view import auto_save


class LoanManager(Manager):
    def get_requests(self):
        return super().get_queryset().filter(
            state__state__in=[LoanState.STATE_NEW, LoanState.STATE_QUEUE,
                              LoanState.STATE_READY_TO_PAY, LoanState.STATE_PAYED,
                              LoanState.STATE_BORROWED])

    def get_borrowed_books(self):
        return super().get_queryset().filter(
            state__state=LoanState.STATE_BORROWED)

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj.borrower.decrease_balance(obj.book.price)
        obj.save(force_insert=True, using=self.db)
        return obj


class Loan(models.Model):
    objects = LoanManager()
    book = models.ForeignKey('books.Books', related_name="loans", on_delete=models.CASCADE)
    borrower = models.ForeignKey('members.Member', related_name='loans',
                                 on_delete=models.CASCADE)

    date = models.DateField(default=0)
    state = models.OneToOneField('loan.LoanState', related_name="+", on_delete='PROTECTED',
                                 blank=True, null=True)

    def save(self, *args, **kwargs):
        self.state = self.state if self.state_id else LoanState.objects.create()
        return super(Loan, self).save(*args, **kwargs)

    @property
    def deadline(self):
        delta = relativedelta(days=1)
        if self.book.period == 'weekly':
            delta = relativedelta(weeks=1)
        elif self.book.period == 'monthly':
            delta = relativedelta(month=1)
        return self.date + delta


class LoanState(models.Model):
    STATE_NEW = 'NEW'
    STATE_QUEUE = 'QUEUE'
    STATE_REJECTED = 'REJECTED'
    STATE_READY_TO_PAY = 'READY_TO_PAY'
    STATE_BORROWED = 'BORROWED'
    STATE_FINISHED = 'FINISHED'
    STATE_CANCELED_BY_BORROWER = 'CANCELED-BY-BORROWER'
    STATE_CANCELED_BY_LENDER = 'CANCELED-BY-LENDER'
    STATE_PAYED = 'PAYED'

    state = FSMField(protected=True, default=STATE_NEW)

    @auto_save
    @transition(field=state, source=STATE_NEW,
                target=STATE_QUEUE)
    def marked_as_seen(self):
        self.save()
        pass

    @auto_save
    @transition(field=state, source=[STATE_QUEUE, STATE_NEW], target=STATE_REJECTED)
    def rejected(self):
        pass

    @auto_save
    @transition(field=state, source=[STATE_QUEUE, STATE_NEW], target=STATE_READY_TO_PAY)
    def ready_for_pay(self):
        pass

    @auto_save
    @transition(field=state, source=STATE_READY_TO_PAY, target=STATE_CANCELED_BY_LENDER)
    def canceled_by_lender(self):
        pass

    @auto_save
    @transition(field=state, source=[STATE_READY_TO_PAY, STATE_QUEUE, STATE_NEW],
                target=STATE_CANCELED_BY_BORROWER)
    def canceled_by_borrower(self):
        pass

    @auto_save
    @transition(field=state, source=STATE_PAYED, target=STATE_BORROWED)
    def borrowed(self):
        pass

    @auto_save
    @transition(field=state, source=STATE_BORROWED, target=STATE_FINISHED)
    def finished(self):
        pass

    @auto_save
    @transition(field=state, source=STATE_READY_TO_PAY, target=STATE_PAYED)
    def payed(self):
        pass

    def update_state(self):
        self.shown_state = self.state

    @property
    def borrower_buttons(self):
        buttons = {
            LoanState.STATE_NEW: [{'label': 'لغو درخواست', 'action': 'borrower-cancel'}],
            LoanState.STATE_QUEUE: [{'label': 'لغو درخواست', 'action': 'borrower-cancel'}],
            LoanState.STATE_REJECTED: [],
            LoanState.STATE_READY_TO_PAY: [{'label': 'لغو درخواست', 'action': 'borrower-cancel'},
                                           {'label': 'پرداخت', 'action': 'borrower-payed'}],
            LoanState.STATE_BORROWED: [{'label': 'بازگشت', 'action': 'borrower-return'}],
            LoanState.STATE_CANCELED_BY_BORROWER: [],
            LoanState.STATE_CANCELED_BY_LENDER: [],
            LoanState.STATE_PAYED: [{'label': 'ثبت‌شدن کتاب', 'action': 'commit'}],
        }
        return buttons.get(self.state)

    borrower_action_map = {'borrower-cancel': canceled_by_borrower,
                           'borrower-payed': payed,
                           'commit': borrowed,
                           'borrower-return': finished}

    @property
    def lender_buttons(self):
        buttons = {
            LoanState.STATE_NEW: [{'label': 'رد کردن', 'action': 'lender-reject'},
                                  {'label': 'قبول کردن', 'action': 'lender-accept'}],
            LoanState.STATE_QUEUE: [{'label': 'رد کردن', 'action': 'lender-reject'},
                                    {'label': 'قبول کردن', 'action': 'lender-accept'}],
            LoanState.STATE_REJECTED: [],
            LoanState.STATE_PAYED: [],
            LoanState.STATE_READY_TO_PAY: [{'label': 'لغو درخواست', 'action': 'lender-cancel'}],
            LoanState.STATE_BORROWED: [],
            LoanState.STATE_CANCELED_BY_BORROWER: [],
            LoanState.STATE_CANCELED_BY_LENDER: [],
        }
        return buttons.get(self.state)

    lender_action_map = {
        'mark-as-seen': marked_as_seen,
        'lender-accept': ready_for_pay,
        'lender-reject': rejected,
        'lender-cancel': canceled_by_lender,
    }
