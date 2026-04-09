from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Supplier, WaterBottle

current_account_id = None

def login_view(request):
    message = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            Account.objects.get(username=username, password=password)
            return redirect('view_supplier')
        except:
            message = "Invalid login"

    return render(request, "MyInventoryApp/login.html", {"message": message})


def signup_view(request):
    message = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if Account.objects.filter(username=username).exists():
            message = "Account already exists"
        else:
            Account.objects.create(username=username, password=password)
            return redirect('login')

    return render(request, "MyInventoryApp/signup.html", {"message": message})


def view_supplier(request):
    suppliers = Supplier.objects.all()
    return render(request, "MyInventoryApp/supplier_list.html", {"suppliers": suppliers})


def view_bottles(request):
    bottles = WaterBottle.objects.all()
    return render(request, "MyInventoryApp/bottle_list.html", {"bottles": bottles})


def view_bottle_details(request, pk):
    bottle = get_object_or_404(WaterBottle, pk=pk)

    if request.method == "POST":
        WaterBottle.objects.filter(pk=pk).delete()
        return redirect('view_bottles')

    return render(request, "MyInventoryApp/view_bottle_details.html", {"bottle": bottle})

def add_bottle(request):
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('view_supplier')

        sku = request.POST.get("sku")
        brand = request.POST.get("brand")
        cost = request.POST.get("cost")
        size = request.POST.get("size")
        mouth_size = request.POST.get("mouth_size")
        color = request.POST.get("color")
        supplied_by_id = request.POST.get("supplied_by")
        current_quantity = request.POST.get("current_quantity")

        supplier = get_object_or_404(Supplier, pk=supplied_by_id)

        WaterBottle.objects.create(
            sku=sku,
            brand=brand,
            cost=cost,
            size=size,
            mouth_size=mouth_size,
            color=color,
            supplied_by=supplier,
            current_quantity=current_quantity
        )

        return redirect('view_supplier')

    return render(request, "MyInventoryApp/bottle_add.html", {"suppliers": suppliers})

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, "MyInventoryApp/manage_account.html", {"account": account})


def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    message = ""

    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('manage_account', pk=account.pk)

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if current_password == account.password and new_password == confirm_password:
            account.password = new_password
            account.save()
            return redirect('manage_account', pk=account.pk)
        else:
            message = "Password change failed"

    return render(request, "MyInventoryApp/change_password.html", {
        "account": account,
        "message": message
    })