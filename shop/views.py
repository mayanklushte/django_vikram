from django.shortcuts import render
from .forms import ProductForm
from .models import Products
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.urls import reverse_lazy


def index(request):
    return render(request, 'shop/index.html',)


def user_check(user):
    return user.is_shop


@login_required
@user_passes_test(user_check, login_url='accounts:user_login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form_r = form.save(commit=False)
            form_r.user = request.user
            form_r.save()
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})


class ProductList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Products
    template_name = 'shop/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = context['object_list'].filter(user=self.request.user)
        return context

    def test_func(self):
        x = self.request.user
        if x.is_shop:
            return True
        else:
            raise Http404("You are Not Allowed Here")


class ProductDetails(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Products
    template_name = 'shop/product_details.html'
    context_object_name = 'product'
    
    def test_func(self):
        x = self.request.user
        if x.is_shop:
            return True
        else:
            raise Http404("You are Not Allowed Here")


class ProductUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Products
    form_class = ProductForm
    success_url = reverse_lazy('shop:product_list')
    template_name = 'shop/update_product.html'

    def test_func(self):
        x = self.request.user
        if x.is_shop:
            return True
        else:
            raise Http404("You are Not Allowed Here")


class ProductDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Products
    success_url = reverse_lazy('shop:product_list')
    context_object_name = 'product'

    def test_func(self):
        x = self.request.user
        if x.is_shop:
            return True
        else:
            raise Http404("You are Not Allowed Here")