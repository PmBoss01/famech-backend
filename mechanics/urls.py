from django.urls import path

from mechanics.views import MechanicProfileView

app_name = "mechanics"

urlpatterns = [
    path("profile/", MechanicProfileView.as_view(), name="profile"),
]
