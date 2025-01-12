from django.shortcuts import redirect ,render
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from random import  randint
from .models import *
# import razorpay


# from essence.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY


# Create your views here.

def home(Request):
    data = Product.objects.all()
    data = data[::-1]
    data = data[0:50]
    brand = Brand.objects.all()
    subcategory = Subcategory.objects.all()
    return render(Request,"index.html",{'data':data,'brand':brand,'subcategory':subcategory})

    
def contact(Request):
    if(Request.method=="POST"):
        c = ContactUs()
        c.name = Request.POST.get("name")
        c.email = Request.POST.get("email")
        c.phone = Request.POST.get("phone")
        c.subject = Request.POST.get("subject")
        c.message = Request.POST.get("message")
        c.save()
        messages.success(Request,"Thanks to Share Your Query With Us. Our Team Will Contact You Soon!!!")
    brand = Brand.objects.all()
    subcategory = Subcategory.objects.all()
    maincategory = Maincategory.objects.all()
    return render(Request,"contact.html",{'brand':brand,'maincategory':maincategory,'subcategory':subcategory})

    

def shop(Request,mc,sc,br):
    if(mc=="All" and sc=="All" and br=="All"):
        data = Product.objects.all()
    elif(mc!="All" and sc=="All" and br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc))
    elif(mc=="All" and sc!="All" and br=="All"):
        data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc))
    elif(mc=="All" and sc=="All" and br!="All"):
        data = Product.objects.filter(brand=Brand.objects.get(name=br))
    elif(mc!="All" and sc!="All" and br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc))
    elif(mc!="All" and sc=="All" and br!="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br))
    elif(mc=="All" and sc!="All" and br!="All"):
        data = Product.objects.filter(brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc))
    else:
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc))
    count = len(data)
    data = data[::-1]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    return render(Request,"shop.html",{'data':data ,'subcategory':subcategory,'maincategory':maincategory,'brand':brand,'sc':sc,'mc':mc,'br':br,'count':count})


def priceFilter(Request,mc,sc,br):
    if(Request.method=="POST"):
        min = Request.POST.get("min")
        max = Request.POST.get("max")
        if(mc=="All" and sc=="All" and  br=="All"):
            data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max)
        elif(mc!="All" and sc=="All" and br=="All"):
            data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max,maincategory=Maincategory.objects.get(name=mc))
        elif(mc=="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max,subcategory=Subcategory.objects.get(name=sc))
        elif(mc=="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max,brand=Brand.objects.get(name=br))
        elif(mc!="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max,maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc))
        elif(mc!="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max,maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br))
        elif(mc=="All" and sc!="All" and br!="All"):
            data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max,brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc))
        else:
            data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max,maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc))
        # data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max)
        count = len(data)
        data = data[::-1]
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        brand = Brand.objects.all()
        return render(Request,"shop.html",{'data':data,'maincategory':maincategory,'subcategory':subcategory,'brand':brand,'mc':mc,'sc':sc,'br':br,'count':count})
    else:
        return redirect("/shop/All/All/All")
    
def searchPage(Request):
    if(Request.method=="POST"):
        search = Request.POST.get("search")
        data = Product.objects.filter(Q(name__icontains=search)|Q(color__icontains=search)|Q(size__icontains=search)|Q(description__icontains=search))
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        brand = Brand.objects.all()
        count = len(data)
        return render(Request,"shop.html",{'data':data,'maincategory':maincategory,'subcategory':subcategory,'brand':brand,'mc':'All','sc':'All','br':'All','count':count})
    else:
        return redirect("/shop/All/All/All")



