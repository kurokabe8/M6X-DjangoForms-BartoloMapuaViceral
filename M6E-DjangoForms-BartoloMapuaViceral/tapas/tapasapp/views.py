from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Account 

def login_view(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = Account.objects.filter(username=u, password=p).first()
        if user:
            return redirect('basic_list', pk=user.pk)
        else:
            return render(request, 'tapasapp/login.html', {'error': 'Invalid login'})

    message = None
    if request.GET.get('created') == '1':
        message = 'Account created successfully'

    return render(request, 'tapasapp/login.html', {'message': message})

def signup_view(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        if Account.objects.filter(username=u).exists():
            return render(request, 'tapasapp/signup.html', {'error': 'Account already exists'})
        else:
            Account.objects.create(username=u, password=p)
            return redirect('/?created=1')
    return render(request, 'tapasapp/signup.html')

def basic_list(request, pk):
    user = get_object_or_404(Account, pk=pk)
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/basic_list.html', {'user': user, 'dishes': dish_objects})

def manage_account(request, pk):
    user = get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/manage_account.html', {'user': user})

def change_password(request, pk):
    user = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        curr_p = request.POST.get('current_password')
        new_p = request.POST.get('new_password')
        conf_p = request.POST.get('confirm_password')

        if curr_p == user.getPassword() and new_p == conf_p:
            user.password = new_p
            user.save()
            return redirect('manage_account', pk=user.pk)
        else:
            return render(request, 'tapasapp/change_password.html', {'user': user, 'error': 'Invalid input'})
            
    return render(request, 'tapasapp/change_password.html', {'user': user})

def delete_account(request, pk):
    Account.objects.filter(pk=pk).delete()
    return redirect('login')

def add_menu(request, pk):
    user = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('basic_list', pk=user.pk)
    else:
        return render(request, 'tapasapp/add_menu.html', {'user': user})

def view_detail(request, user_pk, pk):
    user = get_object_or_404(Account, pk=user_pk)
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'user': user, 'd': d})

def delete_dish(request, user_pk, pk):
    user = get_object_or_404(Account, pk=user_pk)
    Dish.objects.filter(pk=pk).delete()
    return redirect('basic_list', pk=user.pk)

def update_dish(request, user_pk, pk):
    user = get_object_or_404(Account, pk=user_pk)
    if request.method == "POST":
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', user_pk=user.pk, pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'user': user, 'd': d})