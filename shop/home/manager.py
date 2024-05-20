from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    '''custom user manager using base user manager for create super user and normal user and register on website server to acceess services
    from site and control admin side responsibility for super user...'''
    def createuser(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_("Email is required for login, please enter email"))
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    
    def create_superuser(self, email,password,**extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser is must set is_staff = True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser  must set is_superuser= True"))
        return self.createuser(email,password,**extra_fields)