from django.views.generic.base import View
from customer.models import OrderItem
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from shop.models import Products
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def index(request):
    return render(request, 'customer/index.html', {})


def user_check(user):
    return user.is_customer


class ProductList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Products
    template_name = 'customer/product_list.html'

    def test_func(self):
        x = self.request.user
        if x.is_customer:
            return True
        else:
            raise Http404("You are Not Allowed Here")


@login_required
@user_passes_test(user_check, login_url='accounts:user_login')
def product_details(request, id):
    p_det = Products.objects.get(id=id)
    return render(request, 'customer/product_details.html', {'p_det': p_det})


@login_required
@user_passes_test(user_check, login_url='accounts:user_login')
def add_to_cart(request, id):
    item = get_object_or_404(Products, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        product=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(product_id=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("customer:product_list")
        else:
            order.item.add(order_item)
            return redirect("customer:product_list")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
    return redirect("customer:product_list")


@login_required
@user_passes_test(user_check, login_url='accounts:user_login')
def add_to_cart_summary(request, id):
    item = get_object_or_404(Products, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        product=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(product_id=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("customer:order_summary")
        else:
            order.item.add(order_item)
            return redirect("customer:product_list")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
    return redirect("customer:product_list")


@login_required
@user_passes_test(user_check, login_url='accounts:user_login')
def remove_single_item(request, id):
    item = get_object_or_404(Products, id=id)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(product_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                product=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:

                order_item.quantity -= 1
                order_item.save()
                return redirect("customer:order_summary")
            else:
                order.item.model.delete(order_item)
                return redirect("customer:order_summary")
        else:
            messages.warning(request, 'item was not in your cart')
            return redirect("customer:order_summary")
    else:
        messages.warning(request, 'item was not in your cart')
    return redirect("customer:order_summary")


class OrderSummaryView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        try:
            cart_item = OrderItem.objects.filter(
                user=self.request.user, ordered=False)
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object': order, 'cart_item': cart_item}
            return render(self.request, 'customer/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'not have an active order')
            return redirect("customer:product_list")

    def test_func(self):
        x = self.request.user
        if x.is_customer:
            return True
        else:
            raise Http404("You are Not Allowed Here")


class CheckOut(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        form = ChekoutForm()
        return render(self.request, 'customer/checkout.html', {'form': form})

    def post(self, *args, **kwargs):
        form = ChekoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                Apartment_Address = form.cleaned_data.get('Apartment_Address')
                Country = form.cleaned_data.get('Country')
                State = form.cleaned_data.get('State')
                Pin_Code = form.cleaned_data.get('Pin_Code')
                Mobile_No = form.cleaned_data.get('Mobile_No')
                E_mail = form.cleaned_data.get('E_mail')
                same_shiping_address = form.cleaned_data.get(
                    'same_shiping_address')

                billing = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    Apartment_Address=Apartment_Address,
                    Country=Country,
                    State=State,
                    Pin_Code=Pin_Code,
                    Mobile_No=Mobile_No,
                    E_mail=E_mail,
                    same_shiping_address=same_shiping_address)
                billing.save()
                order_item = OrderItem.objects.filter(
                    user=self.request.user, ordered=False)
                for i in order_item:
                    i.ordered = True
                    i.save()
                order.billing_Address = billing
                order.ordered = True
                order.save()
                messages.success(self.request, 'order has been placed')
                return redirect("customer:product_list")

        except ObjectDoesNotExist:
            messages.error(self.request, 'no Active orders')
            return redirect("customer:product_list")

    def test_func(self):
        x = self.request.user
        if x.is_customer:
            return True
        else:
            raise Http404("You are Not Allowed Here")
