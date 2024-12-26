from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

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

# 로그인
def login_view(request):
    # 유저가 인증되었다면 바로 상품 목록 보여줘라.
    if request.user.is_authenticated:
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products:product_list')
        
    else:
        form = AuthenticationForm(request)
        return render(request, 'accounts/login.html', {'form': form})

# 로그아웃
@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')