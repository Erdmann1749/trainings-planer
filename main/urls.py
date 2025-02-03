from django.urls import path
from . import views

urlpatterns  = [
    path("", views.login, name="login"),
    path("add-contacts/", views.addcontacts, name="addcontacts"),
    path("create-group/", views.creategroup, name="creategroup"),
    path("group-details/", views.groupdetailspage, name="groupdetailspage"),
    path("calendar/", views.calendarview, name="calendarview"),
]