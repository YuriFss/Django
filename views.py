from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, DetailsForm

def register(request):
    if request.method == 'POST':
        r_form = UserRegisterForm(request.POST)
        o_form = DetailsForm(request.POST)
        if r_form.is_valid and o_form.is_valid():
            user = r_form.save()
            o_form.instance.user = user
            o_form.save()
            username = r_form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:
        r_form = UserRegisterForm()
        o_form = DetailsForm()

    context = {
        'r_form' : r_form,
        'o_form' : o_form
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        o_form = DetailsForm(request.POST, instance=request.user.details)
        if u_form.is_valid() and p_form.is_valid() and o_form.is_valid():
            u_form.save()
            p_form.save()
            o_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        o_form = DetailsForm(instance=request.user.details)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'o_form': o_form
    }

    return render(request, 'users/profile.html', context)
