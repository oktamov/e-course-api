from django.contrib import admin

from checkout.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    fields = ['id', 'amount', 'card']
