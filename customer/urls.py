
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'customer'

urlpatterns = [
    path('', views.index, name='index'),
    path('product_list', views.ProductList.as_view(), name='product_list'),
    path('product_details/<int:id>', views.product_details, name='product_details'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart_summary/<int:id>',
         views.add_to_cart_summary, name='add_to_cart_summary'),
    path('remove_single_item/<int:id>',
         views.remove_single_item, name='remove_single_item'),
    path('order_summary', views.OrderSummaryView.as_view(), name='order_summary'),
    path('CheckOut', views.CheckOut.as_view(), name='CheckOut'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
