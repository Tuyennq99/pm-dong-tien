from django.urls import path
from . import views


app_name = "cashflow"


urlpatterns = [
    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "nhap-lieu/",
        views.transaction_create,
        name="transaction_create",
    ),

    path(
        "danh-sach/",
        views.transaction_list,
        name="transaction_list",
    ),
]