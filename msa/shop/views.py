from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import UsableItem, Medicine, Vendor, ExpiredItem, CustomerTransaction, VendorTransaction
from .forms import NewMedicineForm, VendorForm, RevenueForm, PasswordChangingForm
from datetime import date
from django.contrib.auth.hashers import check_password




# Create your views here.


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html', {})


def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


@login_excluded('home')
def loginpage(request, backend = None):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect.')
    else:
        list(messages.get_messages(request))
    context = {}
    return render(request, 'loginpage.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def change_password(request):
    currentpassword = request.user.password  # user's current password

    form = PasswordChangingForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            currentpasswordentered = form.cleaned_data.get("old_password")
            password1 = form.cleaned_data.get("new_password1")
            password2 = form.cleaned_data.get("new_password2")

            matchcheck = check_password(currentpasswordentered, currentpassword)
            if matchcheck:
                if password1 == password2:
                    u = request.user
                    u.set_password(password1)
                    u.save()
                    print(password1)
                    messages.success(
                        request, ('Password Was Changed Successfully.'))
                    return render(request, 'home.html', {})
                else:
                    messages.success(
                        request, ('New Passwords do not match.'))
            else:
                messages.success(
                    request, ('Old Password is incorect.'))
        else:
            messages.success(
                request, ('Passwords not Valid.'))
    return render(request, 'change-password.html', {})


@login_required(login_url='login')
def search(request):
    if request.method == "GET":
        usable_item = UsableItem.objects.all()
        search = request.GET.get('search')
        medicine = Medicine.objects.all().filter(
            trade_name__icontains=search) | Medicine.objects.all().filter(generic_name__icontains=search)
        return render(request, 'search.html', {'medicine': medicine, 'usable_item': usable_item})

@login_required(login_url='login')
def listOfMed(request):
    if request.method == "GET":
        usable_item = UsableItem.objects.all()
        medicine = Medicine.objects.all().filter(
            trade_name__icontains='') | Medicine.objects.all().filter(generic_name__icontains='')
        return render(request, 'listOfmed.html', {'medicine': medicine, 'usable_item': usable_item})
        
@login_required(login_url='login')
def newmed(request):
    vendors = Vendor.objects.all
    if request.method == "POST":
        form = NewMedicineForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        else:
            messages.success(
                request, ('There was an error in your form. Please try again...'))
            return render(request, 'newmed.html', {'vendors': vendors})
        messages.success(request, ('Medicine has been added successfully!'))
        return render(request, 'newmed.html', {'vendors': vendors})
    else:
        return render(request, 'newmed.html', {'vendors': vendors})


@login_required(login_url='login')
def below_threshold(request):
    medicine = Medicine.objects.all()
    usable_item = UsableItem.objects.all()
    med_dict = {}
    for meditem in medicine:
        sum = 0
        for item in usable_item:
            if meditem.id == item.medicine.id:
                sum = sum+item.quantity
        med_dict.update({meditem: sum})
    return render(request,
                  'below_threshold.html',
                  {
                      'medicine': medicine,
                      'med_dict': med_dict,
                      'date': date.today()
                  }
                  )

@login_required(login_url='login')
def threshold(request):
    thresholds = Medicine.objects
    new = CustomerTransaction.objects

    quantity = 0

    for a in thresholds.all():
        for b in new.all():
            if(a.trade_name == b.medicine.trade_name):
                quantity += b.quantity
        x = quantity % 7
        quantity /= 7
        if (x > 0):
            quantity += 1
        a.threshold_value = quantity
        a.save()

        quantity = 0

    return render(request, 'threshold.html', {'threshold': thresholds})


@login_required(login_url='login')
def addvendor(request):
    form = VendorForm()
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.success(
                request, ('There was an error in your form. Please try again...'))
            return render(request, 'addvendor.html', {})
        messages.success(request, ('Vendor has been added successfully!'))

    context = {'form': form}
    return render(request, 'addvendor.html', context)


@login_required(login_url='login')
def usable(request):
    usa = UsableItem.objects

    for a in usa.all():
        if(a.expiry_date < date.today()):
            b = ExpiredItem(batch_id=a.batch_id, expiry_date=a.expiry_date,
                            order_date=a.order_date, quantity=a.quantity, medicine=a.medicine)
            b.save()
            a.delete()

    return render(request, 'usable.html', {'usable': usa})


@login_required(login_url='login')
def expired(request):
    usa = UsableItem.objects

    for a in usa.all():
        if(a.expiry_date < date.today()):
            b = ExpiredItem(batch_id=a.batch_id, expiry_date=a.expiry_date,
                            order_date=a.order_date, quantity=a.quantity, medicine=a.medicine)
            b.save()
            a.delete()

    exp = ExpiredItem.objects


    return render(request, 'expired.html', {'expired': exp})


@login_required(login_url='login')
def revenue(request):
    form = RevenueForm()
    if request.method == 'POST':
        form = RevenueForm(request.POST)
        if form.is_valid():
            final_dic = calc(form.cleaned_data)
            return render(request, 'revenue_data.html', final_dic)
        else:
            messages.success(request, ('Please Choose Proper Dates'))


    context = {'form': form}

    return render(request, 'revenue.html', context)



def calc(form):
    start = form['start_date']
    end = form['end_date']
    c_val = 0
    v_val = 0
    c_list = []
    v_list = []

    ct = CustomerTransaction.objects
    v = VendorTransaction.objects

    for i in ct.all():
        if(i.date >= start and i.date <= end):
            price = 0
            c_dict = {}
            price = i.quantity * i.medicine.unit_selling
            c_val += price
            c_dict["transaction_id"] = i.transaction_id
            c_dict["name"] = i.name
            c_dict["trade_name"] = i.medicine.trade_name
            c_dict["vendor"] = i.medicine.vendor
            c_dict["date"] = i.date
            c_dict["quantity"] = i.quantity
            c_dict["c_revenue"] = (i.quantity)*(i.medicine.unit_selling)

            c_list.append(c_dict)

    for i in v.all():
        if(i.date >= start and i.date <= end):
            price = 0
            v_dict = {}
            price = i.quantity * i.medicine.purchasePrice
            v_val += price
            v_dict["transaction_id"] = i.transaction_id
            v_dict["vendor"] = i.vendor
            v_dict["trade_name"] = i.medicine.trade_name
            v_dict["date"] = i.date
            v_dict["quantity"] = i.quantity
            v_dict["v_cost"] = (i.quantity)*(i.medicine.purchasePrice)

            v_list.append(v_dict)

    name_list = []
    name_dict1 = {}
    name_dict1["cus1"] = "Customer Transaction"
    name_dict1["cus2"] = c_val
    name_list.append(name_dict1)

    name_dict2 = {}
    name_dict2["cus1"] = "Vendor Transaction"
    name_dict2["cus2"] = v_val
    name_list.append(name_dict2)

    name_dict3 = {}
    name_dict3["cus1"] = "Net Profit"
    name_dict3["cus2"] = c_val - v_val
    name_list.append(name_dict3)

    final_dic = {}
    final_dic["vendor"] = v_list
    final_dic["customer"] = c_list
    final_dic["name"] = name_list

    return final_dic

@login_required(login_url='login')
def clear_exp(request):
    exp = ExpiredItem.objects
    for a in exp.all():
        a.delete()
    messages.success(request, "ALl the expired items thrown away.")

    return redirect('home')
