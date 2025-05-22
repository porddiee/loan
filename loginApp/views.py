from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerSignUpForm, CustomerLoginForm, UpdateCustomerForm
from django.shortcuts import redirect
from .models import CustomerSignUp
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def sign_up_view(request):
    error = ''
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    form = CustomerSignUpForm()
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set email to empty string if not provided
            if not form.cleaned_data.get('email'):
                user.email = ''
            user.save()
            
            # Create customer profile with default values
            user_profile = CustomerSignUp(
                user=user,
                first_name=user.username,  # Default to username
                last_name='',  # Empty by default
                email=user.email or '',  # Use empty string if no email
                designation='Customer',  # Default designation
                address='Manila, Philippines',  # Default to Manila, Philippines
                profile_picture='profile_pic/default.jpg'  # Default profile picture
            )
            user_profile.save()
            
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account created successfully! Please complete your profile information.')
                return redirect('login_App:edit-customer')
            return HttpResponseRedirect(reverse('login_App:login_customer'))
        else:
            if User.objects.filter(username=request.POST['username']).exists():
                error = 'Customer already exists'
            else:
                error = 'Your password is not strong enough or both passwords must be same'

    return render(request, 'loginApp/signup.html', context={'form': form, 'user': "Customer Register", 'error': error})


def login_view(request):
    form = CustomerLoginForm()
    if request.method == 'POST':
        form = CustomerLoginForm(data=request.POST)
        # username = request.POST['username']
        # password = request.POST['password']
        # print(username, password)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

        else:
            return render(request, 'loginApp/login.html', context={'form': form, 'user': "Customer Login", 'error': 'Invalid username or password'})
    return render(request, 'loginApp/login.html', context={'form': form, 'user': "Customer Login"})


@login_required(login_url='login_App:login_customer')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url='login_App:login_customer')
def edit_customer(request):
    try:
        customer = CustomerSignUp.objects.get(user=request.user)
        # Update address if it's empty or contains Bangladesh
        if not customer.address or 'Bangladesh' in customer.address:
            customer.address = 'Manila, Philippines'
            customer.save()
    except CustomerSignUp.DoesNotExist:
        # Create a new customer profile if it doesn't exist
        customer = CustomerSignUp(
            user=request.user,
            first_name=request.user.username,
            last_name='',
            email=request.user.email,
            designation='Customer',
            address='Manila, Philippines',
            profile_picture='profile_pic/default.jpg'
        )
        customer.save()
    
    form = UpdateCustomerForm(instance=customer)
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            messages.success(request, 'Profile updated successfully!')
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'loginApp/edit.html', context={'form': form})
