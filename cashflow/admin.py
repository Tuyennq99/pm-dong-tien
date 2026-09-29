
from django.urls import reverse
from django.utils.html import format_html

from datetime import date
from django import forms
from django.contrib import admin
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.response import TemplateResponse
from django.utils import timezone



from .models import (
    Account,
    Counterparty,
    Order,
    Transaction,
    TransactionEntry,
)


# ============================================================
# FORM GIAO DỊCH
# ============================================================

class TransactionAdminForm(forms.ModelForm):

    account = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        label="Tài khoản biến động",
        required=True,
    )

    class Meta:
        model = Transaction

        fields = [
            "transaction_date",
            "transaction_type",
            "account",
            "counterparty",
            "order",
            "amount",
            "description",
            "status",
        ]

        widgets = {
            "transaction_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["account"].queryset = (
            Account.objects
            .filter(is_active=True)
            .order_by("code", "name")
        )

        self.fields["transaction_type"].choices = [
            (
                Transaction.TransactionType.INCOME,
                "Thu",
            ),
            (
                Transaction.TransactionType.EXPENSE,
                "Chi",
            ),
        ]

        if self.instance and self.instance.pk:

            entry = (
                self.instance.entries
                .select_related("account")
                .order_by("id")
                .first()
            )

            if entry:
                self.fields["account"].initial = entry.account


# ============================================================
# TÀI KHOẢN
# ============================================================
# List ngân hàng
BANK_CHOICES = [
    ("MBB", "MB Bank"),
    ("TCB", "Techcombank"),
    ("VCB", "Vietcombank"),
    ("BIDV", "BIDV"),
    ("ACB", "ACB"),
    ("VPB", "VPBank"),
    ("CTG", "VietinBank"),
    ("AGR", "Agribank"),
    ("TPB", "TPBank"),
    ("STB", "Sacombank"),
    ("VIB", "VIB"),
    ("SHB", "SHB"),
    ("MSB", "MSB"),
    ("OCB", "OCB"),
    ("HDB", "HDBank"),
    ("SEA", "SeABank"),
    ("LPB", "LPBank"),
    ("EIB", "Eximbank"),
]

class AdminRowActionsMixin:
    class Media:
        css = {
            "all": ("cashflow/css/transaction_list.css",)
        }

    @admin.display(description="Thao tác")
    def row_actions(self, obj):
        opts = obj._meta

        edit_url = reverse(
            f"admin:{opts.app_label}_{opts.model_name}_change",
            args=[obj.pk],
        )

        delete_url = reverse(
            f"admin:{opts.app_label}_{opts.model_name}_delete",
            args=[obj.pk],
        )

        return format_html(
            '<div class="transaction-actions">'
            '<a class="action-link edit" href="{}">Sửa</a>'
            '<a class="action-link delete" href="{}">Xóa</a>'
            '</div>',
            edit_url,
            delete_url,
        )

    def changeform_view(
        self,
        request,
        object_id=None,
        form_url="",
        extra_context=None,
    ):
        extra_context = extra_context or {}

        # Chỉ giữ nút Lưu giống form Giao dịch
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False
        extra_context["show_delete_link"] = False

        return super().changeform_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )
    @admin.display(description="Thao tác")
    def row_actions(self, obj):
        opts = obj._meta

        edit_url = reverse(
            f"admin:{opts.app_label}_{opts.model_name}_change",
            args=[obj.pk],
        )

        delete_url = reverse(
            f"admin:{opts.app_label}_{opts.model_name}_delete",
            args=[obj.pk],
        )

        return format_html(
            '<div class="transaction-actions">'
            '<a class="action-link edit" href="{}">Sửa</a>'
            '<a class="action-link delete" href="{}">Xóa</a>'
            '</div>',
            edit_url,
            delete_url,
        )
