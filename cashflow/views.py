from django.shortcuts import render


def dashboard(request):
    return render(
        request,
        "cashflow/dashboard.html",
        {
            "active_page": "dashboard",
        },
    )


def transaction_create(request):
    return render(
        request,
        "cashflow/transaction_form.html",
        {
            "active_page": "input",
        },
    )


def transaction_list(request):
    return render(
        request,
        "cashflow/transaction_list.html",
        {
            "active_page": "list",
        },
    )