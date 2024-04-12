from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render , redirect, get_object_or_404
from .models import Category,Product,ProductReview,CartOrder,CartOrderItems,Wishlist,Address
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from taggit.models import Tag

from .forms import ProductReviewForm
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.template.loader import render_to_string
from django.contrib import messages

from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from authusers.models import Profile,ContactUs
from django.core import serializers
from django.db.models import Avg,Count,Q
import calendar
from django.db.models.functions import ExtractMonth
# from core.filters import ProductFilter
# from django.views.generic.list import ListView

# Create your views here.
def index(request):
    categories =Category.objects.all()
    products  = Product.objects.all().order_by('-date')[:8]
    search = request.GET.get('recherche')
    if search != '' and search is not None:
        products = Product.objects.filter(
            Q(title__icontains = search ) and Q(category__title__icontains=search)
            )
    # paginator = Paginator(products,4)
    # page =request.GET.get('page')
    # try:
    #     products = paginator.page(page)
    # except PageNotAnInteger:
    #     products = paginator.page(1)
    # except EmptyPage:
    #     products = paginator.page(paginator.num_pages)
    context={
        'categories':categories,
        'products':products
    }

    return render(request,'core/index.html',context)


# class ListProductView(ListView):
#     queryset = Product.objects.all()
#     template_name = "products2.html"
#     context_object_name ="products"

#     def get_queryset(self):
#         queryset= super().get_queryset()
#         self.filterset =ProductFilter(self.request.GET , queryset=queryset)
#         return self.filterset.qs

#     def get_context_data(self, **kwargs: Any):
#         context =  super().get_context_data(**kwargs)
#         context['form'] = self.filterset.form
#         return context


def is_valid_query(param):
    return param !=''and param is not None

def list_product(request):
    query = Product.objects.all().order_by("-date")
    # product_filter=ProductFilter(request.GET , queryset=query) 


    category = Category.objects.all()

    search_product_category = request.GET.get('recherche')
    search_price_min = request.GET.get('min')
    search_price_max = request.GET.get('max')

    search_date_debut = request.GET.get('debut')   
    search_date_end = request.GET.get('end')


    if is_valid_query(search_product_category):
        query = query.filter(Q(title__icontains = search_product_category) | Q(category__title__icontains = search_product_category))
    if is_valid_query(search_price_min):
        query = query.filter(price__gte = search_price_min)
    if is_valid_query(search_price_max):
        query =query.filter(price__lt=search_price_max)
    if is_valid_query(search_date_debut):
        query = query.filter(date__gte = search_date_debut)
    if is_valid_query(search_date_end):
        query = query.filter(date__lt=search_date_end)

    paginator = Paginator(query,6)
    page =request.GET.get('page')
    try:
       query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    context = {
        # 'form': product_filter.form,
        'products':query,
        'cat':category
    }
    return render(request , 'core/product.html',context)


def list_product_category(request,cid):
    category = Category.objects.all()
    categories = Category.objects.get(cid=cid)
    product = Product.objects.filter(category=categories)
    paginator = Paginator(product , 3)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    context={
        'categories':categories,
        'products':product,
        'cat':category
    }
    return render(request,'core/category_product.html',context)

def product_detail(request,slug,pid):
    products = get_object_or_404(Product,slug=slug,pid=pid)
    image_product = products.p_image.all()
    c_products = Product.objects.filter(category=products.category).exclude(pid=pid)

    reviews = ProductReview.objects.filter(product=products).order_by('-date')

    avg_reviews = ProductReview.objects.filter(product=products).aggregate(rating=Avg('rating'))

    form_review = ProductReviewForm()
    # 

    context ={
        'products':products,
        'image':image_product,
        'cproducts':c_products,
        'reviews':reviews,
        'avg':avg_reviews,
        'form_review':form_review,
    }
    return render(request,'core/product-detail.html',context)

def tag_list(request,slug_tag=None):
    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = None
    if slug_tag:
        tag = get_object_or_404(Tag,slug=slug_tag)
        products =products.filter(tags__in=[tag])

    context={
        'products':products,
        'tag':tag
    }
    return render(request,'core/tag.html',context)

def ajax_add_review(request,slug,pid):
    products = Product.objects.get(slug=slug,pid=pid)
    user =request.user
    rev = ProductReview.objects.create(
        user = user , 
        product = products,
        review = request.POST['review'],
        rating = request.POST['rating']
    )
    
    avg_review = ProductReview.objects.filter(product=products).aggregate(rating=Avg('rating'))
    context = {
        'user':user.username,
        'review':request.POST['review'],
        'rating': request.POST['rating']
    }
    return JsonResponse(
        {
            'bool':True,
            'context':context,
            'avg':avg_review,
        }
    )




