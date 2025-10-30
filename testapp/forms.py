# In testapp/forms.py
from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        # These fields MATCH your new models.py
        fields = ['name', 'mobile', 'address'] 
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Full Name'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Your Mobile Number'}),
            'address': forms.Textarea(attrs={'placeholder': 'Your Full Address', 'rows': 4}),
        }