@admin.register(Account)
class AccountAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    change_list_template = "admin/cashflow/shared/change_list.html"



    @admin.display(
    description="Số dư ban đầu",
    ordering="opening_balance",
)
    def opening_balance_display(self, obj):
        return f"{obj.opening_balance:,.0f}".replace(",", ".")





    class Media:
        css = {
            "all": ("cashflow/css/transaction_list.css",)
        }
    actions = None


    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False

        return super().changeform_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

        
    list_display = [
        "code",
        "name",
        "account_number",
        "account_type",
        "opening_balance_display",
        "opening_date",
        "is_active",
        "row_actions",
    ]

    list_filter = [
        # "account_type",
        # "is_active",
    ]

    search_fields = [
        "code",
        "name",
        "account_number",
    ]

    def get_form(self, request, obj=None, **kwargs):
            if obj is None and request.GET.get("bank") == "1":
                kwargs["exclude"] = ["account_type"]

            return super().get_form(request, obj, **kwargs)


    def save_model(self, request, obj, form, change):
            if not change and request.GET.get("bank") == "1":
                obj.account_type = "BANK"

            super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
            if db_field.name == "name" and request.GET.get("bank") == "1":
                kwargs["widget"] = forms.Select(
                    choices=[("", "---------")] + BANK_CHOICES
                )

            return super().formfield_for_dbfield(
                db_field,
                request,
                **kwargs,
    )

    
    ordering = [
        "code",
        "name",
    ]


# ============================================================
# NGƯỜI GỬI / NHẬN
# ============================================================

@admin.register(Counterparty)
class CounterpartyAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    change_list_template = "admin/cashflow/shared/change_list.html"

    class Media:
        css = {
            "all": ("cashflow/css/transaction_list.css",)
        }
    actions = None
# Hiển thị nút lưu ở form
    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False

        return super().changeform_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
    )
    list_display = [
        "code",
        "name",
        "counterparty_type",
        "is_active",
        "row_actions",
    ]

    list_filter = [
        # "counterparty_type",
        "is_active",
    ]

    search_fields = [
        "code",
        "name",
        "tax_code",
        "address",
    ]

    ordering = [
        "name",
    ]


# ============================================================
# ĐƠN HÀNG
# ============================================================


class OrderAdminForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in [
            "order_type",
            "code",
            "name",
            "customer",
            "status",
        ]:
            if field_name in self.fields:
                self.fields[field_name].required = True
@admin.register(Order)
class OrderAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    change_list_template = "admin/cashflow/shared/change_list.html"
    form = OrderAdminForm
    actions = None
# Ẩn ký tự ở thêm form
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(
            db_field,
            request,
            **kwargs,
        )
        if db_field.name == "customer" and formfield:
            widget = formfield.widget
            if hasattr(widget, "can_add_related"):
                widget.can_add_related = False
                widget.can_change_related = False
                widget.can_delete_related = False
                widget.can_view_related = False

        return formfield
# /////////////
    list_display = [
        "code",
        "name",
        "customer",
        "status",
        "order_type",
        "row_actions",
    ]

    list_filter = [
        "order_type",
        "status",
        "customer",
    ]

    search_fields = [
        "code",
        "name",
        "customer__name",
    ]

    ordering = ["-id"]


