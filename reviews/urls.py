from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("create_review/<int:room>/", views.create_review, name="create-review")
]
