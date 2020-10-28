from django.shortcuts import render, redirect
from .models import Budget, Income_Category, Income_Item, Expense_Category, Expense_Item
from .forms import BudgetForm, IncomeCategoryForm, IncomeItemForm, ExpenseCategoryForm, ExpenseItemForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from datetime import datetime
# Create your views here.

# Static views
def index(request):
    """Home page of the Budget App."""
    return render(request, 'budgeting/index.html')

def base(request):
    """Data needs to display all through out the website."""
    # for future context
    context = {}
    return render(request, 'budgeting/base.html', context)

@login_required
def budgets(request):
    """A list of the user's budgets."""
    budgets = Budget.objects.filter(owner=request.user).order_by('-date_created')
    context = {
        'budgets': budgets
    }
    
    return render(request, 'budgeting/budgets.html', context)

@login_required
def detailed_budget(request, budget_id):
    """A detailed look of a budget."""
    budget = Budget.objects.filter(owner=request.user).get(id=budget_id)
    expense_categories = budget.expense_category_set.order_by('title')
    income_categories = budget.income_category_set.order_by('title')
    context = {
        'budget': budget,
        'expense_categories':expense_categories,
        'income_categories': income_categories,
    }

    return render(request, 'budgeting/detailed_budget.html', context)

@login_required
def detailed_income_category(request, income_category_id):
    """A detailed look of an income category."""
    income_category = Income_Category.objects.filter(owner=request.user).get(id=income_category_id)
    income_items = income_category.income_item_set.order_by('-date')
    context = {
        'income_category': income_category,
        'income_items': income_items,
        'budget': income_category.budget
    }

    return render(request, 'budgeting/detailed_income_category.html', context)

@login_required
def detailed_expense_category(request, expense_category_id):
    """A detailed look of an expense category."""
    expense_category = Expense_Category.objects.filter(owner=request.user).get(id=expense_category_id)
    expense_items = expense_category.expense_item_set.order_by('-date')
    context = {
        'expense_category': expense_category,
        'expense_items': expense_items,
        'budget': expense_category.budget
    }

    return render(request, 'budgeting/detailed_expense_category.html', context)

@login_required
def budget_transactions(request, budget_id):
    """Displays a list of all the transactions of a budget (income items and expense items.)"""
    budget = Budget.objects.filter(owner=request.user).get(id=budget_id)
    expense_items = budget.expense_item_set.order_by('-date')
    income_items = budget.income_item_set.order_by('-date')
    context = {
        'budget': budget,
        'expense_items': expense_items,
        'income_items': income_items,
    }

    return render(request, 'budgeting/budget_transactions.html', context)


# New, Edit and Delete Budget Forms
@login_required
def new_budget(request):
    """Adds a new budget.""" 
    if request.method != 'POST':
        form = BudgetForm()
    else:
        form = BudgetForm(data=request.POST)
        if form.is_valid():
            new_budget = form.save(commit=False)
            new_budget.owner = request.user
            new_budget.save()
            return redirect('budgeting:budgets')
    
    context = {'form': form}
    return render(request, 'budgeting/new_budget.html', context)

