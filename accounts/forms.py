from django import forms
from .models import Customer, MilkEntry


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'balance_amount']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name'
            }),
            'balance_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
        }


class MilkEntryForm(forms.ModelForm):
    # Optional: create new customer
    customer_name = forms.CharField(
        required=False,
        label="New Customer (optional)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new customer name'
        })
    )

    class Meta:
        model = MilkEntry
        fields = ['customer', 'customer_name', 'date', 'quantity_ml']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'quantity_ml': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Quantity in ml'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        customer_name = cleaned_data.get('customer_name')

        # Normalize input
        if customer_name:
            customer_name = customer_name.strip()
            cleaned_data['customer_name'] = customer_name

        # ❌ both empty → INVALID
        if not customer and not customer_name:
            raise forms.ValidationError(
                "Select an existing customer OR enter a new customer name."
            )

        # ❌ both filled → INVALID
        if customer and customer_name:
            raise forms.ValidationError(
                "Please choose only ONE: existing customer OR new customer name."
            )

        return cleaned_data
