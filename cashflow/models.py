from django.conf import settings
from django.db import models
from django.db.models import Q


# =========================================================
# 1. TÀI KHOẢN / NGUỒN TIỀN
# Ví dụ: Tiền mặt, MB, BIDV, TPBank...
# =========================================================
class Account(models.Model):

    class AccountType(models.TextChoices):
        CASH = "CASH", "Tiền mặt"
        BANK = "BANK", "Ngân hàng"
        OTHER = "OTHER", "Khác"

    code = models.CharField(
        "Mã tài khoản",
        max_length=30,
        unique=True,
    )

    name = models.CharField(
        "Tên tài khoản",
        max_length=255,
    )

    account_type = models.CharField(
        "Loại tài khoản",
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.BANK,
    )

    opening_balance = models.DecimalField(
        "Số dư ban đầu",
        max_digits=20,
        decimal_places=2,
        default=0,
    )

    opening_date = models.DateField(
        "Ngày bắt đầu",
    )

    account_number = models.CharField(
        "Số tài khoản",
        max_length=100,
        blank=True,
    )

    note = models.TextField(
        "Ghi chú",
        blank=True,
    )

    is_active = models.BooleanField(
        "Đang sử dụng",
        default=True,
    )

    created_at = models.DateTimeField(
        "Ngày tạo",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Ngày cập nhật",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Tài khoản"
        verbose_name_plural = "Tài khoản"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


# =========================================================
# 2. NGƯỜI GỬI / NHẬN
# Dùng chung cho khách hàng, NCC, nhân viên...
# =========================================================
class Counterparty(models.Model):

    class CounterpartyType(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Khách hàng"
        SUPPLIER = "SUPPLIER", "Nhà cung cấp"
        EMPLOYEE = "EMPLOYEE", "Nhân viên"
        OTHER = "OTHER", "Khác"

    code = models.CharField(
        "Mã đối tác",
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )

    name = models.CharField(
        "Tên người gửi / nhận",
        max_length=255,
    )

    counterparty_type = models.CharField(
        "Loại đối tác",
        max_length=20,
        choices=CounterpartyType.choices,
        default=CounterpartyType.OTHER,
    )

    tax_code = models.CharField(
        "Mã số thuế",
        max_length=50,
        blank=True,
    )

    address = models.CharField(
        "Địa chỉ",
        max_length=500,
        blank=True,
    )

    note = models.TextField(
        "Ghi chú",
        blank=True,
    )

    is_active = models.BooleanField(
        "Đang sử dụng",
        default=True,
    )

    created_at = models.DateTimeField(
        "Ngày tạo",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Ngày cập nhật",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Người gửi / nhận"
        verbose_name_plural = "Người gửi / nhận"
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================================================
# 3. ĐƠN HÀNG / ĐẦU VIỆC
# Ví dụ:
# - Máy nghiền SIM2000
# - Chi phí cố định
# =========================================================
class Order(models.Model):
    class OrderType(models.TextChoices):
        REPAIR = "REPAIR", "Sửa chữa"
        PRODUCTION = "PRODUCTION", "Sản xuất"
        DEVELOPMENT = "DEVELOPMENT", "Phát triển"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Đang thực hiện"
        COMPLETED = "COMPLETED", "Hoàn thành"
        INACTIVE = "INACTIVE", "Ngừng sử dụng"


    order_type = models.CharField(
        max_length=20,
        choices=OrderType.choices,
        blank=True,
        default="",
        verbose_name="Loại đơn hàng",
    )

    code = models.CharField(
        "Mã đơn hàng",
        max_length=30,
        unique=True,
    )

    name = models.CharField(
        "Tên đơn hàng",
        max_length=255,
    )

    customer = models.ForeignKey(
        Counterparty,
        on_delete=models.PROTECT,
        verbose_name="Khách hàng",
    )

    status = models.CharField(
        "Tình trạng",
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    note = models.TextField(
        blank=True,
        verbose_name="Ghi chú",
    )

    created_at = models.DateTimeField(
        "Ngày tạo",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Ngày cập nhật",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


# =========================================================
# 4. GIAO DỊCH
# Đây là dữ liệu người dùng nhìn thấy:
# ngày, thu/chi, người gửi nhận, đơn hàng, số tiền...
# =========================================================
class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = "INCOME", "Thu"
        EXPENSE = "EXPENSE", "Chi"

        # Chưa cần dùng ở Phase 1.
        # Để sẵn để sau này mở rộng chuyển tiền nội bộ.
        TRANSFER = "TRANSFER", "Chuyển nội bộ"

    class Status(models.TextChoices):
        APPROVED = "APPROVED", "Đã duyệt - chưa thực hiện"
        COMPLETED = "COMPLETED", "Đã thực hiện"

    code = models.CharField(
        "Mã giao dịch",
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )

    transaction_date = models.DateField(
        "Ngày phát sinh",
    )

    transaction_type = models.CharField(
        "Thu / Chi",
        max_length=20,
        choices=TransactionType.choices,
    )

    order = models.ForeignKey(
        Order,
        verbose_name="Đơn hàng",
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    counterparty = models.ForeignKey(
        Counterparty,
        verbose_name="Người gửi / nhận",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="transactions",
    )

    amount = models.DecimalField(
        "Số tiền",
        max_digits=20,
        decimal_places=2,
    )

    description = models.TextField(
        "Nội dung",
        blank=True,
    )

    status = models.CharField(
        "Tình trạng",
        max_length=20,
        choices=Status.choices,
        default=Status.COMPLETED,
    )

    created_at = models.DateTimeField(
        "Ngày tạo",
        auto_now_add=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Người tạo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_cashflow_transactions",
    )

    updated_at = models.DateTimeField(
        "Ngày cập nhật",
        auto_now=True,
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Người cập nhật",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_cashflow_transactions",
    )

    # Xóa mềm:
    # Người dùng bấm Xóa nhưng dữ liệu vẫn còn để truy vết.
    is_deleted = models.BooleanField(
        "Đã xóa",
        default=False,
    )

    deleted_at = models.DateTimeField(
        "Ngày xóa",
        null=True,
        blank=True,
    )

    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Người xóa",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deleted_cashflow_transactions",
    )

    class Meta:
        verbose_name = "Giao dịch"
        verbose_name_plural = "Giao dịch"

        ordering = [
            "-transaction_date",
            "-id",
        ]

        indexes = [
            models.Index(
                fields=["transaction_date"],
            ),
            models.Index(
                fields=["status", "transaction_date"],
            ),
            models.Index(
                fields=["transaction_type", "transaction_date"],
            ),
        ]

        constraints = [
            models.CheckConstraint(
                check=Q(amount__gt=0),
                name="transaction_amount_gt_zero",
            ),
        ]

    def __str__(self):
        return (
            f"{self.get_transaction_type_display()} - "
            f"{self.amount:,.2f}"
        )


# =========================================================
# 5. BIẾN ĐỘNG TÀI KHOẢN
#
# Ví dụ:
#
# Thu 100 triệu vào MB:
# MB | IN | 100 triệu
#
# Chi 30 triệu từ BIDV:
# BIDV | OUT | 30 triệu
#
# Sau này chuyển MB -> BIDV 50 triệu:
# MB   | OUT | 50 triệu
# BIDV | IN  | 50 triệu
# =========================================================
class TransactionEntry(models.Model):

    class Direction(models.TextChoices):
        IN = "IN", "Tiền vào"
        OUT = "OUT", "Tiền ra"

    transaction = models.ForeignKey(
        Transaction,
        verbose_name="Giao dịch",
        on_delete=models.CASCADE,
        related_name="entries",
    )

    account = models.ForeignKey(
        Account,
        verbose_name="Tài khoản biến động",
        on_delete=models.PROTECT,
        related_name="entries",
    )

    direction = models.CharField(
        "Chiều biến động",
        max_length=10,
        choices=Direction.choices,
    )

    amount = models.DecimalField(
        "Số tiền",
        max_digits=20,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        "Ngày tạo",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Biến động tài khoản"
        verbose_name_plural = "Biến động tài khoản"

        indexes = [
            models.Index(
                fields=["account", "direction"],
            ),
        ]

        constraints = [
            models.CheckConstraint(
                check=Q(amount__gt=0),
                name="transaction_entry_amount_gt_zero",
            ),
        ]

        

    def __str__(self):
        return (
            f"{self.transaction_id} - "
            f"{self.account.name} - "
            f"{self.get_direction_display()} - "
            f"{self.amount:,.2f}"
        )

    