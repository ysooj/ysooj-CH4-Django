from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm

# Create your views here.
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

# # 로그인돼있어야 새로운 상품을 등록할 수 있게 해야 한다.
@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save() # 유저 설정, db 적재, product 저장
            return redirect('products:product_list')
        
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {'form' : form})

@login_required
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.views += 1
    product.save()
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk) # 항상 검증 필수! 해당 상품이 db에 있는지!
    if product.user != request.user:    # 해당 상품을 등록한 유저가, 지금 로그인한 유저인지 검증!
        return redirect('products:product_detail', pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product_detail', pk=pk)
    else:   # post 요청이 아닌 get 요청일 때.
        form = ProductForm(instance=product, initial={'hashtags_str': ' '.join(ht.name for ht in product.hashtags.all())})

    return render(request, 'products/product_form.html', {'form': form, 'product':product})

@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk) # 항상 검증 필수! 해당 상품이 db에 있는지!
    if product.user != request.user:
        return redirect('products:product_detail', pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/product_detail.html', {'product':product})