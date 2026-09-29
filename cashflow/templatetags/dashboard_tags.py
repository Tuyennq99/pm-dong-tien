from datetime import date, timedelta
from decimal import Decimal

from django import template
from django.db.models import Sum

from cashflow.models import (
    Account,
    Transaction,
    TransactionEntry,
)


register = template.Library()


def parse_date(value, default):
    """
    Chuyển chuỗi YYYY-MM-DD thành date.
    Nếu không hợp lệ thì dùng giá trị mặc định.
    """
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return default


def account_balance(account, to_date=None):
    """
    Tính số dư của một tài khoản.

    Số dư =
        Số dư ban đầu
        + tổng tiền vào đã thực hiện
        - tổng tiền ra đã thực hiện

    Không tính:
    - Giao dịch chưa thực hiện
    - Giao dịch đã xóa mềm
    """

    entries = TransactionEntry.objects.filter(
        account=account,
        transaction__status=Transaction.Status.COMPLETED,
        transaction__is_deleted=False,
    )

    if to_date:
        entries = entries.filter(
            transaction__transaction_date__lte=to_date
        )

    money_in = (
        entries
        .filter(
            direction=TransactionEntry.Direction.IN
        )
        .aggregate(
            total=Sum("amount")
        )
        ["total"]
        or Decimal("0")
    )

    money_out = (
        entries
        .filter(
            direction=TransactionEntry.Direction.OUT
        )
        .aggregate(
            total=Sum("amount")
        )
        ["total"]
        or Decimal("0")
    )

    return (
        account.opening_balance
        + money_in
        - money_out
    )


@register.simple_tag(takes_context=True)
def cashflow_dashboard(context):
    """
    Dữ liệu sử dụng cho trang Tổng quan Admin.
    """

    request = context["request"]

    today = date.today()

    # Mặc định xem từ đầu tháng hiện tại đến hôm nay.
    default_start = today.replace(day=1)

    start_date = parse_date(
        request.GET.get("from"),
        default_start,
    )

    end_date = parse_date(
        request.GET.get("to"),
        today,
    )

    # Nếu người dùng chọn ngược ngày thì tự đảo lại.
    if start_date > end_date:
        start_date, end_date = (
            end_date,
            start_date,
        )

    # =====================================================
    # TÀI KHOẢN + SỐ DƯ HIỆN TẠI
    # =====================================================

    accounts = list(
        Account.objects
        .filter(is_active=True)
        .order_by("code")
    )

    account_rows = []

    current_total = Decimal("0")

    for account in accounts:

        balance = account_balance(account)

        current_total += balance

        account_rows.append(
            {
                "account": account,
                "balance": balance,
            }
        )

    # =====================================================
    # GIAO DỊCH TRONG KHOẢNG THỜI GIAN
    # =====================================================

    transactions = Transaction.objects.filter(
        transaction_date__range=(
            start_date,
            end_date,
        ),
        status=Transaction.Status.COMPLETED,
        is_deleted=False,
    )

    total_income = (
        transactions
        .filter(
            transaction_type=Transaction.TransactionType.INCOME
        )
        .aggregate(
            total=Sum("amount")
        )
        ["total"]
        or Decimal("0")
    )

    total_expense = (
        transactions
        .filter(
            transaction_type=Transaction.TransactionType.EXPENSE
        )
        .aggregate(
            total=Sum("amount")
        )
        ["total"]
        or Decimal("0")
    )

    net_cashflow = (
        total_income
        - total_expense
    )

    # =====================================================
    # CÁC NGÀY TỔNG TIỀN BỊ ÂM
    # =====================================================

    negative_days = []

    current_day = start_date

    while current_day <= end_date:

        company_balance = Decimal("0")

        for account in accounts:

            # Tài khoản chưa tồn tại tại thời điểm này
            # thì chưa đưa vào tổng.
            if account.opening_date > current_day:
                continue

            company_balance += account_balance(
                account,
                current_day,
            )

        if company_balance < 0:

            negative_days.append(
                {
                    "date": current_day,
                    "balance": company_balance,
                }
            )

        current_day += timedelta(days=1)

    return {
        "start_date": start_date,
        "end_date": end_date,

        "current_total": current_total,

        "total_income": total_income,
        "total_expense": total_expense,
        "net_cashflow": net_cashflow,

        "accounts": account_rows,

        "negative_days": negative_days,
    }


@register.filter
def money_vnd(value):
    """
    Format số tiền theo kiểu Việt Nam.

    Ví dụ:
    1000000       -> 1.000.000
    1250000000    -> 1.250.000.000
    -500000       -> -500.000
    """

    if value is None:
        return "0"

    try:
        value = Decimal(value)

        formatted = f"{value:,.0f}"

        return formatted.replace(",", ".")

    except (
        ValueError,
        TypeError,
    ):
        return "0"

@register.simple_tag
def admin_filter_choices(spec, cl):
    return list(spec.choices(cl))