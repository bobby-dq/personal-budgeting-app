from django.urls import path, include
from . import views


app_name = 'budgeting'

urlpatterns = [
    # Static views
    path('', views.index, name='index'),
    path('budgets/', views.budgets, name='budgets'),
    path('budgets/budget/<int:budget_id>/', views.detailed_budget, name='detailed_budget'),
    path('budgets/income_category/<int:income_category_id>', views.detailed_income_category, name='detailed_income_category'),
    path('budgets/expense_category/<int:expense_category_id>', views.detailed_expense_category, name='detailed_expense_category'),
    path('budget/transactions/<int:budget_id>', views.budget_transactions, name='budget_transactions'),

    # Add, Edit, Delete Budget Forms
    path('new_budget/', views.new_budget, name='new_budget'),
    path('budget/edit_budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),
    path('budget/delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),

    # Add, Edit, Delete Income Category Forms
    path('budget/new_income_category/<int:budget_id>/',views.new_income_category, name='new_income_category'),
    path('budget/edit_income_category/<int:income_category_id>/', views.edit_income_category, name='edit_income_category'),
    path('budget/delete_income_category/<int:income_category_id>/', views.delete_income_category, name='delete_income_category'),

    # Add, Edit, Delete Income Item Forms
    path('budget/new_income_item/<int:income_category_id>/',views.new_income_item, name='new_income_item'),
    path('budget/edit_income_item/<int:income_item_id>/', views.edit_income_item, name='edit_income_item'),
    path('budget/delete_income_item/<int:income_item_id>/', views.delete_income_item, name='delete_income_item'),

    # Add, Edit, Delete Expense Category Forms
    path('budget/new_expense_category/<int:budget_id>/',views.new_expense_category, name='new_expense_category'),
    path('budget/edit_expense_category/<int:expense_category_id>/', views.edit_expense_category, name='edit_expense_category'),
    path('budget/delete_expense_category/<int:expense_category_id>/', views.delete_expense_category, name='delete_expense_category'),

    # Add, Edit, Delete Expense Item Forms
    path('budget/new_expense_item/<int:expense_category_id>/',views.new_expense_item, name='new_expense_item'),
    path('budget/edit_expense_item/<int:expense_item_id>/', views.edit_expense_item, name='edit_expense_item'),
    path('budget/delete_expense_item/<int:expense_item_id>/', views.delete_expense_item, name='delete_expense_item'),
]
