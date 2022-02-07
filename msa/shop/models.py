from django.db import models
from django.utils.timezone import now
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=500, blank=False)
    phone_regex = RegexValidator(
        regex=r'^(?:\s+|)((0|(?:(\+|)91))(?:\s|-)*(?:(?:\d(?:\s|-)*\d{9})|(?:\d{2}(?:\s|-)*\d{8})|(?:\d{3}(?:\s|-)*\d{7}))|\d{10})(?:\s+|)', message=("Phone Number is not valid"))
    phone = models.CharField(max_length=14, blank=False, validators=[phone_regex] )
    email = models.EmailField(blank=False)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    def validate_price(price):
        if price <= 0:
            raise ValidationError("Price is not valid.")

    trade_name = models.CharField(max_length=100, blank=False)
    generic_name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=500, default=None, blank=True)
    purchasePrice = models.DecimalField(
        decimal_places=2, default=0.00, blank=False, max_digits=10, validators=[validate_price])
    unit_selling = models.DecimalField(
        decimal_places=2, default=0.00, blank=False, max_digits=10, validators=[validate_price])
    threshold_value = models.IntegerField(
        default=0, blank=True)
    vendor = models.ForeignKey(Vendor, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.trade_name


class Transaction(models.Model):

    def validate_quantity(quan):
        if quan <= 0:
            raise ValidationError("Not a valid quantity.")
    def validate_date(date):
        if date < date.today():
            raise ValidationError("Date cannot be in the past")
    
    transaction_id = models.IntegerField(blank=False)
    quantity = models.IntegerField(default=0, blank=False, validators=[validate_quantity])
    date = models.DateField(blank=False, default=now,
                            validators=[validate_date])
    expiry_date = models.DateField(blank=False, default=now, validators=[validate_date])
    batch_id = models.CharField(max_length=100, blank=False)
    medicine = models.ForeignKey(
        Medicine, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.transaction_id)


class CustomerTransaction(Transaction):
    phone_regex = RegexValidator(
        regex=r'^(?:\s+|)((0|(?:(\+|)91))(?:\s|-)*(?:(?:\d(?:\s|-)*\d{9})|(?:\d{2}(?:\s|-)*\d{8})|(?:\d{3}(?:\s|-)*\d{7}))|\d{10})(?:\s+|)', message=("Phone Number is not valid"))

    name = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=14, blank=False,
                             validators=[phone_regex])

    def __str__(self):
        return self.name


class VendorTransaction(Transaction):
    vendor = models.ForeignKey(Vendor, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.vendor.name


class Item(models.Model):
    def validate_date(date):
        if date < date.today():
            pass
            raise ValidationError("Date cannot be in the past")
    def validate_quantity(quan):
        if quan <= 0:
            raise ValidationError("Not a valid quantity.")


    batch_id = models.CharField(max_length=100, blank=False)
    expiry_date = models.DateField(blank=False, default=now, validators=[validate_date])
    order_date = models.DateField(blank=False, default=now, validators=[validate_date])
    quantity = models.IntegerField(
        default=0, blank=False, validators=[validate_quantity])
    medicine = models.ForeignKey(
        Medicine, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.medicine.trade_name



class UsableItem(Item):
    pass


class ExpiredItem(Item):
    pass
