from math import ceil
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import (Cart, Products, Category,CustomUser, Contact,CheckoutDetails,) 
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from twilio.rest import Client

# Create your views here.




stripe.api_key = settings.STRIPE_SECRET_KEY

account_sid = 'ACee0fefeb62e474ada2968d54cc64b7fa'
auth_token = 'baf64cb1a91ace07d2d0bf1c4bfacc0c'
verify_sid = 'VA224108f166e8f6548b53fee7f234fdd2'
client = Client(account_sid,auth_token)
print('client: ', client)


def home(request):
    ''' render all product category basd on category availble in data base'''
    category = Category.objects.all()
    context = {'category': category}
    return render(request,'log/home.html',context)


def about(request):
    ''' about page of company and all details for contact and log in new user for continue shooping on site.'''
    return render(request, 'log/about.html')


@login_required(login_url='login_usr')
def search(request):
    '''srach button in navigation bar for displaying eesire product of user request.'''
    if request.method =='POST':
        search_query = request.POST['search_query']
        prod = Products.objects.filter(product_name__contains = search_query) 
        return render(request, 'log/search.html' , {'query': search_query, 'prod': prod})
    else:
        return render(request,'log/search.html', {})



########           product view and details views       ###############################
@login_required(login_url='login_usr')
def products(request):
    '''display all products available oin site with all cateogry.'''
    products = Products.objects.all()
    p = Paginator(products, 8)
    #print(p)
    page_number = request.GET.get('page')
    print(page_number)
    try:
        page= p.get_page(page_number)  # returns the desired page object
        print(page)    
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page = p.page(p.num_pages)
    params  = {
        'products': page,
        'page_obj': page_number
    }
   # print('params', params)
    return render(request, 'log/products.html', params)


@login_required(login_url='login_usr')
def productView(request, vid):
    ''' saperated productview based on request made by user and display details of that particluar prods....'''
    product = Products.objects.filter(id = vid)
    if request.method == "POST":
        messages.success(request, f"{product.product_name} added to your cart.")
        return redirect("cart:add_to_cart", product_id=product.id)
    context = {"product": product,}
    return render(request,"log/productview.html", context)


@login_required(login_url='login_usr')
def checkout(request,pid):
    '''check out page for rendering amount and details for delivering address of customer and save that adderss in database.'''
    product = Products.objects.filter(id = pid)
    print('product',product)
    #total_price = sum(item.quantity * item.product.price for item in product)
    context = {"product":product}
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        phone_number = request.POST.get('phone_address', '')
        email_address = request.POST.get('email_address', '')
        pincode = request.POST.get('pincode', '')
        address = request.POST.get('address', '')
        checkout = CheckoutDetails(full_name=full_name,phone_number=phone_number,email_address=email_address,pincode=pincode,address=address)
        checkout.save()     
    return render(request,'log/checkout.html',context)



#################  register and login function for customer   #######################
def register(request):
    '''registration for new user in company databse and use that information for further for access website for shopping.'''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_usr')
    else:
        form = RegistrationForm()
    return render (request, 'log/register.html', {"form": form})        


def login_usr(request):
    '''log in function for giving access of site whoch user are alreadty registered in database and if user not register its redirect to registration form'''
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid(): 
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_exist = CustomUser.objects.filter(email=email).exists()
            if not user_exist:
                return redirect('register')
            else:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    request.session['username'] = email
                    request.session['password'] =password
                    return redirect('verifynumber')
                    #login(request, user)
                    #return redirect('home')
    else:
        form = AuthenticationForm()
    if not request.user.is_authenticated:
        messages.info(request, 'You are not authenticated. Please log in.')
    return render(request, 'log/login.html', {'form':form})     
  

@login_required(login_url='login_usr')
def logout_user(request):
    logout(request)
    return redirect('login_usr') 


def verifynumber(request):
 '''phone num input from user and send otp on that number'''
 if request.method == "POST":
    phone_no = request.POST.get('phone_no')
    return redirect('verify', phoneNo=phone_no) 
 return render(request,'log/verifynum.html')


def verify(request, phoneNo):
    '''It takes OTP input from user and validate it on system and if otp approved then user get logged in on website..'''
    if request.method == 'POST':
        code = request.POST.get('code')
        verification_check = client.verify.services(verify_sid).verification_checks.create(to=f"+91{phoneNo}",code=code)
        if verification_check.status == "approved":
            user = authenticate(request,username=request.session.get('username'),password=request.session.get('password'))
            login(request,user)
            return redirect('home')
        else:
            return redirect('login_usr')
        
    verification = client.verify.services(verify_sid).verifications.create(to=f"+91{phoneNo}",channel='sms')
    return render(request,'log/verify.html')



######################################    cart functionality for add, delete, and remove     ###########################
@login_required(login_url='login_usr')
def add_to_cart(request, product_id):
    '''adding product in cart using product id and if already added the increase quanity of that product'''
    product = get_object_or_404(Products, id=product_id)
    print(product)
    cart_item = Cart.objects.filter(user=request.user, product__product_name= product).first()
    print('cart_item',cart_item)
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Your product has been added to yur cart, please check.")
    else:
        Cart.objects.create(user=request.user, product=product)
        messages.success(request, "Your product has been added to yur cart, please check.")  
    return redirect('cart_detail')        
       
  
