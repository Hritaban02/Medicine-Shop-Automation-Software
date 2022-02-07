from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UsableItem, Vendor, VendorTransaction, Medicine
from .forms import ItemForm
from datetime import date


# @login_required(login_url='login')
def newsupply(request):
    vendors = Vendor.objects
    # print(vendors.count())
    context = {'vendors': vendors}
    return render(request, 'newsupply.html', context)


list2 = []


@login_required(login_url='login')
def printvendorreceipt(request, trans):
    trans = int(trans)
    list = []
    context = {}
    context['trans'] = trans
    if VendorTransaction.objects.filter(transaction_id=trans).count() == 0:
        messages.info(request, 'Transaction ID not valid')
        return redirect('home')
    context['name'] = VendorTransaction.objects.filter(
        transaction_id=trans).first().vendor.name
    context['phone'] = VendorTransaction.objects.filter(
        transaction_id=trans).first().vendor.phone
    context['address'] = VendorTransaction.objects.filter(
        transaction_id=trans).first().vendor.address
    context['email'] = VendorTransaction.objects.filter(
        transaction_id=trans).first().vendor.email
    context['date'] = VendorTransaction.objects.filter(
        transaction_id=trans).first().date
    context['total'] = 0

    for obj in VendorTransaction.objects.filter(transaction_id=trans):
        dict = {'obj': obj,
                'total_price': obj.quantity * obj.medicine.purchasePrice
                }
        context['total'] += obj.quantity * obj.medicine.purchasePrice
        list.append(dict)
        print(obj.medicine.trade_name)

    context['list'] = list
    return render(request, 'vendorreceipt.html', context)


@login_required(login_url='login')
def newsupplymed(request, id):
    vendor = Vendor.objects.get(id=id)
    medicines = Medicine.objects.filter(vendor=vendor).order_by('trade_name')
    context = {'vendor': vendor,
               'medicines': medicines,
               'list': [],
               'total': 0 
               }
    # context['form'] = ItemForm(request.POST, vendor)
    global list2
    if medicines.count() == 0:
        messages.info(request, 'This Vendor Supplies No Medicine')
    if request.method == 'POST':
        details = ItemForm(request.POST, vendor)
        trans = request.POST.get('trans')
        if details.is_valid():
            result = details.cleaned_data
            result['price'] = result['medicine'].purchasePrice
            result['total_price'] = result['medicine'].purchasePrice * \
                result['quantity']
            list2.append(result)
            vtrans = VendorTransaction(
                transaction_id=trans,
                quantity=result['quantity'],
                date=result['order_date'],
                medicine=result['medicine'],
                vendor=vendor,
                batch_id=result['batch_id'],
                expiry_date=result['expiry_date'],
            )
            vtrans.save()
            obj = UsableItem(
                batch_id=result['batch_id'],
                expiry_date=result['expiry_date'],
                order_date=result['order_date'],
                quantity=result['quantity'],
                medicine=result['medicine']
            )
            obj.save()
        else:
            messages.info(request, 'Please enter valid data')
        context['list'] = list2
        context['trans'] = trans
        for item in list2:
            context['total'] += item['total_price']
    else:
        list2 = []
        if VendorTransaction.objects.count() != 0:
            trans = VendorTransaction.objects.last().transaction_id+1
        else:
            trans = 1
        context['trans'] = trans
    return render(request, 'newsupplymed.html', context)
