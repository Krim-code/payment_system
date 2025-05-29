import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from backend import Organization, Payment
import uuid

pytestmark = pytest.mark.django_db

client = APIClient()

valid_payload = {
    "operation_id": str(uuid.uuid4()),
    "amount": 145000,
    "payer_inn": "1234567890",
    "document_number": "PAY-328",
    "document_date": "2024-04-27T21:00:00Z"
}


def test_webhook_creates_payment_and_updates_balance():
    url = reverse("bank-webhook")
    response = client.post(url, data=valid_payload, format="json")
    assert response.status_code == 200
    assert response.data["processed"] is True

    org = Organization.objects.get(inn="1234567890")
    assert org.balance == 145000

    payment = Payment.objects.get(operation_id=valid_payload["operation_id"])
    assert payment.amount == 145000


def test_webhook_duplicate_operation_id_not_processed():
    url = reverse("bank-webhook")
    client.post(url, data=valid_payload, format="json")  # первая попытка
    response = client.post(url, data=valid_payload, format="json")  # дубль

    assert response.status_code == 200
    assert response.data["processed"] is False

    org = Organization.objects.get(inn="1234567890")
    assert org.balance == 145000  # второй раз не начислилось


def test_balance_endpoint_returns_correct_balance():
    # ручное создание
    Organization.objects.create(inn="9990001112", balance=888888)
    url = reverse("org-balance", kwargs={"inn": "9990001112"})
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["balance"] == 888888
    assert response.data["inn"] == "9990001112"


def test_balance_endpoint_returns_404_for_missing_org():
    url = reverse("org-balance", kwargs={"inn": "doesnotexist"})
    response = client.get(url)
    assert response.status_code == 404