@login_required(login_url='login_usr')
def remove_from_cart(request, cart_item_id):
    '''remove product form cart if exist and deduct price from total amount'''
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    if cart_item.user == request.user:
        cart_item.delete()
        messages.success(request, "your product has been deleted from cart")
    return redirect('cart_detail')


@login_required(login_url='login_usr')
def cart_detail(request):
    '''get product of cart and its details and button for remove product '''
    cart_items = Cart.objects.filter(user= request.user)
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    count = cart_items.count
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'count': count,
    }
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        phone_number = request.POST.get('phone_address', '')
        email_address = request.POST.get('email_address', '')
        pincode = request.POST.get('pincode', '')
        address = request.POST.get('address', '')
        checkout = CheckoutDetails(full_name=full_name,phone_number=phone_number,email_address=email_address,pincode=pincode,address=address)
        checkout.save()
    return render(request, 'log/cart_detail.html', context)



############################################        cart check out           ##################################################################
@login_required(login_url='login_usr')
def cart_checkout(request):
    '''check out price of product and total price of products of user purchase'''
    c_checkout = Cart.objects.filter(user= request.user)
    print('c_checkout', c_checkout)
    total_price = sum(item.quantity * item.product.price for item in c_checkout)
    context = {
        'product': c_checkout,
        'total_price': total_price,
    }
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        phone_number = request.POST.get('phone_address', '')
        email_address = request.POST.get('email_address', '')
        pincode = request.POST.get('pincode', '')
        address = request.POST.get('address', '')
        checkout = CheckoutDetails(full_name=full_name,phone_number=phone_number,email_address=email_address,pincode=pincode,address=address)
        checkout.save()
        

    return render(request, 'log/cartcheckout.html', context)



#################################  navigation bar fuctions       ########################################################################### 
def contact_us(request):
    '''contact form for reaching out org with details of customer.'''
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        inquiry = request.POST.get('inquiry', '')
        contact = Contact(name=name, email=email,phone=phone,inquiry=inquiry)
        contact.save()
    return render(request, 'log/contact_us.html',)   


@login_required(login_url='login_usr')
def accessories(request):
    '''specified accessories view '''
    products= Products.objects.all().filter(c_name=1).order_by('-price')
   #print(products)
    context = {'products':products}
    return render(request, 'log/accessories.html', context)


@login_required(login_url='login_usr')
def mobiles(request):
    products= Products.objects.all().filter(c_name=2).order_by('-price')
   # print(products)
    context = {'products':products}
    return render(request, 'log/mobiles.html', context)


@login_required(login_url='login_usr')
def fashion(request):
    products= Products.objects.all().filter(c_name=3).order_by('-price')
   # print(products)
    context = {'products':products}
    return render(request, 'log/fashion.html', context)


def demo(request):
    return render(request, 'log/demo.html')


@login_required(login_url='login_usr')
def invoice(request,cid, pid):
    c_details = Cart.objects.get(id=cid)
    p_details = CheckoutDetails.objects.get(id=pid)
    context = {"c_details": c_details, "p_details": p_details}  
    return render(request, 'log/invoice.html', context)


class StripeCheckoutPayment(View):
    '''stripe payment using test mode and create user which made payment and store in stripe account manager'''
    def post(self, request, *args, **kwargs):
        print('price', self.kwargs['pk'])
        price = Products.objects.get(id = self.kwargs['pk'])
    #    print(price.product_name)
     #   print(price.product_id)
      #  print(price.price)
       # print(price.details)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data":{
                        "currency": "usd",
                        "unit_amount": int(price.price) * 100,
                        "product_data":{
                            "name": price.product_name,
                            "description":price.details,
                            "images": [
                                f"{settings.BACKEND_DOMAIN}/{price.img}"
                            ],
                        },      
                    },
                    "quantity": 1
                }
            ],
            metadata={"product_id": price.product_id},
            mode= "payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        stripe.Customer.create(
            name="Pacific Group",
            address={
            "line1": "Ribda, Rajkot",
            "postal_code": "394101",
            "city": "Rajkot",
            "state": "GJ",
            "country": "IND",
        },
)
        return redirect(checkout_session.url)

class StripeCartCheckoutPayment(View):
    '''stripe cart chehckout view for confirm order and make payment with submit shipping address.'''
    def post(self,request, *args, **kwargs):
        price = Cart.objects.filter(user= request.user)
        print('p',price)
        total_price = sum(item.quantity * item.product.price for item in price)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data":{
                        "currency": "usd",
                        "unit_amount": total_price * 100,
                        "product_data":{
                            "name": "Total Amount",
                            "description":"For complete your order.",
                            "images": [
                                f"Images"
                            ],
                        },
                    },
                    "quantity": '1'
                }
            ],
            metadata={"product_id": '1'},
            mode= "payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        stripe.Customer.create(
            name="Pacific Engitech",
            address={
            "line1": "Ribda, Rajkot",
            "postal_code": "394101",
            "city": "Surat",
            "state": "GJ",
            "country": "IND",
        },
)
        return redirect(checkout_session.url)

class SuccessView(TemplateView):
    template_name = "log/checkout.html"

def Confirm(request):
    return render(request, 'log/success.html')

class CancelView(TemplateView):
    template_name = "log/cancel.html"    
    
    