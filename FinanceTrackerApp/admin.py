from django.contrib import admin
from FinanceTrackerApp.models import Category, Transaction

# Register your models here.
admin.site.register(Category)
admin.site.register(Transaction)