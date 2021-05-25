from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_register', views.customer_register, name='user_register'),
    path('shop_register', views.shop_register, name='shop_register'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
