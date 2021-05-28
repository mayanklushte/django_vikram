from django import forms
from .models import BillingAddress

class ChekoutForm(forms.Form):
    street_address = forms.CharField(max_length=50)
    Apartment_Address = forms.CharField(max_length=50)
    Country = forms.CharField(max_length=20)
    State = forms.CharField(max_length=30)
    Pin_Code = forms.CharField(max_length=6)
    Mobile_No = forms.CharField(max_length=10)
    E_mail = forms.EmailField()
    same_shiping_address = forms.BooleanField()
