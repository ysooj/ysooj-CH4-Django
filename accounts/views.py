from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login

# 회원가입
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('porducts:product_list')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form':form})