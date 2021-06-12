from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.loginPage, name="loginPage"),
    path('register', views.registerPage, name="registerPage"),
    path('index/', views.index, name="indexPage"),

    path('forgotpassword', views.forgotPassword, name="forgotPassword"),
    path('forgotpasswordotp', views.forgotPasswordOtp, name="forgotPasswordOtp"),
    path('resetpassword', views.resetPassword, name="resetPassword"),
    path('cart/', views.cart, name="cart"),
    path('updateItem/', views.updateItem, name="updateItem"),
    path('checkOut/', views.checkOut, name="checkOut"),


    #    path('about/',views.About,name="aboutus"),
    #    path('contact/',views.Contact1,name="contactus"),
    #    path('tracker/',views.Tracker,name="trackingstatus"),
    #    path('search/',views.Search,name="search"),
    #    path('product/<int:id>',views.Productview,name="productview"),
    #    path('checkout/',views.Checkout,name="checkout"),
    #    path('showorders/',views.ShowOrders,name="ShowOrders"),

]
