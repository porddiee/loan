from django import forms
from .models import loanRequest, loanTransaction


class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = loanRequest
        fields = ('category', 'reason', 'amount', 'duration_type', 'duration_value', 'collateral')


class LoanTransactionForm(forms.ModelForm):
    class Meta:
        model = loanTransaction
        fields = ('payment',)
