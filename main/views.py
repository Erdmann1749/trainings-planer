from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("addcontacts")  # Wo der Nutzer nach dem Login hingeleitet wird
        else:
            messages.error(request, "Ungültige Anmeldeinformationen")
    return render(request, "main/login.html")

def custom_logout(request):
    logout(request)
    return redirect("login")


def addcontacts(request):
    return render(request, "main/addcontacts.html")

def creategroup(request):
    return render(request, "main/creategroup.html")

def groupdetailspage(request):
    return render(request, "main/groupdetailspage.html")

def calendarview(request):
    return render(request, "main/calendarview.html")