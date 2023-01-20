from django.shortcuts import render
from django.http import JsonResponse
from .models import * 
import json
def store(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cart_items = order['get_cart_items']


    products = Product.objects.all()
    brands = Brand.objects.all()
    categorys = Category.objects.all()
    context = {'products':products,'brands':brands,'categorys':categorys,'cartItems':cart_items,'shipping':False}
    
    return render(request,'store/store.html',context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
        cart_items = order['get_cart_items']

    products = Product.objects.all()
    brands = Brand.objects.all()
    categorys = Category.objects.all()
    context = {'products':products,'brands':brands,'categorys':categorys,'items':items,'order':order,'cartItems':cart_items,'shipping':False}
    return render(request,'store/cart.html',context)

def checkout(request):
    

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
        cart_items = order['get_cart_items']

    cart_items = order.get_cart_items
    products = Product.objects.all()
    brands = Brand.objects.all()
    categorys = Category.objects.all()
    context = {'products':products,'brands':brands,'categorys':categorys,'items':items,'order':order,'cartItems':cart_items,'shipping':False}
    return render(request,'store/checkout.html',context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action) 
    print('ProductId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.qtd = (orderItem.qtd +1)
    elif action == 'remove':
        orderItem.qtd = (orderItem.qtd - 1)
    
    orderItem.save()

    if orderItem.qtd <= 0:
        orderItem.delete()

    return JsonResponse('item was added',safe=False)