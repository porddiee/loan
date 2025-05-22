from django.contrib import admin
from .models import loanRequest, loanCategory, CustomerLoan, loanTransaction
# Register your models here.loanCategory,

class LoanTransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'payment', 'payment_date')

admin.site.register(loanRequest)
admin.site.register(loanCategory)
admin.site.register(loanTransaction, LoanTransactionAdmin)
admin.site.register(CustomerLoan)
