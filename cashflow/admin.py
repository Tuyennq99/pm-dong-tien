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

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = [
        "code",
        "name",
        "account_type",
        "opening_balance",
        "opening_date",
        "is_active",
    ]

    list_filter = [
        "account_type",
        "is_active",
    ]

    search_fields = [
        "code",
        "name",
        "account_number",
    ]

    ordering = [
        "code",
        "name",
    ]


# ============================================================
# NGƯỜI GỬI / NHẬN
# ============================================================

@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):

    list_display = [
        "code",
        "name",
        "counterparty_type",
        "is_active",
    ]

    list_filter = [
        "counterparty_type",
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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        "code",
        "name",
        "customer",
        "status",
    ]

    list_filter = [
        "status",
    ]

    search_fields = [
        "code",
        "name",
        "customer__name",
    ]

    ordering = [
        "code",
    ]


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