# ============================================================
# GIAO DỊCH
# ============================================================

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    form = TransactionAdminForm

    change_list_template = (
        "admin/cashflow/transaction/change_list.html"
    )

    ordering = [
        "-transaction_date",
        "-id",
    ]


    # ========================================================
    # QUERYSET
    # ========================================================

    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        return (
            queryset
            .filter(is_deleted=False)
            .select_related(
                "counterparty",
                "order",
                "updated_by",
            )
            .prefetch_related(
                "entries__account",
            )
        )


    # ========================================================
    # DANH SÁCH GIAO DỊCH CUSTOM
    # ========================================================

    def changelist_view(
        self,
        request,
        extra_context=None,
    ):

        queryset = self.get_queryset(request)


        # ----------------------------------------------------
        # TỪ NGÀY
        # ----------------------------------------------------

        date_from = request.GET.get(
            "from",
            "",
        )

        if date_from:

            try:

                parsed_date = date.fromisoformat(
                    date_from
                )

                queryset = queryset.filter(
                    transaction_date__gte=parsed_date
                )

            except ValueError:
                pass


        # ----------------------------------------------------
        # ĐẾN NGÀY
        # ----------------------------------------------------

        date_to = request.GET.get(
            "to",
            "",
        )

        if date_to:

            try:

                parsed_date = date.fromisoformat(
                    date_to
                )

                queryset = queryset.filter(
                    transaction_date__lte=parsed_date
                )

            except ValueError:
                pass


        # ----------------------------------------------------
        # THU / CHI
        # ----------------------------------------------------

        transaction_type = request.GET.get(
            "type",
            "",
        )

        valid_types = {
            Transaction.TransactionType.INCOME,
            Transaction.TransactionType.EXPENSE,
        }

        if transaction_type in valid_types:

            queryset = queryset.filter(
                transaction_type=transaction_type
            )


        # ----------------------------------------------------
        # TÀI KHOẢN
        # ----------------------------------------------------

        account_id = request.GET.get(
            "account",
            "",
        )

        if account_id.isdigit():

            queryset = queryset.filter(
                entries__account_id=int(account_id)
            )


        # ----------------------------------------------------
        # TÌNH TRẠNG
        # ----------------------------------------------------

        status = request.GET.get(
            "status",
            "",
        )

        valid_statuses = {
            value
            for value, label
            in Transaction.Status.choices
        }

        if status in valid_statuses:

            queryset = queryset.filter(
                status=status
            )


        # ----------------------------------------------------
        # TÌM KIẾM
        # ----------------------------------------------------

        keyword = request.GET.get(
            "q",
            "",
        ).strip()

        if keyword:

            queryset = queryset.filter(

                Q(code__icontains=keyword)

                | Q(
                    order__code__icontains=keyword
                )

                | Q(
                    order__name__icontains=keyword
                )

                | Q(
                    counterparty__name__icontains=keyword
                )

                | Q(
                    description__icontains=keyword
                )

            )


        queryset = (
            queryset
            .distinct()
            .order_by(
                "-transaction_date",
                "-id",
            )
        )


        # ----------------------------------------------------
        # PHÂN TRANG
        # ----------------------------------------------------

        paginator = Paginator(
            queryset,
            10,
        )

        page_number = request.GET.get(
            "page",
            1,
        )

        page_obj = paginator.get_page(
            page_number
        )


        # ----------------------------------------------------
        # GIỮ FILTER KHI CHUYỂN TRANG
        # ----------------------------------------------------

        query_params = request.GET.copy()

        if "page" in query_params:
            query_params.pop("page")

        base_query = query_params.urlencode()


        # ----------------------------------------------------
        # CONTEXT
        # ----------------------------------------------------

        context = {

            **self.admin_site.each_context(
                request
            ),

            "title": "Giao dịch",

            "opts": self.model._meta,

            "transactions": (
                page_obj.object_list
            ),

            "page_obj": page_obj,

            "paginator": paginator,

            "base_query": base_query,

            "accounts": (
                Account.objects
                .filter(is_active=True)
                .order_by(
                    "code",
                    "name",
                )
            ),

            "transaction_types": [
                (
                    Transaction.TransactionType.INCOME,
                    "Thu",
                ),
                (
                    Transaction.TransactionType.EXPENSE,
                    "Chi",
                ),
            ],

            "statuses": (
                Transaction.Status.choices
            ),

            "filter_from": date_from,

            "filter_to": date_to,

            "filter_type": transaction_type,

            "filter_account": account_id,

            "filter_status": status,

            "filter_q": keyword,

            "transaction_count": (
                paginator.count
            ),

            "has_add_permission": (
                self.has_add_permission(
                    request
                )
            ),

            "media": self.media,
        }

        if extra_context:

            context.update(
                extra_context
            )

        return TemplateResponse(
            request,
            self.change_list_template,
            context,
        )


    # ========================================================
    # LƯU GIAO DỊCH
    # ========================================================

    def save_model(
        self,
        request,
        obj,
        form,
        change,
    ):

        obj.updated_by = request.user

        if not change:
            obj.created_by = request.user

        super().save_model(
            request,
            obj,
            form,
            change,
        )


        # ----------------------------------------------------
        # SINH MÃ GIAO DỊCH
        # ----------------------------------------------------

        if not obj.code:

            obj.code = (
                f"GD{obj.pk:06d}"
            )

            obj.save(
                update_fields=[
                    "code",
                ]
            )


        account = (
            form.cleaned_data["account"]
        )


        # ----------------------------------------------------
        # HƯỚNG TIỀN
        # ----------------------------------------------------

        if (
            obj.transaction_type
            == Transaction.TransactionType.INCOME
        ):

            direction = (
                TransactionEntry.Direction.IN
            )

        else:

            direction = (
                TransactionEntry.Direction.OUT
            )


        # ----------------------------------------------------
        # ENTRY
        # ----------------------------------------------------

        entry = (
            obj.entries
            .order_by("id")
            .first()
        )


        if entry:

            entry.account = account

            entry.direction = direction

            entry.amount = obj.amount

            entry.save(
                update_fields=[
                    "account",
                    "direction",
                    "amount",
                ]
            )

            keep_entry = entry


        else:

            keep_entry = (
                TransactionEntry.objects.create(
                    transaction=obj,
                    account=account,
                    direction=direction,
                    amount=obj.amount,
                )
            )


        # Phase demo:
        # Thu/Chi chỉ có đúng một entry.
        obj.entries.exclude(
            pk=keep_entry.pk
        ).delete()


    # ========================================================
    # XÓA MỀM 1 GIAO DỊCH
    # ========================================================

    def delete_model(
        self,
        request,
        obj,
    ):

        obj.is_deleted = True

        obj.deleted_at = (
            timezone.now()
        )

        obj.deleted_by = (
            request.user
        )

        obj.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "deleted_by",
            ]
        )


    # ========================================================
    # XÓA MỀM NHIỀU GIAO DỊCH
    # ========================================================

    def delete_queryset(
        self,
        request,
        queryset,
    ):

        queryset.update(

            is_deleted=True,

            deleted_at=timezone.now(),

            deleted_by_id=request.user.pk,

        )


