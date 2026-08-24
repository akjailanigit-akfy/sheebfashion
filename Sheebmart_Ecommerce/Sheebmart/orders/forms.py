from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name", "mobile", "door_number", "street",
            "city", "state", "pincode"
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
            "mobile": forms.TextInput(attrs={"class": "form-control", "placeholder": "Mobile number"}),
            "door_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "House / Door number"}),
            "street": forms.TextInput(attrs={"class": "form-control", "placeholder": "Street"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "pincode": forms.TextInput(attrs={"class": "form-control", "placeholder": "Pincode"}),
        }
