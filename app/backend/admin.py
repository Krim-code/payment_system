from django.contrib import admin
from .models import Organization, Payment

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("inn", "balance")
    search_fields = ("inn",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("operation_id", "payer_inn", "amount", "document_number", "document_date", "created_at")
    search_fields = ("operation_id", "payer_inn", "document_number")
    list_filter = ("document_date",)
    ordering = ("-created_at",)
