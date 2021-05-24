
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_product', views.add_product, name='add_product'),
    path('product_list', views.ProductList.as_view(), name='product_list'),
    path('update_product/<int:pk>', views.ProductUpdate.as_view(), name='update_product'),
    path('product_detail/<int:pk>', views.ProductDetails.as_view(), name='product_detail'),
    path('product_delete/<int:pk>', views.ProductDelete.as_view(), name='product_delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
