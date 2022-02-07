from django.contrib import admin
from .models import Medicine, Vendor
from .models import VendorTransaction, CustomerTransaction
from .models import ExpiredItem, UsableItem


# Register your models here.

admin.site.register(Vendor)
admin.site.register(Medicine)
admin.site.register(ExpiredItem)
admin.site.register(UsableItem)
admin.site.register(CustomerTransaction)
admin.site.register(VendorTransaction)
