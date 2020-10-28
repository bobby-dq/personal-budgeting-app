from django.contrib import admin
from . models import Budget, Income_Category, Income_Item, Expense_Category, Expense_Item

# Register your models here.

admin.site.register(Budget)
admin.site.register(Income_Category)
admin.site.register(Income_Item)
admin.site.register(Expense_Category)
admin.site.register(Expense_Item)