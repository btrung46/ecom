from django.shortcuts import render, redirect
from django.views import View
from .models import Product,Customer,Cart
from .forms import CustomerRegisterForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.
def home(request):
    return render(request,'website/home.html',{})
def about(request):
    return render(request,'website/about.html',{})
def contact(request):
    return render(request,'website/contact.html',{})
class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category = val)
        Title = Product.objects.filter(category = val).values('title')
        return render(request, 'website/category.html',locals())
class CategoryTitle(View):
    def get(self, request,val):
        product = Product.objects.filter(title = val)
        Title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'website/category.html',locals())
class productDetail(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,'website/productdetail.html',locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegisterForm()
        return render(request, 'website/register.html',locals())
    def post(self,request):
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "congratulation user register successfuly!!!")
        else:
            messages.warning(request,"invalid Input data")
            
        return render(request, 'website/register.html',locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'website/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user= user, name = name, city = city, mobile=mobile, address = address, zipcode=zipcode)
            reg.save()
            messages.success(request, 'save profile successfully!!!')
        else:
             messages.warning(request, 'invalid Input data')
        return render(request, 'website/profile.html',locals())
    
    
def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'website/address.html',locals())

class updatAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'website/updateAddress.html',locals())
    def post(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST , instance=add)
        if form.is_valid():
            form.save()
            messages.success(request, 'address is updated')
        else:
            messages.success(request, 'invalid input data')
            
        return redirect('address')
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    cart = Cart.objects.filter(user = user)
    for p in cart:
        if product.title == p.product.title:
            messages.success(request,'Products already in the cart')
            return redirect('/cart')
    else:
        Cart(user=user, product = product).save()
    return redirect('/cart')
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user = user)
    amount = 0
    for p in cart:
        value = p.quantity*p.product.discounted_price
        amount += value
    totalamount = amount + 40
    return render(request,'website/addtocart.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id  = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user= request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount += value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount,   
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id  = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user= request.user))
        c.quantity-=1
        if c.quantity == 0:
            c.quantity = 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount += value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount,   
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.method == 'GET':
        prod_id  = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user= request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount += value
        totalamount = amount + 40
        data={
            'amount': amount,
            'totalamount': totalamount,   
        }
        return JsonResponse(data)
class checkout(View):
    def get(self,request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            amount += value
        totalamount = amount + 40
        return render(request,'website/checkout.html',locals())
        