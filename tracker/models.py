from django.conf import settings
from django.db import models

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=120)
    is_income = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['-is_income', 'name']

    def __str__(self):
        return f"{self.name} ({'Income' if self.is_income else 'Expense'})"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('EXP', 'Expense'),
        ('INC', 'Income'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        transaction_type_display = dict(self.TRANSACTION_TYPE_CHOICES).get(self.transaction_type, self.transaction_type)
        return f"{transaction_type_display} {self.amount} on {self.date}"
