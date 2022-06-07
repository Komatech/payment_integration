from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    telNo = models.CharField(max_length=20)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()


class Sales(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="sales"
    )
    amount = models.IntegerField()
    pay_id = models.CharField(max_length=250)
    transaction_id = models.CharField(max_length=250)
    status = models.CharField(max_length=20, default="pending")
    checkout_link = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.customer}-{self.transaction_id}"