# ============================================================
# BIẾN ĐỘNG TÀI KHOẢN
# ============================================================

@admin.register(TransactionEntry)
class TransactionEntryAdmin(admin.ModelAdmin):

    list_display = [
        "transaction",
        "account",
        "direction",
        "amount",
        "created_at",
    ]

    readonly_fields = [
        "transaction",
        "account",
        "direction",
        "amount",
        "created_at",
    ]


    # --------------------------------------------------------
    # ẨN KHỎI MENU ADMIN
    # --------------------------------------------------------

    def get_model_perms(
        self,
        request,
    ):

        return {}


    # --------------------------------------------------------
    # KHÔNG CHO TẠO ENTRY TRỰC TIẾP
    # --------------------------------------------------------

    def has_add_permission(
        self,
        request,
    ):

        return False


    # --------------------------------------------------------
    # KHÔNG CHO SỬA ENTRY TRỰC TIẾP
    # --------------------------------------------------------

    def has_change_permission(
        self,
        request,
        obj=None,
    ):

        return False


    # --------------------------------------------------------
    # QUYỀN XÓA
    #
    # Khi xóa Transaction, Django kiểm tra luôn quyền xóa
    # TransactionEntry liên quan.
    #
    # Ta cho phép bước kiểm tra này nếu request hiện tại
    # chính là màn xóa Transaction.
    #
    # Nếu người dùng cố vào URL xóa TransactionEntry trực tiếp,
    # vẫn bị chặn.
    # --------------------------------------------------------

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):

        resolver_match = getattr(
            request,
            "resolver_match",
            None,
        )

        if not resolver_match:
            return False

        return (
            resolver_match.url_name
            == "cashflow_transaction_delete"
        )


# ============================================================
# ADMIN
# ============================================================

admin.site.site_header = (
    "PM DÒNG TIỀN"
)

admin.site.site_title = (
    "PM Dòng Tiền"
)

admin.site.index_title = (
    "Tổng quan"
)

admin.site.enable_nav_sidebar = True