def filter_product(request):
    categories = request.GET.getlist('category[]')
    products = Product.objects.all().order_by('-id').distinct()

   
    # min_price = request.GET['min_price']
    # max_price = request.GET['max_price']

    # products = products.filter(price__gte=min_price)
    # products = products.filter(price__lt=max_price)



    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    paginator = Paginator(products,6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    data = render_to_string("core/async/product.html", {"products":products})
    return JsonResponse(
        {
            'data':data
        }
    )
     

def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'quantity':request.GET['quantity'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET["id"])]['quantity'] = int(cart_product[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse(
        {
            "data":request.session['cart_data_obj'],
            'totalitems': len(request.session['cart_data_obj'])
        }
    )


def cart(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])
        return render(request,'core/cart.html',{
             'cart_data':request.session['cart_data_obj'],
             'totalitems': len(request.session['cart_data_obj']),
             'cart_total_amount': cart_total_amount
            })
    else:
        messages.warning(request,"Votre panier est vide")
        return redirect('core:index')

def delete_item_cart(request):
    product_id =str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
             
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html",{
        'cart_data':request.session['cart_data_obj'],
        'cart_total_amount': cart_total_amount
    })
    return JsonResponse({
        'data':context,
        'totalitems': len(request.session['cart_data_obj']),
    })
            

def update_item_cart(request):
    product_id =str(request.GET['id'])
    product_qty = request.GET['quantity']
    

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = product_qty
            request.session['cart_data_obj'] = cart_data
             
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html",{
        'cart_data':request.session['cart_data_obj'],
        'cart_total_amount': cart_total_amount
    })
    return JsonResponse({
        'data':context,
        'totalitems': len(request.session['cart_data_obj']),
    })

@login_required
def checkout(request):
    cart_total_amount = 0
    total_amount = 0
    if 'cart_data_obj' in request.session:

        for p_id , item in request.session['cart_data_obj'].items():
            total_amount += int(item['quantity']) * float(item['price'])
        
        order = CartOrder.objects.create(
            user = request.user,
            price = total_amount,
           
        )

        for p_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])

        order_cart_item = CartOrderItems.objects.create(
            order=order,
            invoce_no = "INVOICE_NO-"+str(order.id),
            item = item['title'],
            image = item['image'],
            quantity=item['quantity'],
            price =item['price'],
            total = float(item['price']) * float(item['quantity']),
            
        )


    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": cart_total_amount,
        "item_name": f"Order-{item['title']}-No-{str(order.id)}",
        "invoice": "INVOICE_NO-"+ item['title'] +"-"+str(order.id),
        "currency_code":"EUR",
        "notify_url":'http://{}{}'.format(host,reverse("core:paypal-ipn")),
        "return_url":'http://{}{}'.format(host,reverse("core:payment-success")),
        "cancel_url":'http://{}{}'.format(host,reverse("core:payment-failed")),
        # "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        # "return": request.build_absolute_uri(reverse('your-return-view')),
        # "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict) 

    # cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])
    # context={
    #     'cart_data':request.session['cart_data_obj'],
    #     'cart_total_amount': cart_total_amount,
    #     'totalitems': len(request.session['cart_data_obj']),
    #     'form':paypal_payment_button,
    # }
    return render(request, 'core/checkout.html',{
        'cart_data':request.session['cart_data_obj'],
        'cart_total_amount': cart_total_amount,
        'totalitems': len(request.session['cart_data_obj']),
        'form':paypal_payment_button,
    })

@csrf_exempt
@login_required
def payment_success(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])
    
        order = CartOrder.objects.filter(user=request.user)
        # for order in orders:
        #     order_cart_item =CartOrderItems.objects.get(order=order)
    
    context={
        'cart_data':request.session['cart_data_obj'],
        'cart_total_amount': cart_total_amount,
        'totalitems': len(request.session['cart_data_obj']),
        'order':order,
        # 'order_cart':order_cart_item
    }

    return render(request,'core/payment-success.html',context)

@login_required
def payment_failed(request):
    return render(request,'core/payment-failed.html')

@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user)
    profile =Profile.objects.get(user=request.user)
    
    orders_list = CartOrder.objects.annotate(month=ExtractMonth('date_order')).values("month").annotate(count=Count("id")).values("month","count")
    
    month = []
    total_orders = []

    for i in orders_list:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i["count"])
    context = {
        'profile':profile,
        'orders':orders,
        'orderslists':orders_list,
        'month':month,
        'total_orders':total_orders
       
    }
    return render(request,'core/dashboard.html',context)

def order_detail(request,id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products_order = CartOrderItems.objects.filter(order=order)
    context={
        'products':products_order
    }
    return render(request,'core/detail-order.html',context)

@login_required
def wishlist(request):
    wislist = Wishlist.objects.all()
    context = {
        'wishlist':wislist
    }
    return render(request,'core/wishlist.html',context)

def get_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context={}

    wishlist_count =Wishlist.objects.filter(product=product,user=request.user).count()

    if wishlist_count > 0:
        context = {
            'bool':True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product = product,
            user = request.user
        )
        context={
            'bool':True
        }
    return JsonResponse(context)

def remove_wishlist(request):
    product_id=request.GET['id']
    wishlist =  Wishlist.objects.filter(user=request.user)

    wish = Wishlist.objects.get(id=product_id)
    wish.delete()

    context={
        'bool':True,
        'wishlist':wishlist
    }
    wishlist_json = serializers.serialize('json',wishlist)
    data =  render_to_string("core/async/wishlist-list.html",context)
    return JsonResponse(
        {
            'data':data,
            'wishjson':wishlist_json,
        }
    )

def contact(request):
    return render(request,'core/contact.html')