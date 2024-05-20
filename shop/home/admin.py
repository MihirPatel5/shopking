from django.contrib import admin
from .models import Category, Contact, Invoice,Products,CustomUser,Cart,CustomUserManager,CheckoutDetails
from django.contrib.auth.admin import UserAdmin
from .forms import RegistrationForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    form = RegistrationForm()
  
    model = CustomUser
    list_display = ["email", "is_staff", "is_active"]
    list_filter = ["email", "is_staff", "is_active"]
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "is_staff",
                "is_active","groups","user_permissions",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(Category)
admin.site.register(Products)    
admin.site.register(CustomUser)
admin.site.register(Cart)
admin.site.register(Contact)
admin.site.register(CheckoutDetails)
admin.site.register(Invoice)

