"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from home.views import CancelView, StripeCartCheckoutPayment, StripeCheckoutPayment, SuccessView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name="register"),
    path('', views.login_usr, name= 'login_usr'),
    path('home/', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('search/', views.search, name="search"),
    path('products/', views.products, name="products"),
    path('checkout/<int:pid>', views.checkout, name="checkout"),
    path('login/', views.login_usr, name="login_usr"),
    path('logout/', views.logout_user, name='logout'),
    path('add/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('cart_detail/', views.cart_detail, name="cart_detail"),
    path('cartcheckout/', views.cart_checkout, name="cartcheckout"),
    path("products/<int:vid>", views.productView, name="ProductView"),
    path('contact/', views.contact_us, name="contact"),
    path('accessories/', views.accessories, name="accessories"),
    path('mobiles/', views.mobiles, name="mobiles"),
    path('fashion/', views.fashion, name="fashion"),
    path('demo/', views.demo, name="demo"),
    path('invoice/', views.invoice, name='invoice'),
    path("create-checkout-session/<int:pk>/",
        StripeCheckoutPayment.as_view(),
        name="create-checkout-session",),
    path("success/", views.Confirm, name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("create-cartcheckout-session/",
        StripeCartCheckoutPayment.as_view(),
        name="create-cartcheckout-session",),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path("verifynumber/",views.verifynumber,name="verifynumber"),
    path('verify/<str:phoneNo>/', views.verify, name='verify'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)