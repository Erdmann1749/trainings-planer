from django.shortcuts import render

def login(request):
    return render(request, "main/login.html")

def addcontacts(request):
    return render(request, "main/addcontacts.html")

def creategroup(request):
    return render(request, "main/creategroup.html")

def groupdetailspage(request):
    return render(request, "main/groupdetailspage.html")

def calendarview(request):
    return render(request, "main/calendarview.html")