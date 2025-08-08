from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import RegistrationForm, CategoryForm, TransactionForm
from .models import Transaction, Category

# Create your views here.
@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user = request.user)
    total_income = transactions.filter(type = 'income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type = 'expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses
    recent_transactions = transactions.order_by('-date')[:5]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_transactions': recent_transactions,
    }

    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html',{'form': form})

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).order_by('name')
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
        
    else:
        form = CategoryForm()

    return render(request, 'category_form.html', {'form': form, 'title': 'Create Category'})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category_form.html', {'form': form, 'title': 'Update Category'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transaction_list.html', {'transactions': transactions})

@login_required
def transaction_create(request):
    form = TransactionForm(initial={'user': request.user})
    form.fields['category'].queryset = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        form.fields['category'].queryset = Category.objects.filter(user = request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    return render(request, 'transaction_form.html', {'form': form, 'title': 'Add New Transaction'})

@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    form = TransactionForm(instance=transaction)
    form.fields['category'].queryset = Category.objects.filter(user = request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        form.fields['category'].queryset = Category.objects.filter(user = request.user)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')

    return render(request, 'transaction_form.html', {'form': form, 'title': 'Edit Transaction'})

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user = request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    
    return render(request, 'transaction_confirm_delete.html', {'transaction': transaction})
        