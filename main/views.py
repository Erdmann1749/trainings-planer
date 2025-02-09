from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddStudentForm
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

User = get_user_model()


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

@login_required
def addcontacts(request):
    logger.info(f"Role of user: {request.user.role}")

    if request.user.role == "student":
        return redirect("groupdetailspage")  # Schüler dürfen diese Seite nicht sehen

    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("addcontacts")
    else:
        form = AddStudentForm()

    return render(request, "main/addcontacts.html", {"form": form})

def creategroup(request):
    return render(request, "main/creategroup.html")

def groupdetailspage(request):
    print(f"Role of user: {request.user.role}")
    return render(request, "main/groupdetailspage.html")

def calendarview(request):
    return render(request, "main/calendarview.html")