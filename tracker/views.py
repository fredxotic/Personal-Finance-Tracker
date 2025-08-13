from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm, CategoryForm
from django.db.models import Sum
from datetime import date
from django.shortcuts import get_object_or_404
from .models import Category

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

@login_required
def dashboard(request):
    today = date.today()
    transactions = Transaction.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    )

    income_total = transactions.filter(transaction_type='INC').aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = transactions.filter(transaction_type='EXP').aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'tracker/dashboard.html', {
        'transactions': transactions,
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': income_total - expense_total
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).order_by('-is_income', 'name')
    return render(request, 'tracker/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'tracker/category_form.html', {'form': form})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')
    return render(request, 'tracker/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'tracker/transaction_form.html', {'form': form})

@login_required
def transaction_edit(request, pk):
    t = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=t)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=t)
    return render(request, 'tracker/transaction_form.html', {'form': form, 'edit': True})

@login_required
def transaction_delete(request, pk):
    t = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        t.delete()
        return redirect('transaction_list')
    return render(request, 'tracker/transaction_confirm_delete.html', {'transaction': t})