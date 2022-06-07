from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import Customer, Sales


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "email", "telNo")


class SalesSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False)
    transaction_id = serializers.CharField(required=False)

    class Meta:
        model = Sales
        fields = ("amount", "pay_id", "transaction_id", "status")


class CustomerDetailSerializer(serializers.ModelSerializer):
    sales = SalesSerializer(many=True)

    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "email", "telNo", "sales")


class PaymentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    amount = serializers.IntegerField()

    def validate_email(self, value):
        self.customer = Customer.objects.filter(email=value).first()
        if not self.customer:
            raise serializers.ValidationError("Customer does not exist")
        return value

    def validate(self, attrs):
        attrs.pop("email")
        attrs["customer"] = self.customer
        return attrs


class SalesPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ("status", "checkout_link", "created_at", "pay_id", "amount")


class CallbackSerializer(serializers.Serializer):
    tx_ref = serializers.CharField()
    transaction_id = serializers.CharField()

    def validate_tx_ref(self, value):
        qs = Sales.objects.filter(pay_id=value)
        if not qs.exists():
            raise NotFound("Transaction not found", "Transaction Error")
        self.transaction = qs.filter().first()
        return value

    def validate(self, attrs):
        attrs.pop("tx_ref")
        attrs["transaction"] = self.transaction
        return super().validate(attrs)


class CallbackOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        exclude = ("customer",)
