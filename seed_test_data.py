import os
import random
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings_local",
)

import django

django.setup()

from django.db import transaction
from cashflow.models import (
    Account,
    Counterparty,
    Order,
    Transaction,
    TransactionEntry,
)


BANKS = [
    ("TEST-MBB", "MBB"),
    ("TEST-TCB", "Techcombank"),
    ("TEST-VCB", "Vietcombank"),
    ("TEST-BIDV", "BIDV"),
    ("TEST-ACB", "ACB"),
    ("TEST-VPB", "VPBank"),
    ("TEST-CTG", "VietinBank"),
    ("TEST-TPB", "TPBank"),
    ("TEST-VIB", "VIB"),
    ("TEST-MSB", "MSB"),
]

PEOPLE_NAMES = [
    "Nguyễn Văn An",
    "Trần Minh Đức",
    "Lê Hoàng Nam",
    "Phạm Thu Trang",
    "Nguyễn Thị Mai",
    "Hoàng Anh Tuấn",
    "Đỗ Minh Long",
    "Vũ Thanh Hà",
    "Bùi Quốc Huy",
    "Phan Ngọc Anh",
]

ORDER_TYPES = [
    "REPAIR",
    "PRODUCTION",
    "DEVELOPMENT",
]


def random_date():
    start = date(2026, 1, 1)
    end = date(2026, 9, 28)

    days = (end - start).days

    return start + timedelta(
        days=random.randint(0, days)
    )


with transaction.atomic():

    print("Đang tạo ngân hàng...")

    accounts = []

    for index, (code, name) in enumerate(BANKS, start=1):
        account, _ = Account.objects.get_or_create(
            code=code,
            defaults={
                "name": name,
                "account_type": "BANK",
                "opening_balance": Decimal(
                    random.randint(50, 500) * 1_000_000
                ),
                "opening_date": date(2026, 1, 1),
                "account_number": f"99999999{index:02d}",
                "note": "Dữ liệu test",
                "is_active": True,
            },
        )

        accounts.append(account)

    print("Đang tạo người gửi / nhận...")

    counterparties = []

    for i in range(1, 101):
        base_name = PEOPLE_NAMES[(i - 1) % len(PEOPLE_NAMES)]

        counterparty, _ = Counterparty.objects.get_or_create(
            code=f"TEST-KH{i:04d}",
            defaults={
                "name": f"{base_name} {i}",
                "counterparty_type": random.choice(
                    [
                        "CUSTOMER",
                        "SUPPLIER",
                        "EMPLOYEE",
                        "OTHER",
                    ]
                ),
                "note": "Dữ liệu test",
                "is_active": True,
            },
        )

        counterparties.append(counterparty)

    print("Đang tạo đơn hàng...")

    orders = []

    for i in range(1, 201):
        customer = random.choice(counterparties)

        order, _ = Order.objects.get_or_create(
            code=f"TEST-DH{i:04d}",
            defaults={
                "name": f"Đơn hàng thử nghiệm {i}",
                "order_type": random.choice(ORDER_TYPES),
                "customer": customer,
                "status": random.choice(
                    [
                        "ACTIVE",
                        "COMPLETED",
                        "INACTIVE",
                    ]
                ),
                "note": "Đơn hàng dùng để test hệ thống",
            },
        )

        orders.append(order)

    print("Đang tạo 2.000 giao dịch...")

    for i in range(1, 2001):

        transaction_type = random.choice(
            [
                "INCOME",
                "EXPENSE",
            ]
        )

        amount = Decimal(
            random.randint(1, 500) * 100_000
        )

        order = random.choice(orders)
        counterparty = random.choice(counterparties)
        account = random.choice(accounts)

        tx, created = Transaction.objects.get_or_create(
            code=f"TEST-GD{i:06d}",
            defaults={
                "transaction_date": random_date(),
                "transaction_type": transaction_type,
                "order": order,
                "counterparty": counterparty,
                "amount": amount,
                "description": (
                    f"Giao dịch test số {i}"
                ),
                "status": "COMPLETED",
            },
        )

        if created:
            TransactionEntry.objects.create(
                transaction=tx,
                account=account,
                direction=(
                    "IN"
                    if transaction_type == "INCOME"
                    else "OUT"
                ),
                amount=amount,
            )

print("")
print("HOÀN THÀNH")
print("10 ngân hàng")
print("100 người gửi / nhận")
print("200 đơn hàng")
print("2.000 giao dịch")