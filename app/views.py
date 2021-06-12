from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
import datetime
from django.http import HttpResponse
from django.conf import settings
import random
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
# Create your views here.


def loginPage(req):
    if req.method == 'POST':
        email = req.POST['email']
        password = req.POST['pass']
        customer = CustomerRegister.objects.get(Email=email)
        print('------1----------', customer.First_Name)
        if customer.Password == password:
            req.session['firstName'] = customer.First_Name
            req.session['Customer_id'] = customer.Customer_id
            req.session['email'] = customer.Email
            return redirect('indexPage')
        else:
            message = "Your Password is incorrct or User does not exist"
            return render(req, 'app/login.html', {'message': message})
    return render(req, 'app/login.html')


def registerPage(req):
    if req.method == 'POST':
        firstname = req.POST['fn']
        lastname = req.POST['ln']
        email = req.POST['email']
        password = req.POST['pass1']
        confirm_password = req.POST['pass2']
        check_customer = CustomerRegister.objects.filter(Email=email)
        print(check_customer)
        if check_customer:
            message = "This user is already exist"
            return render(req, "app/register.html", {'message': message})
        else:
            if password == confirm_password:
                cus = CustomerRegister(
                    First_Name=firstname, Last_Name=lastname, Email=email, Password=password)
                cus.save()
                return redirect('loginPage')
            else:
                message = 'password & Confirm password does not match !!'
                return render(req, 'app/register.html', {'message': message})
    return render(req, 'app/register.html')


def forgotPassword(req):
    if req.method == 'POST':
        email1 = req.POST.get('EMail')
        check_email = CustomerRegister.objects.filter(Email=email1).first()
        if check_email:
            req.session['email'] = email1
            otp = str(random.randint(100000, 999999))
            subject = 'Reset Password Otp'
            message = f'Your OTP is {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email1, ]
            send_mail(subject, message, email_from, recipient_list)
            req.session['otp'] = otp
            return render(req, 'app/forgotPasswordOtp.html')
        else:
            msg = "Wrong Otp"
            return render(req, 'app/forgotPassword.html', {'message': msg})
    return render(req, 'app/forgotPassword.html')


def forgotPasswordOtp(req):
    session_otp = req.session['otp']
    if req.method == 'POST':
        otp = req.POST['otp']
        if session_otp == otp:
            return render(req, 'app/resetPassword.html')
        else:
            message = 'Wrong Otp, Enter again!'
            return render(req, 'app/forgotPasswordOtp.html', {'message': message})


def resetPassword(req):
    if req.method == 'POST':
        password = req.POST['pass1']
        confirm_password = req.POST['pass2']
        if password == confirm_password:
            email = req.session['email']
            CustomerRegister.objects.filter(
                Email=email).update(Password=password)
            return redirect('loginPage')
        else:
            message = 'Password and Confirm password both are diffrent!'
            return render(req, 'app/resetPassword.html', {'message': message})


def index(req):
    firstName = req.session['firstName']
    product = None
    category = Category.objects.all()
    cat_id = req.GET.get('category')
    print(cat_id)
    if cat_id:
        product = Product.objects.all().filter(Category_id=cat_id)
    else:
        product = Product.objects.all()
    user = req.session['Customer_id']
    order, created = Order.objects.get_or_create(Customer_id_id=user)
    items = order.orderitem_set.all()
    cartItem = order.get_cart_item
    return render(req, 'app/index.html', {'fn': firstName, 'product': product, 'category': category, 'cartItem': cartItem})


@login_required
def cart(req):
    user = req.session['Customer_id']
    order, created = Order.objects.get_or_create(Customer_id_id=user)
    items = order.orderitem_set.all()
    cartItem = order.get_cart_item

    # items = order
    # item1 = OrderItem.objects.all().filter(Customer_id=user)
    # newTotal = 0
    # for item in OrderItem.objects.all().filter(Customer_id=user):
    #     newTotal += (float(item.Product_id.Price)*item.Qty)
    # cartTotal = newTotal
    # cartTotal = Order.objects.all().filter(Customer_id=user)
    # print(cartTotal, '-------------1----------------')
    return render(req, 'app/cart.html', {'item': items, 'cartTotal': order, 'cartItem': cartItem})


@login_required
def updateItem(req):
    data = json.loads(req.body)
    productId = data['productId']
    action = data['action']

    user = req.session['Customer_id']

    product = Product.objects.get(Product_id=productId)
    order, created = Order.objects.get_or_create(
        Customer_id=user)
    orderitem, created = OrderItem.objects.get_or_create(
        Order_id=order, Product_id=product)

    if action == 'add':
        orderitem.Qty = (orderitem.Qty + 1)
    elif action == 'remove':
        orderitem.Qty = (orderitem.Qty - 1)
    orderitem.save()

    if orderitem.Qty <= 0:
        orderitem.delete()

    return JsonResponse('Item Was Added', safe=False)


@login_required
def checkOut(req):
    if req.method == 'POST':
        firstname = req.POST['fname']
        lastname = req.POST['lname']
        phone = req.POST['number']
        address = req.POST['add1']
        chkout = ShippingAddress(
            First_Name=firstname, Last_Name=lastname, num=phone, address=address).save()
        user = req.session['Customer_id']
        return redirect('indexPage')
    return render(req, 'app/checkout.html')
