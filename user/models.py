from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """custom user manager class for chainable querysets"""
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model class"""
    first_name = models.CharField(_('fist name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, blank=False)    
    email = models.EmailField(_('email'), unique=True, default='')
    # we are using a phonenumberField   3rd party api
    contact_no = PhoneNumberField(unique=True, blank=True, null=True)
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    
    # next 3 fields will not be visable to user
    is_superadmin = models.BooleanField(_('is_superadmin'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=True)
    is_active = True


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    objects = CustomUserManager() # CustomUserManager for performing chainable QuerySets

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """stirng repr"""
        return self.email

        
    
        