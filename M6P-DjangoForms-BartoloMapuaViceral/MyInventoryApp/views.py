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