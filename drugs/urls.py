from django.urls import path
from . import views

urlpatterns = [
    path("create/<int:user_id>", views.DrugCreateView.as_view(), name="create-drug"),
    # path("delete/<int:pill_id>/", views.DrugDeleteView.as_view(), name="delete-drug"),
]