@login_required
def edit_budget(request, budget_id):
    """Edits an existing budget."""
    budget = Budget.objects.filter(owner=request.user).get(id=budget_id)
    
    if budget.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = BudgetForm(instance=budget)
    else:
        form = BudgetForm(instance=budget, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgeting:detailed_budget', budget_id=budget.id)
    
    context = {'form': form, 'budget': budget}
    return render(request, 'budgeting/edit_budget.html', context)

@login_required
def delete_budget(request, budget_id):
    """Deletes an existing budget."""
    budget = Budget.objects.filter(owner=request.user).get(id=budget_id)

    if budget.owner != request.user:
        raise Http404

    if request.method == 'POST':
        budget.delete()
        return redirect('budgeting:budgets')
    
    context = {'budget': budget}
    return render(request, 'budgeting/delete_budget.html', context)

# New, Edit, and Delete Income Category Forms
@login_required
def new_income_category(request, budget_id):
    """Add a new income category for a budget."""
    budget = Budget.objects.filter(owner=request.user).get(id=budget_id)

    if request.method != 'POST':
        form = IncomeCategoryForm()
    else:
        form = IncomeCategoryForm(data=request.POST)
        if form.is_valid():
            new_income_category = form.save(commit=False)
            new_income_category.budget = budget
            new_income_category.owner = request.user
            new_income_category.save()
            return redirect('budgeting:detailed_budget', budget_id=budget_id)
    
    context = {'budget': budget, 'form': form}
    return render(request, 'budgeting/new_income_category.html', context)

@login_required
def edit_income_category(request, income_category_id):
    """Edits an existing income category."""
    income_category = Income_Category.objects.filter(owner=request.user).get(id=income_category_id)
    budget = income_category.budget
    
    if income_category.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = IncomeCategoryForm(instance=income_category)
    else:
        form = IncomeCategoryForm(instance=income_category, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgeting:detailed_income_category', income_category_id=income_category.id)
    
    context = {'form': form, 'budget': budget, 'income_category': income_category}
    return render(request, 'budgeting/edit_income_category.html', context)

@login_required
def delete_income_category(request, income_category_id):
    """Deletes an existing budget."""
    income_category = Income_Category.objects.filter(owner=request.user).get(id=income_category_id)
    budget = income_category.budget

    if income_category.owner != request.user:
        raise Http404

    if request.method == 'POST':
        income_category.delete()
        return redirect('budgeting:detailed_budget', budget_id=budget.id)
    
    context = {'income_category': income_category, 'budget': budget}
    return render(request, 'budgeting/delete_income_category.html', context)

# New, Edit, and Delete Income Item Forms
@login_required
def new_income_item(request, income_category_id):
    """Add a new income item for an income category."""
    income_category = Income_Category.objects.filter(owner=request.user).get(id=income_category_id)
    budget = income_category.budget

    if request.method != 'POST':
        form = IncomeItemForm()
    else:
        form = IncomeItemForm(data=request.POST)
        if form.is_valid():
            new_income_item = form.save(commit=False)
            new_income_item.budget = budget
            new_income_item.owner = request.user
            new_income_item.income_category = income_category
            new_income_item.save()
            return redirect('budgeting:detailed_budget', budget_id=budget.id)
    
    context = {'income_category': income_category,'budget': budget, 'form': form}
    return render(request, 'budgeting/new_income_item.html', context)

@login_required
def edit_income_item(request, income_item_id):
    """Edits an existing income category."""
    income_item = Income_Item.objects.filter(owner=request.user).get(id=income_item_id)
    budget = income_item.budget
    income_category = income_item.income_category

    if income_item.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = IncomeItemForm(instance=income_item)
    else:
        form = IncomeItemForm(instance=income_item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgeting:detailed_income_category', income_category_id=income_category.id)
    
    context = {'form': form, 'budget': budget, 'income_item': income_item, 'income_category': income_category}
    return render(request, 'budgeting/edit_income_item.html', context)

@login_required
def delete_income_item(request, income_item_id):
    """Deletes an existing budget."""
    income_item = Income_Item.objects.filter(owner=request.user).get(id=income_item_id)
    budget = income_item.budget
    income_category = income_item.income_category

    if income_item.owner != request.user:
        raise Http404

    if request.method == 'POST':
        income_item.delete()
        return redirect('budgeting:detailed_income_category', income_category_id=income_category.id)
    
    context = {'income_category': income_category, 'budget': budget, 'income_item': income_item}
    return render(request, 'budgeting/delete_income_item.html', context)

# New, Edit, and Delete Expense Category Forms
@login_required
def new_expense_category(request, budget_id):
    """Add a new expense category for a budget."""
    budget = Budget.objects.filter(owner=request.user).get(id=budget_id)

    if request.method != 'POST':
        form = ExpenseCategoryForm()
    else:
        form = ExpenseCategoryForm(data=request.POST)
        if form.is_valid():
            new_expense_category = form.save(commit=False)
            new_expense_category.budget = budget
            new_expense_category.owner = request.user
            new_expense_category.save()
            return redirect('budgeting:detailed_budget', budget_id=budget_id)
    
    context = {'budget': budget, 'form': form}
    return render(request, 'budgeting/new_expense_category.html', context)

@login_required
def edit_expense_category(request, expense_category_id):
    """Edits an existing expense category."""
    expense_category = Expense_Category.objects.filter(owner=request.user).get(id=expense_category_id)
    budget = expense_category.budget

    if expense_category.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = ExpenseCategoryForm(instance=expense_category)
    else:
        form = ExpenseCategoryForm(instance=expense_category, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgeting:detailed_expense_category', expense_category_id=expense_category.id)
    
    context = {'form': form, 'budget': budget, 'expense_category': expense_category}
    return render(request, 'budgeting/edit_expense_category.html', context)

@login_required
def delete_expense_category(request, expense_category_id):
    """Deletes an existing budget."""
    expense_category = Expense_Category.objects.filter(owner=request.user).get(id=expense_category_id)
    budget = expense_category.budget

    if expense_category.owner != request.user:
        raise Http404

    if request.method == 'POST':
        expense_category.delete()
        return redirect('budgeting:detailed_budget', budget_id=budget.id)
    
    context = {'expense_category': expense_category, 'budget': budget}
    return render(request, 'budgeting/delete_expense_category.html', context)

# New, Edit, and Delete Expense Item Forms
@login_required
def new_expense_item(request, expense_category_id):
    """Add a new expense item for an expense category."""
    expense_category = Expense_Category.objects.filter(owner=request.user).get(id=expense_category_id)
    budget = expense_category.budget

    if request.method != 'POST':
        form = ExpenseItemForm()
    else:
        form = ExpenseItemForm(data=request.POST)
        if form.is_valid():
            new_expense_item = form.save(commit=False)
            new_expense_item.budget = budget
            new_expense_item.owner = request.user
            new_expense_item.expense_category = expense_category
            new_expense_item.save()
            return redirect('budgeting:detailed_budget', budget_id=budget.id)
    
    context = {'expense_category': expense_category,'budget': budget, 'form': form}
    return render(request, 'budgeting/new_expense_item.html', context)

@login_required
def edit_expense_item(request, expense_item_id):
    """Edits an existing expense category."""
    expense_item = Expense_Item.objects.filter(owner=request.user).get(id=expense_item_id)
    budget = expense_item.budget
    expense_category = expense_item.expense_category

    if expense_item.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = ExpenseItemForm(instance=expense_item)
    else:
        form = ExpenseItemForm(instance=expense_item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgeting:detailed_expense_category', expense_category_id=expense_category.id)
    
    context = {'form': form, 'budget': budget, 'expense_item': expense_item, 'expense_category': expense_category}
    return render(request, 'budgeting/edit_expense_item.html', context)

@login_required
def delete_expense_item(request, expense_item_id):
    """Deletes an existing budget."""
    expense_item = Expense_Item.objects.filter(owner=request.user).get(id=expense_item_id)
    budget = expense_item.budget
    expense_category = expense_item.expense_category

    if expense_item.owner != request.user:
        raise Http404

    if request.method == 'POST':
        expense_item.delete()
        return redirect('budgeting:detailed_expense_category', expense_category_id=expense_category.id)
    
    context = {'expense_category': expense_category, 'budget': budget, 'expense_item': expense_item}
    return render(request, 'budgeting/delete_expense_item.html', context)