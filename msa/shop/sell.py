from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UsableItem, Medicine, CustomerTransaction
from .forms import SellForm
from django.db.models import Sum
from datetime import date




list1 = []


@login_required(login_url='login')
def printreceipt(request, trans):
    trans = int(trans)
    list = []
    context = {}
    context['trans'] = trans
    if CustomerTransaction.objects.filter(transaction_id=trans).count() == 0:
        messages.info(request, 'Transaction ID not valid')
        return redirect('home')
    context['name'] = CustomerTransaction.objects.filter(
        transaction_id=trans).first().name
    context['phone'] = CustomerTransaction.objects.filter(
        transaction_id=trans).first().phone
    context['date'] = CustomerTransaction.objects.filter(
        transaction_id=trans).first().date
    context['total'] = 0

    for obj in CustomerTransaction.objects.filter(transaction_id=trans):
        dict = {'obj': obj,
            'total_price': obj.quantity * obj.medicine.unit_selling
        }
        context['total'] += obj.quantity * obj.medicine.unit_selling
        list.append(dict)
        print(obj.medicine.trade_name)

    context['list'] = list
    return render(request, 'receipt.html', context)



def sellmedicine_update(result, name, phone, trans):
    lis = []
    q = result['quantity']
    amt = 0
    sum = UsableItem.objects.filter(
        medicine=result['medicine']).aggregate(sum=Sum('quantity'))['sum']
    if sum is None or sum < q:
        return None
    for obj in UsableItem.objects.filter(medicine=result['medicine']):
        v = 0
        if amt+obj.quantity <= q:
            amt += obj.quantity
            v = obj.quantity
            obj.delete()
        else:
            obj.quantity -= q-amt
            v = q-amt
            amt += q-amt
            obj.save()
        ctrans = CustomerTransaction(
            transaction_id=trans,
            quantity=v,
            date=date.today(),
            medicine=result['medicine'],
            name=name,
            phone=phone,
            batch_id=obj.batch_id,
            expiry_date=obj.expiry_date,
        )
        ctrans.save(force_insert=True)
        dict = {
            'name': result['medicine'].trade_name,
            'batch_id': obj.batch_id,
            'expiry_date': obj.expiry_date,
            'quantity': v,
            'price': result['medicine'].unit_selling,
            'total_price': result['medicine'].unit_selling * v
        }
        lis.append(dict)
        if amt == q:
            break

    return lis


@login_required(login_url='login')
def sellmedicine(request):
    global list1

    medicines = Medicine.objects.order_by('trade_name')
    context = {'medicines': medicines, 'list': [], 'total': 0}
    # context['form'] = SellForm(request.POST)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        trans = request.POST.get('trans')
        details = SellForm(request.POST)
        context['form'] = details
        if details.is_valid():
            result = details.cleaned_data
            lis = sellmedicine_update(
                result, name, phone, trans)
            if lis is not None:
                list1 = list1 + lis
            else:
                messages.info(request, 'Enough Quantity is not available')
        else:
            messages.info(request, 'Please enter valid data')
        context['list'] = list1
        if name != "":
            context['name'] = name
        if phone != "":
            context['phone'] = phone
        context['trans'] = trans
        for item in list1:
            context['total'] += item['total_price'] 
    else:
        list1 = []
        print("GET method")
        if CustomerTransaction.objects.count() != 0:
            trans = CustomerTransaction.objects.last().transaction_id+1
        else:
            trans = 1
        context['trans'] = trans


    return render(request, 'sellmedicine.html', context)
