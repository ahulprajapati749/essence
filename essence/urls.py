"""
URL configuration for essence project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views 



admin.site.site_header = "Essence"
admin.site.site_title = "Essence Admin Portal"
admin.site.index_title = "Welcome to Essence Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('price-filter/<str:mc>/<str:sc>/<str:br>/',views.priceFilter),
    path('sort-filter/<str:mc>/<str:sc>/<str:br>/',views.sortFilterPage),
    path('shop/<str:mc>/<str:sc>/<str:br>/',views.shop),
    path('search/',views.searchPage),
    path('single/<int:id>/',views.singleproduct),
    path('contact/',views.contact),
    path('login/',views.loginPage),
    path('profile/',views.profilePage),
    path('update-profile/',views.updateprofile),
    path('signup/',views.signup),
    path('logout/',views.logoutPage),
    path('addtocart/<int:id>/',views.addtocart),
    path('cart/',views.cartpage),
     path('delete-cart/<str:pid>/',views.deletecart),
     path('update-cart/<int:pid>/<str:op>/',views.updateCart),
     path('checkout/',views.checkoutPage),
     path('order/',views.orderpage),
     path('confirmation/',views.confirmationPage),
     path('forget-1/',views.forgetPasswordPage1),
    path('forget-2/',views.forgetPasswordPage2),
    path('forget-3/',views.forgetPasswordPage3),
    # path('forget-3/',views.forgetPasswordPage3),
#    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/',views.paymentSuccess),
   
   
   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

