from django.forms import ModelForm
from django import forms
from .models import Item, Medicine, Vendor
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class PasswordChangingForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    class Meta:
        model = User
        fields = '__all__'


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('batch_id', 'expiry_date',
                  'order_date', 'quantity', 'medicine')

    def __init__(self, request, vendor):
        super().__init__(request)
        self.fields['medicine'].queryset = Medicine.objects.filter(
            vendor=vendor).order_by('trade_name')


class SellForm(forms.Form):
    name = forms.CharField()
    phone_regex = RegexValidator(
        regex=r'^(?:\s+|)((0|(?:(\+|)91))(?:\s|-)*(?:(?:\d(?:\s|-)*\d{9})|(?:\d{2}(?:\s|-)*\d{8})|(?:\d{3}(?:\s|-)*\d{7}))|\d{10})(?:\s+|)', message=("Phone Number is not valid"))
    phone = forms.CharField(validators=[phone_regex])
    medicine = forms.ModelChoiceField(
        queryset=Medicine.objects.order_by('trade_name'))

    def validate_quantity(quan):
        if quan <= 0:
            raise ValidationError("Not a valid quantity.")
    quantity = forms.IntegerField(min_value=1, validators=[validate_quantity])




class UsableItemForm(ModelForm):
	class Meta:
		model = Medicine
		fields = ['trade_name', 'generic_name', 'description',
                    'purchasePrice', 'unit_selling', 'threshold_value', 'vendor']






class NewMedicineForm(ModelForm):
	vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), initial=0)

	class Meta:
		model = Medicine
		fields = ['trade_name', 'generic_name', 'description',
                    'purchasePrice', 'unit_selling', 'threshold_value', 'vendor']


class VendorForm(ModelForm):
	class Meta:
		model = Vendor
		fields = '__all__'


class RevenueForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    def validate(start, end):
        pass
