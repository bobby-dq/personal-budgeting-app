from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm

# Create your views here.

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            new_user = form.save()
            login(request, new_user)
            return redirect('budgeting:budgets')

    context = {'form': form}
    return render (request, 'registration/register.html', context)