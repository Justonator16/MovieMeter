from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RegisterForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from movies.models import Review
from django.contrib.auth.models import User

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('movies:home', )

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('accounts:login')

# Profile CRUD
#Retrive profile of user who is logged in

@login_required(login_url=reverse_lazy('accounts:login'))
def profile(request, username):
    profile = User.objects.filter(username=username)
    reviews = Review.objects.filter(reviewer=request.user.id)
    context = {
        'profile': profile,
        'reviews': reviews,
        }
    return render(request, 'registration/profile_detail.html', context)

#Update profile
@login_required(login_url=reverse_lazy('accounts:login'))
def profile_update(request, username):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated successfully")
            return redirect(reverse_lazy('accounts:login'))
        else:
            return render(request, 'registration/profile_update.html', {'form': form})
        
    elif request.method == 'GET':
        form = ProfileUpdateForm(instance=request.user)
        return render(request, 'registration/profile_update.html', {'form': form})

# Delete profile
@login_required(login_url=reverse_lazy('accounts:login'))
def profile_delete(request, username):
    if request.method == 'POST':
        user = User.objects.filter(username=request.user)
        user.delete()
        messages.success(request, "Profile successfully deleted")
        return redirect(reverse_lazy('accounts:login'))
    else:
        return render(request, 'registration/profile_delete.html' )
    
