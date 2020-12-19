from django.urls import path
from rooms import views as room_views

urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]

app_name = "core"
