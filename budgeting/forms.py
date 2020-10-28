from django import forms
from . models import Budget, Income_Category, Income_Item, Expense_Category, Expense_Item

class BudgetForm(forms.ModelForm):
    """A form for creating a new Budget."""

    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'e.g. January Budget'
        self.fields['start_date'].widget.attrs['placeholder'] = 'yyyy-mm-dd'
        self.fields['end_date'].widget.attrs['placeholder'] = 'yyyy-mm-dd'
    
    class Meta:
        model = Budget
        fields = [
            'title',
            'start_date',
            'end_date',
        ]
        labels = {
            'title': 'Title (Required):',
            'start_date': 'Start Date (Required):',
            'end_date': 'End Date (Required):',
        }

class IncomeCategoryForm(forms.ModelForm):
    """A form for creating an IncomeCategory."""

    def __init__(self, *args, **kwargs):
        super(IncomeCategoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'e.g. Payroll'
        self.fields['description'].widget.attrs['placeholder'] = 'e.g. Company Name'
        self.fields['budgeted_amount'].widget.attrs['placeholder'] = 'e.g. 1500'

    class Meta:
        model = Income_Category
        fields = [
            'title',
            'description',
            'budgeted_amount',
        ]
        labels = {
            'title': 'Title (Required):',
            'description': 'Description:',
            'budgeted_amount': 'Budgeted Amount (Required):',
        }

class IncomeItemForm(forms.ModelForm):
    """A form for creating an income item."""

    def __init__(self, *args, **kwargs):
        super(IncomeItemForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'e.g. Paycheque 1'
        self.fields['description'].widget.attrs['placeholder'] = 'Optional'
        self.fields['amount'].widget.attrs['placeholder'] = 'e.g. 1500'
        self.fields['date'].widget.attrs['placeholder'] = 'yyyy-mm-dd'
     
    class Meta:
        model = Income_Item
        fields = [
            'title',
            'description',
            'amount',
            'date',
        ]
        labels = {
            'title': 'Title (Required):',
            'description': 'Description:',
            'amount': 'Amount (Required):',
            'date': 'Transaction Date (Required):',
        }

class ExpenseCategoryForm(forms.ModelForm):
    """A form for creating an ExpenseCategory."""

    def __init__(self, *args, **kwargs):
        super(ExpenseCategoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'e.g. Car Insurance'
        self.fields['description'].widget.attrs['placeholder'] = 'e.g. Company'
        self.fields['budgeted_amount'].widget.attrs['placeholder'] = 'e.g. 200'

    class Meta:
        model = Expense_Category
        fields = [
            'title',
            'description',
            'budgeted_amount',
        ]
        labels = {
            'title': 'Title (Required):',
            'description': 'Description:',
            'budgeted_amount': 'Budgeted Amount (Required):',
        }

class ExpenseItemForm(forms.ModelForm):
    """A form for creating an expense item."""

    def __init__(self, *args, **kwargs):
        super(ExpenseItemForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'e.g. Groceries'
        self.fields['description'].widget.attrs['placeholder'] = 'Optional'
        self.fields['amount'].widget.attrs['placeholder'] = 'e.g. 100'
        self.fields['date'].widget.attrs['placeholder'] = 'yyyy-mm-dd'
     
    class Meta:
        model = Expense_Item
        fields = [
            'title',
            'description',
            'amount',
            'date',
        ]
        labels = {
            'title': 'Title (Required):',
            'description': 'Description:',
            'amount': 'Amount (Required):',
            'date': 'Transaction Date (Required):',
        }

