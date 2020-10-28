from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.models import User
 
# Create your models here.

class Budget(models.Model):
    """An object that will represent the budget of a given timeline."""
    # Relations to 'parent' models
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Distinct attributes
    title = models.CharField(max_length=32)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    date_created = models.DateTimeField(auto_now_add=True)
    

    def total_income(self):
        """Return the total income of the budget."""
        context = self.income_item_set.aggregate(total_income=Sum('amount'))
        return context['total_income']
    
    def total_expense(self):
        """Return the total expense of the budget."""
        context = self.expense_item_set.aggregate(total_expense=Sum('amount'))
        return context['total_expense']
    
    def total_income_budgeted(self):
        """Return the total budgeted income of a budget"""
        context = self.income_category_set.aggregate(total_income_budgeted=Sum('budgeted_amount'))
        return context['total_income_budgeted']
    
    def total_expense_budgeted(self):
        """Return the total budgeted expenese of the budget."""
        context = self.expense_category_set.aggregate(total_expense_budgeted=Sum('budgeted_amount'))
        return context['total_expense_budgeted']

    def budgeted_difference(self):
        """Return the difference between the totals of budgeted expense and budgeted income."""
        total_income_budgeted = self.total_income_budgeted()
        total_expense_budgeted = self.total_expense_budgeted()
        
        if total_income_budgeted is None or total_expense_budgeted is None:
            return 0
        
        context = total_income_budgeted - total_expense_budgeted
        return context
    
    def savings(self):
        """Return the difference between income and expense."""
        income = self.total_income()
        expense = self.total_expense()
        
        if income is None or expense is None:
            return 0
        
        context = income - expense
        return context

    def progress(self):
        """Return the progress of the budget (savings/total_income)"""

    class Meta:
        verbose_name = 'Budget'

    def __str__(self):
        return self.title

class Income_Category(models.Model):
    """Income category that will contain one or multiple income items."""
    # Relations to 'parent' models.
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Distinct attributes
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=32, blank=True)
    budgeted_amount = models.DecimalField(max_digits=99, decimal_places=2)

    def actual_amount(self):
        """Return the total income of the budget."""
        context = self.income_item_set.aggregate(actual_amount=Sum('amount'))
        return context['actual_amount']

    def difference(self):
        """Return the difference between the budgeted amount and actual amount."""
        budgeted = self.budgeted_amount
        actual = self.actual_amount()
        
        if actual is None:
            return 0
        
        context = actual-budgeted
        return context

    class Meta:
        verbose_name_plural = 'Income Categories'
        verbose_name = 'Income Category'

    def __str__(self):
        return self.title

class Income_Item(models.Model):
    """Income item that belongs to an income category."""
    # Relations to parent models.
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    income_category = models.ForeignKey(Income_Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Distinct attributes.
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=32, blank=True)
    amount = models.DecimalField(max_digits=99, decimal_places=2)
    date = models.DateField(default=datetime.now)

    class Meta:
        verbose_name_plural = 'Income Items'
        verbose_name = 'Income Item'
    
    def __str__(self):
        return self.title

class Expense_Category(models.Model):
    """Expense category that will contain one or multiple expense items."""
    # Relations to parent models.
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Distinct attributes
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=32, blank=True)
    budgeted_amount = models.DecimalField(max_digits=99, decimal_places=2)

    def actual_amount(self):
        """Return the total income of the budget."""
        context = self.expense_item_set.aggregate(actual_amount=Sum('amount'))
        return context['actual_amount']

    def difference(self):
        """Return the difference between the budgeted amount and actual amount."""
        budgeted = self.budgeted_amount
        actual = self.actual_amount()
        
        if actual is None:
            return 0
        
        context = budgeted-actual
        return context

    class Meta:
        verbose_name_plural = 'Expense Categories'
        verbose_name = 'Expense Category'
    
    def __str__(self):
        return self.title

class Expense_Item(models.Model):
    """Expense item that belongs to an expense category."""
    # Relations to parent models.
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    expense_category = models.ForeignKey(Expense_Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Distinct attributes.
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=32, blank=True)
    amount = models.DecimalField(max_digits=99, decimal_places=2)
    date = models.DateField(default=datetime.now)

    class Meta:
        verbose_name_plural = 'Expense Items'
        verbose_name = 'Expense Item'
    
    def __str__(self):
        return self.title