from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from shop.models import Products


def index(request):
    products = Products.objects.all()
    return render(request, 'accounts/index.html', {'products': products})


def customer_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form_r = form.save(commit=False)
            form_r.is_customer = True
            form_r.set_password(form_r.password)
            form.save()

        else:
            return HttpResponse('form not valid')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/user_form.html', {'form': form})


def shop_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form_r = form.save(commit=False)
            form_r.is_shop = True
            form_r.set_password(form_r.password)
            form.save()

        else:
            return HttpResponse('form not valid')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/shop_register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active and user.is_customer:
                login(request, user)
                return redirect('customer:index')
            elif user.is_active and user.is_shop:
                login(request, user)
                return redirect('shop:index')
            else:
                return HttpResponse('user is not active')
        else:
            return HttpResponse('username or password is wrong')
    else:

        return render(request, 'accounts/user_login.html', {})
    


def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')