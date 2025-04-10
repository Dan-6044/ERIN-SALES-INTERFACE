from django.contrib.auth.models import User
from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line

    def __str__(self):
        return f"{self.name} - {self.location}"


from django.db import models
from django.contrib.auth.models import User
from supervisors.models import Branch 

class SalesRepresentative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_salesreps')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.branch.name})"


from django.db import models
from django.contrib.auth.models import User

class Sale(models.Model):
    customer_name = models.CharField(max_length=255)
    total_amount = models.FloatField()
    invoice_amount = models.FloatField()
    amount_paid = models.FloatField()
    balance = models.FloatField()
    profit = models.FloatField()
    place_of_delivery = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=50)
    sales_rep = models.ForeignKey('SalesRepresentative', on_delete=models.CASCADE)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to logged-in user

    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the record is created

    def __str__(self):
        return self.customer_name