def sortFilterPage(Request,mc,sc,br):
    if(Request.method=="POST"):
        sort = Request.POST.get("sort")
        if(sort=="Newest"):
            sort="id"
        elif(sort=="LTOH"):
            sort="-finalprice"
        else:
            sort="finalprice"
        if(mc=="All" and sc=="All" and br=="All"):
            data = Product.objects.all().order_by(sort)
        elif(mc!="All" and sc=="All" and br=="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by(sort)
        elif(mc=="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by(sort)
        elif(mc=="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(brand=Brand.objects.get(name=br)).order_by(sort)
        elif(mc!="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by(sort)
        elif(mc!="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br)).order_by(sort)
        elif(mc=="All" and sc!="All" and br!="All"):
            data = Product.objects.filter(brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by(sort)
        else:
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by(sort)
        # data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max)
        count = len(data)
        data = data[::-1]
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        brand = Brand.objects.all()
        return render(Request,"shop.html",{'data':data,'maincategory':maincategory,'subcategory':subcategory,'brand':brand,'mc':mc,'sc':sc,'br':br,'count':count})
    else:
        return redirect("/shop/All/All/All")
    

@login_required(login_url="/login/")
def profilePage(Request):
    user = User.objects.get(username=Request.user.username)
    if(user.is_superuser):
        return redirect("/admin")
    else:
        buyer = Buyer.objects.get(username=user.username)
        orders = Checkout.objects.filter(user=buyer)
        
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    return render(Request,"profile.html",{'data':buyer,'orders':orders})

    
def addtocart(Request, id):
    # Request.session.flush()
    cart = Request.session.get('cart', None)
    p = Product.objects.get(id=id)
    cartCount = Request.session.get("cartCount",0)
    if (cart is None):
        cart = {str(p.id): {'pid': p.id, 'pic': p.pic1.url, 'name': p.name, 'color': p.color, 'size': p.size, 'price': p.finalprice,
                            'qty': 1, 'total': p.finalprice, 'maincategory': p.maincategory.name, 'subcategory': p.subcategory.name, 'brand': p.brand.name}}
    else:
        if (str(p.id) in cart):
            item = cart[str(p.id)]
            item['qty'] = item['qty']+1
            item['total'] = item['total']+item['price']
            
            cart[str(p.id)] = item
            
            
            
            
        else:
            cart.setdefault(str(p.id), {'pid': p.id, 'pic': p.pic1.url, 'name': p.name, 'color': p.color, 'size': p.size, 'price': p.finalprice,
                            'qty': 1, 'total': p.finalprice, 'maincategory': p.maincategory.name, 'subcategory': p.subcategory.name, 'brand': p.brand.name})

    Request.session['cartCount']=cartCount+1
    Request.session['cart'] = cart
    Request.session.set_expiry(60*60*24*45)
    
    return redirect("/cart")


def cartpage(Request):
    cart = Request.session.get('cart', None)
    c = []
    total = 0
    shipping = 0

    if (cart is not None):
        for value in cart.values():
            total = total + value['total']
            c.append(value)
        if (total < 1000 and total > 0):
            shipping = 150
    final = total+shipping
    

    return render(Request, "cart.html", {'cart': c, 'total': total, 'shipping': shipping, 'final': final})



def deletecart(Request, pid):
    cart = Request.session.get("cart",None)
    cartCount = 0
    if(cart and pid in cart):
        del cart[pid]
        Request.session['cart']=cart

        total = 0
        for value in cart.values():
            total = total+value['total']
            cartCount = cartCount+value['qty']
        if(total<1000 and total>0):
            shipping = 150
        else:
            shipping = 0
        Request.session['total']=total
        Request.session['shipping']=shipping
        Request.session['final']=total+shipping
        Request.session['cartCount']=cartCount
    # cart = Request.session.get('cart', None)
    # cartCount = 0
    # if (cart):
    #     for key in cart.keys():
    #         if (str(pid) == key):
    #             del cart[key]
                
    #             break
               
    #     Request.session['cart'] = cart
    #     Request.session['cartCount']=cartCount
    return redirect("/cart")

def updateCart(Request, pid, op):
    cart = Request.session.get('cart', None)
    if (cart):
        for key, value in cart.items():
            if (str(pid) == key):
                if (op == "inc"):
                    value['qty'] = value['qty']+1
                    value['total'] = value['total']+value['price']
                elif (op == 'dec' and value['qty'] > 1):
                    value['qty'] = value['qty']-1
                    value['total'] = value['total']-value['price']
                cart[key] = value
                break
        Request.session['cart'] = cart
    return redirect("/cart")


def signup(Request):
    if(Request.method=="POST"):
        name = Request.POST.get("name")
        username = Request.POST.get("username")
        email = Request.POST.get("email")
        phone = Request.POST.get("phone")
        password = Request.POST.get("password")
        cpassword = Request.POST.get("cpassword")
        if(password==cpassword):
            try:
                user = User(username=username)
                user.set_password(password)
                user.save()
                buyer = Buyer()
                buyer.name = name
                buyer.username = username
                buyer.email = email
                buyer.phone = phone
                buyer.password = password
                buyer.save()
                return redirect("/login")
            except:
                messages.error(Request,"User Name Already Exist!!!")                
        else:
            messages.error(Request,"Password and Confirm Password Doesn't Matched!!!")
    return render(Request,"signup.html")
    

def loginPage(Request):
    if(Request.method=='POST'):
        username = Request.POST.get("username")
        password = Request.POST.get("password")
        user = authenticate(username=username,password=password)
        if(user is not None):
            login(Request,user)
            if(user.is_superuser):
                return redirect("/admin")
            else:
                return redirect("/profile")
        else:
            messages.error(Request,"Invalid Username or Password!!!!")
    brand = Brand.objects.all()
    subcategory = Subcategory.objects.all()
    maincategory = Maincategory.objects.all()
    return render(Request,"login.html",{'maincategory':maincategory,'subcategory':subcategory,'brand':brand})

def logoutPage(Request):
    logout(Request)
    return redirect("/login/")

@login_required(login_url="/login/")
def updateprofile(Request):
    user = User.objects.get(username=Request.user)
    if(user.is_superuser):
        return redirect("/admin")
    else:
        buyer = Buyer.objects.get(username=user.username)
        if(Request.method == "POST"):
            buyer.name = Request.POST.get("name")
            buyer.email = Request.POST.get("email") 
            buyer.phone = Request.POST.get("phone")
            buyer.addressline1 = Request.POST.get("addressline1")
            buyer.addressline2 = Request.POST.get("addressline2")
            buyer.addressline3 = Request.POST.get("addressline3")
            buyer.pin = Request.POST.get("pin")
            buyer.city = Request.POST.get("city")
            buyer.state = Request.POST.get("state")
            if(Request.FILES.get("pic")):
                buyer.pic = Request.FILES.get("pic")
            buyer.save()
            return redirect("/profile")    
    return render(Request,"update-profile.html",{'data':buyer})


def singleproduct(Request,id):
    data = Product.objects.get(id=id)
    return render(Request,"single.html",{'data':data})




def checkoutPage(Request):
    try:
        buyer = Buyer.objects.get(username=Request.user)
        cart = Request.session.get('cart', None)
        c = []
        total = 0
        shipping = 0
        if (cart is not None):
            for value in cart.values():
                total = total + value['total']
                c.append(value)
            if (total < 1000 and total > 0):
                shipping = 150
        final = total+shipping
        if(total==0):
            return redirect("/cart/")
        return render(Request, "checkout.html",{'user':buyer,'cart':c,'total':total,'shipping':shipping,'final':final})
    except:
        return redirect("/admin")
    

# client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))   
@login_required(login_url='/login/')    
def orderpage(Request):
    if(Request.method=="POST"):
        mode = Request.POST.get("mode")
        user = Buyer.objects.get(username=Request.user.username)
        cart = Request.session.get('cart',None)
        if(cart is None):
            return redirect("/cart")
        else:
            check = Checkout()
            check.user = user
            total = 0
            shipping = 0
            for value in cart.values():
                total = total + value['total']
            if (total < 1000 and total > 0):
                shipping = 150
            final = total+shipping
            check.total = total
            check.shipping = shipping
            check.final=final
            check.save()
            for value in cart.values():
                cp = CheckoutProducts()
                cp.checkout = check
                cp.p = Product.objects.get(id=value['pid'])
                cp.qty = value['qty']
                cp.total = value['total']
                cp.save()  
                Request.session['cartCount']=0
                Request.session['cart']={}

            mode = Request.POST.get("mode")    
            if(mode=="COD"):
                return redirect("/confirmation")
            else:
                
                
                return redirect("/confirmation")
                    
            #     orderAmount = check.final*100
            #     orderCurrency = "INR"
            #     paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
            #     paymentId = paymentOrder['id']
            #     check.mode="Net Banking"
            #     check.save()
            #     return render(Request,"pay.html",{
            #         "amount":orderAmount,
            #         "api_key":RAZORPAY_API_KEY,
            #         "order_id":paymentId,
            #         "User":user
                # })
    else:
        return redirect("/checkout")
    
# @login_required(login_url='/login/')
# def paymentSuccess(request,rppid,rpoid,rpsid):
#     buyer = Buyer.objects.get(username=request.user)
#     check = Checkout.objects.filter(buyer=buyer)
#     check=check[::-1]
#     check=check[0]
#     check.rppid=rppid
#     # check.rpoid=rpoid
#     # check.rpsid=rpsid
#     check.paymentstatus=1
#     check.save()
#     return redirect('/confirmation/')    
    
def confirmationPage(Request):
    return render(Request,'confirmation.html')


def forgetPasswordPage1(Request):
    if(Request.method=="POST"):
        username = Request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            if(user.is_superuser):
                return redirect("/admin/")
            else:
                Request.session['resetuser'] = username
                num = randint(100000,999999)
                buyer = Buyer.objects.get(username=username)
                buyer.otp = num
                buyer.save() 
                subject = 'OTP for Password Reset- Team Essence'
                message = "OTP for Password Reset is "+str(num)+"\nNever Share Your OTP With Anyone"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [buyer.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return redirect("/forget-2/")
        except:
            messages.error(Request,"Invalid Username")
    brand = Brand.objects.all()
    subcategory = Subcategory.objects.all()
    maincategory = Maincategory.objects.all()
    return render(Request,"forget-1.html",{'maincategory':maincategory,'subcategory':subcategory,'brand':brand})

def forgetPasswordPage2(Request):
    username = Request.session.get("resetuser",None)
    if(Request.method=="POST" and username):
        otp = Request.POST.get("otp")
        try:
            buyer = Buyer.objects.get(username=username)
            if(buyer.otp == int(otp)):
                Request.session['otp']=otp
                return redirect("/forget-3/")
            else:
                messages.error(Request,"Invalid OTP")                
        except:
            messages.error(Request,"Invalid Username")
    brand = Brand.objects.all()
    subcategory = Subcategory.objects.all()
    maincategory = Maincategory.objects.all()
    return render(Request,"forget-2.html",{'maincategory':maincategory,'subcategory':subcategory,'brand':brand})

def forgetPasswordPage3(Request):
    otp = Request.session.get("otp",None)
    if(otp):
        if(Request.method=="POST"):
            resetUser = Request.session.get("resetuser",None)
            if(resetUser and otp):
                buyer = Buyer.objects.get(username=resetUser)
                if(int(otp)==buyer.otp):
                    password = Request.POST.get("password")
                    cpassword = Request.POST.get("cpassword")
                    if(password!=cpassword):
                        messages.error(Request,"Password and Confirm Password Doesn't Matched!!!!")
                    else:
                        user = User.objects.get(username=resetUser)
                        user.set_password(password)
                        user.save()
                        subject = 'Password Reset SuccessFully- Team Essence'
                        message = "Your Password Has Been Reset Successfully Now you can login to Your Account"
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [buyer.email, ]
                        send_mail( subject, message, email_from, recipient_list )
                        del Request.session['resetuser']
                        del Request.session['otp']
                        return redirect("/login/")
                else:
                    messages.error(Request,"Un-Authorised!!!")                
            else:
                messages.error(Request,"Un-Authorised!!!")
                brand = Brand.objects.all()
                subcategory = Subcategory.objects.all()
                maincategory = Maincategory.objects.all()
                return render(Request,"forget-3.html",{'maincategory':maincategory,'subcategory':subcategory,'brand':brand})
    else:
        return redirect("/forget-1/")