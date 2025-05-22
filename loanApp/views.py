from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoanRequestForm, LoanTransactionForm
from .models import loanRequest, loanTransaction, CustomerLoan
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from loginApp.models import CustomerSignUp
from django.contrib import messages

# Create your views here.


# @login_required(login_url='/account/login-customer')
def home(request):

    return render(request, 'home.html', context={})


@login_required(login_url='login_App:login_customer')
def LoanRequest(request):
    from loginApp.models import CustomerSignUp
    try:
        customer = request.user.customer
    except CustomerSignUp.DoesNotExist:
        messages.warning(request, "No customer profile found. Please complete your profile before requesting a loan.")
        return redirect('login_App:edit-customer')

    form = LoanRequestForm()
    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            loan_obj = form.save(commit=False)
            loan_obj.customer = customer
            loan_obj.save()
            messages.success(request, 'Loan application submitted successfully! We will review your request shortly.')
            return redirect('/')
    return render(request, 'loanApp/loanrequest.html', context={'form': form})

    # reason = request.POST.get('reason')
    # amount = request.POST.get('amount')
    # category = request.POST.get('category')
    # year = request.POST.get('year')
    # customer = request.user.customer

    # loan_request = LoanRequest(request)
    # loan_request.customer = customer
    # loan_request.save()
    # if form.is_valid():
    #     loan_request = form.save(commit=False)
    #     loan_request.customer = request.user.customer
    #     print(loan_request)
    #     return redirect('/')


@login_required(login_url='login_App:login_customer')
def LoanPayment(request):
    form = LoanTransactionForm()
    if request.method == 'POST':
        form = LoanTransactionForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = request.user.customer
            payment.save()
            messages.success(request, f'Payment of ${payment.payment} processed successfully!')
            return redirect('/')

    return render(request, 'loanApp/payment.html', context={'form': form})


@login_required(login_url='login_App:login_customer')
def UserTransaction(request):
    transactions = loanTransaction.objects.filter(
        customer=request.user.customer)
    return render(request, 'loanApp/user_transaction.html', context={'transactions': transactions})


@login_required(login_url='login_App:login_customer')
def UserLoanHistory(request):
    from loginApp.models import CustomerSignUp
    try:
        customer = request.user.customer
        loans = loanRequest.objects.filter(customer=customer)
        latest_approved_loan = loans.filter(status='approved').order_by('-request_date').first()
        loan_remaining = {}
        from loanApp.models import loanTransaction
        from django.db.models import Sum
        for loan in loans:
            if loan == latest_approved_loan and loan.status == 'approved':
                customer_loan = CustomerLoan.objects.filter(customer=loan.customer).first()
                payable = customer_loan.payable_loan if customer_loan else 0
                total_paid = loanTransaction.objects.filter(
                    customer=loan.customer,
                    payment_date__gte=loan.request_date
                ).aggregate(Sum('payment'))['payment__sum'] or 0
                loan_remaining[loan.id] = max(payable - total_paid, 0)
            else:
                loan_remaining[loan.id] = '-'
        message = ''
    except CustomerSignUp.DoesNotExist:
        loans = []
        loan_remaining = {}
        message = 'No customer profile found. Please complete your profile.'
    return render(request, 'loanApp/user_loan_history.html', {'loans': loans, 'loan_remaining': loan_remaining, 'message': message})


@login_required(login_url='login_App:login_customer')
def UserDashboard(request):
    try:
        customer = request.user.customer
        requestLoan = loanRequest.objects.all().filter(
            customer=customer).count()
        approved = loanRequest.objects.all().filter(
            customer=customer).filter(status='approved').count()
        rejected = loanRequest.objects.all().filter(
            customer=customer).filter(status='rejected').count()
        totalLoan = CustomerLoan.objects.filter(customer=customer).aggregate(Sum('total_loan'))[
            'total_loan__sum']
        totalPayable = CustomerLoan.objects.filter(customer=customer).aggregate(
            Sum('payable_loan'))['payable_loan__sum']
        totalPaid = loanTransaction.objects.filter(customer=customer).aggregate(Sum('payment'))[
            'payment__sum']
        total_loan_amount = loanRequest.objects.filter(status='approved').aggregate(Sum('amount'))['amount__sum'] or 0

        dict = {
            'request': requestLoan,
            'approved': approved,
            'rejected': rejected,
            'totalLoan': totalLoan if totalLoan else 0,
            'totalPayable': totalPayable if totalPayable else 0,
            'totalPaid': totalPaid if totalPaid else 0,
            'total_loan_amount': total_loan_amount,
        }

        return render(request, 'loanApp/user_dashboard.html', context=dict)
    except CustomerSignUp.DoesNotExist:
        # Redirect to profile completion page if customer profile doesn't exist
        return redirect('login_App:edit-customer')


@login_required(login_url='login_App:login_customer')
def view_loan_status(request):
    from loginApp.models import CustomerSignUp
    try:
        customer = request.user.customer
        loans = loanRequest.objects.filter(customer=customer)
        message = ''
    except CustomerSignUp.DoesNotExist:
        loans = []
        message = 'No customer profile found. Please complete your profile.'
    return render(request, 'loanApp/loan_status.html', context={'loans': loans, 'message': message})


def error_404_view(request, exception):
    print("not found")
    return render(request, 'notFound.html')
