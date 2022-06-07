from .models import Customer, Sales
from .utils import process_payment, verify_transaction


def payment_create(*, customer: Customer, amount: int) -> Sales:
    name = customer.get_full_name()
    data = process_payment(
        name=name, email=customer.email, amount=amount, phone=customer.telNo
    )
    sale = Sales.objects.create(
        customer=customer,
        amount=amount,
        pay_id=data.get("tx_ref"),
        checkout_link=data.get("link"),
    )
    return sale


def sales_verify(*, transaction: Sales, transaction_id: str):
    data = verify_transaction(transaction=transaction_id)
    if data.get("status") != "success":
        transaction.status = "failed"
    else:
        transaction.status = "approved"

    transaction.transaction_id = transaction_id
    transaction.save(update_fields=["status", "transaction_id"])
    return transaction
