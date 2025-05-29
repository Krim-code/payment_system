import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .serializers import PaymentWebhookSerializer, OrganizationBalanceSerializer
from .models import Organization, Payment
from .services import process_bank_webhook

logger = logging.getLogger(__name__)

class BankWebhookView(APIView):
    def post(self, request):
        try:
            serializer = PaymentWebhookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            if Payment.objects.filter(operation_id=request.data.get("operation_id")).exists():
                logger.warning(f"Duplicate webhook: {request.data}")
                return Response({"status": "ok", "processed": False}, status=200)
            logger.error(f"Invalid webhook payload: {request.data} — {e}")
            raise

        processed = process_bank_webhook(serializer.validated_data)
        return Response({"status": "ok", "processed": processed}, status=200)
class OrganizationBalanceView(APIView):
    def get(self, request, inn):
        try:
            org = Organization.objects.get(inn=inn)
        except Organization.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrganizationBalanceSerializer(org)
        return Response(serializer.data)
