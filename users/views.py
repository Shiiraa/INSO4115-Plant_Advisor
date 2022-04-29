from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from users.models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .forms import User
from blog.models import Post, Address

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('blog-home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('blog-home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'users/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('blog-intro')

@login_required
def profile(request): 
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': Post.objects.all(),
        'addresses':Address.objects.all()
    }

    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/edit.html', context)

@login_required
def delete_profile(request):
    
    u = User.objects.get(username=request.user)
    u.delete()

    messages.info(request, f'Your account has been deleted!') 
    return redirect('login')

def searchProfile(request):

    if request.method == "POST":
        searched = request.POST['searched']
        venues = Profile.objects.filter(user__username__contains = searched)

        return render(request,'users/searchProfile.html', {'searched': searched, 'venues':venues} )
    else:

        return render(request,'users/searchProfile.html',{})
