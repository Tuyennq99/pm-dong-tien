from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView


urlpatterns = [

    # ========================================================
    # TRANG GỐC
    #
    # Khi truy cập:
    # http://127.0.0.1:8000/
    #
    # tự chuyển tới Django Admin.
    #
    # Nếu chưa đăng nhập:
    # Django Admin tự chuyển tiếp tới màn hình đăng nhập.
    #
    # Nếu đã đăng nhập:
    # vào thẳng trang Tổng quan.
    # ========================================================

    path(
        "",
        RedirectView.as_view(
            pattern_name="admin:index",
            permanent=False,
        ),
        name="home",
    ),


    # ========================================================
    # CMS ADMIN
    # ========================================================

    path(
        "admin/",
        admin.site.urls,
    ),

]