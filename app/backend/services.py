# services.py
from .models import Organization, Payment
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

def process_bank_webhook(data):
    if Payment.objects.filter(operation_id=data['operation_id']).exists():
        logger.warning(f"Duplicate operation_id {data['operation_id']} — skipping")
        return False

    with transaction.atomic():
        Payment.objects.create(**data)
        org, _ = Organization.objects.get_or_create(inn=data['payer_inn'])
        org.balance += data['amount']
        org.save()

        logger.info(
            f"Payment received: INN={org.inn}, amount={data['amount']}, "
            f"doc={data['document_number']}, new_balance={org.balance}"
        )

    return True