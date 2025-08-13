from django.contrib import admin
from django.contrib import admin
from .models import Category, Transaction

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_income', 'user')
    list_filter = ('is_income', 'user')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'category', 'date', 'user')
    list_filter = ('transaction_type', 'date', 'category', 'user')
    search_fields = ('note',)
    date_hierarchy = 'date'
