from django import forms
from .models import Customer, MilkEntry

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'whatsapp_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+919xxxxxxxxx'}),
        }

class MilkEntryForm(forms.ModelForm):
    # extra field to allow typing a new customer name
    customer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type new customer name (or leave blank to select)',
            'id': 'new_customer_input'
        }),
        label='New Customer (optional)'
    )

    class Meta:
        model = MilkEntry
        fields = ['customer', 'customer_name', 'date', 'quantity_ml']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-select select-customer',
                'id': 'id_customer_select',
                'data-placeholder': '-- Select or search customer --'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_date_input'
            }),
            'quantity_ml': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1',
                'placeholder': 'Enter quantity in ml',
                'id': 'id_quantity_input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # populate customer choices with all customers
        self.fields['customer'].queryset = Customer.objects.all().order_by('name')
        # make customer optional (user can create new)
        self.fields['customer'].required = False

    def clean(self):
        cleaned = super().clean()
        cust = cleaned.get('customer')
        cust_name = cleaned.get('customer_name')
        if not cust and not cust_name:
            raise forms.ValidationError("Please select an existing customer or enter a new customer name.")
        return cleaned