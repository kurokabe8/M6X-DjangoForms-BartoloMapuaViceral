from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Supplier, WaterBottle

def view_supplier(request):
    suppliers = Supplier.objects.all()
    return render(request, "MyInventoryApp/supplier_list.html", {"suppliers": suppliers})
A
def view_bottles(request):
    bottles = WaterBottle.objects.all()
    return render(request, "MyInventoryApp/bottle_list.html", {"bottles": bottles})

def add_bottle(request):
    return render(request, "MyInventoryApp/bottle_add.html")
