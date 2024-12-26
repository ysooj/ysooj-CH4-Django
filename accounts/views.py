from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from products.models import Product

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form':form})

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    # 등록 물품
    my_products = Product.objects.filter(user=profile_user)
    # 찜한 물품
    liked_products = profile_user.liked_products.all()
    # 팔로잉 여부 확인
    # 로그인한 사용자(requrest.user)가 해당 profile_user를 팔로우 하고 있는 지 확인하는 것. True/False를 반환한다.
    is_following = request.user.follows.filter(pk=profile_user.pk).exists()
    
    context = {
        'profile_user': profile_user,
        'my_products': my_products,
        'liked_products': liked_products,
        'is_following': is_following,
    }
    
    return render(request, 'accounts/profile.html', context)

def profile_edit(request, username):
    if request.user.username != username:   # 프로필 편집을 요청한 사람이 해당 프로필의 유저가 아니면
        return redirect('accounts:profile', username=username)  # 프로필을 편집하지 못하게 그냥 프로필 페이지로 이동.
    
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)  # instance는 어떤 유저인지를 알려줘야 하기 때문에 필요하다.
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username=username)
    else:
        form = ProfileForm(instance=user)

    return render(request, 'accounts/profile_edit.html', {'form': form})

def follow_view(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user: # 팔로우를 요청한 사람은 팔로우 당하는 사람과 다르다.
        # 팔로우가 되어 있는 상태 -> 라면 팔로우 취소 버튼을 준다.
        if request.user.follows.filter(pk=target_user.pk).exists():
            # 취소하는 버튼 생성
            request.user.follows.remove(target_user)
        else:
            request.user.follows.add(target_user)
    return redirect('accounts:profile', username=username)