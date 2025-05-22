from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from managerApp.forms import AdminLoginForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from loanApp.models import loanCategory, loanRequest, CustomerLoan, loanTransaction
from .forms import LoanCategoryForm
from loginApp.models import CustomerSignUp
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Sum

def superuser_login_view(request):
    form = AdminLoginForm()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        if request.method == 'POST':
            form = AdminLoginForm(data=request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(
                    request, username=username, password=password)

                if user is not None:
                    if user.is_superuser:
                        login(request, user)
                        return HttpResponseRedirect(reverse('managerApp:dashboard'))
                    else:
                        return render(request, 'admin/adminLogin.html', context={'form': form, 'error': "You are not Super User"})

            else:
                return render(request, 'admin/adminLogin.html', context={'form': form, 'error': "Invalid Username or Password "})
    return render(request, 'admin/adminLogin.html', context={'form': form, 'user': "Admin Login"})

@staff_member_required(login_url='/manager/admin-login')
def dashboard(request):
    # Count only non-admin users
    total_customer = CustomerSignUp.objects.filter(user__is_superuser=False).count()
    total_loan = loanRequest.objects.all().count()
    total_category = loanCategory.objects.all().count()
    total_transaction = loanTransaction.objects.all().count()
    total_revenue = loanTransaction.objects.aggregate(Sum('payment'))['payment__sum'] or 0
    total_loan_amount = loanRequest.objects.filter(status='approved').aggregate(Sum('amount'))['amount__sum'] or 0
    total_payable = CustomerLoan.objects.aggregate(Sum('payable_loan'))['payable_loan__sum'] or 0
    
    # Get pending loan requests
    pending_requests = loanRequest.objects.filter(status='pending').count()
    approved_requests = loanRequest.objects.filter(status='approved').count()
    rejected_requests = loanRequest.objects.filter(status='rejected').count()

    context = {
        'total_customer': total_customer,
        'total_loan': total_loan,
        'total_category': total_category,
        'total_transaction': total_transaction,
        'total_revenue': total_revenue,
        'total_loan_amount': total_loan_amount,
        'total_payable': total_payable,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests
    }
    return render(request, 'admin/dashboard.html', context)

@staff_member_required(login_url='/manager/admin-login')
def total_users(request):
    # Get all users except superusers
    users = CustomerSignUp.objects.filter(user__is_superuser=False)
    return render(request, 'admin/customer.html', context={'users': users})

@staff_member_required(login_url='/manager/admin-login')
def user_remove(request, pk):
    try:
        customer = CustomerSignUp.objects.get(user__id=pk)
        customer.delete()
    except CustomerSignUp.DoesNotExist:
        pass  # Optionally log this
    try:
        user = User.objects.get(id=pk)
        user.delete()
    except User.DoesNotExist:
        pass  # Optionally log this
    return HttpResponseRedirect('/manager/users')

@staff_member_required(login_url='/manager/admin-login')
def add_category(request):
    form = LoanCategoryForm()
    if request.method == 'POST':
        form = LoanCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('managerApp:dashboard')
    return render(request, 'admin/admin_add_category.html', {'form': form})

@staff_member_required(login_url='/manager/admin-login')
def loan_request(request):
    loanrequest = loanRequest.objects.filter(status='pending').order_by('-request_date')
    return render(request, 'admin/request_user.html', context={'loanrequest': loanrequest})

@staff_member_required(login_url='/manager/admin-login')
def approved_request(request, id):
    today = date.today()
    status_date = today.strftime("%B %d, %Y")
    loan_obj = loanRequest.objects.get(id=id)
    loan_obj.status_date = status_date
    loan_obj.save()
    duration_value = loan_obj.duration_value
    duration_type = loan_obj.duration_type
    if duration_type == 'months':
        duration_in_years = duration_value / 12
    else:
        duration_in_years = duration_value

    approved_customer = loanRequest.objects.get(id=id).customer
    if CustomerLoan.objects.filter(customer=approved_customer).exists():
        # find previous amount of customer
        PreviousAmount = CustomerLoan.objects.get(customer=approved_customer).total_loan
        PreviousPayable = CustomerLoan.objects.get(customer=approved_customer).payable_loan
        # update balance using duration_in_years
        CustomerLoan.objects.filter(customer=approved_customer).update(total_loan=int(PreviousAmount) + int(loan_obj.amount))
        CustomerLoan.objects.filter(customer=approved_customer).update(payable_loan=int(PreviousPayable) + int(loan_obj.amount) + int(loan_obj.amount) * 0.12 * duration_in_years)
    else:
        # request customer
        # CustomerLoan object create
        save_loan = CustomerLoan()
        save_loan.customer = approved_customer
        save_loan.total_loan = int(loan_obj.amount)
        save_loan.payable_loan = int(loan_obj.amount) + int(loan_obj.amount) * 0.12 * duration_in_years
        save_loan.save()

    loanRequest.objects.filter(id=id).update(status='approved')
    loanrequest = loanRequest.objects.filter(status='pending')
    return render(request, 'admin/request_user.html', context={'loanrequest': loanrequest})

@staff_member_required(login_url='/manager/admin-login')
def rejected_request(request, id):

    today = date.today()
    status_date = today.strftime("%B %d, %Y")
    loan_obj = loanRequest.objects.get(id=id)
    loan_obj.status_date = status_date
    loan_obj.save()
    # rejected_customer = loanRequest.objects.get(id=id).customer
    # print(rejected_customer)
    loanRequest.objects.filter(id=id).update(status='rejected')
    loanrequest = loanRequest.objects.filter(status='pending')
    return render(request, 'admin/request_user.html', context={'loanrequest': loanrequest})

@staff_member_required(login_url='/manager/admin-login')
def approved_loan(request):
    # print(datetime.now())
    approvedLoan = loanRequest.objects.filter(status='approved')
    return render(request, 'admin/approved_loan.html', context={'approvedLoan': approvedLoan})

@staff_member_required(login_url='/manager/admin-login')
def rejected_loan(request):
    rejectedLoan = loanRequest.objects.filter(status='rejected')
    return render(request, 'admin/rejected_loan.html', context={'rejectedLoan': rejectedLoan})

@staff_member_required(login_url='/manager/admin-login')
def transaction_loan(request):
    transactions = loanTransaction.objects.all()
    return render(request, 'admin/transaction.html', context={'transactions': transactions})
