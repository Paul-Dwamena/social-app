from django.db import models
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user realization based on Django AbstractUser and PermissionMixin.
    """


    PUBLIC = "public"
    PRIVATE = "private"

    ACCOUNTTYPE_CHOICES = (
        (PUBLIC, "public"),
        (PRIVATE, "private")
        
    )

    email = models.EmailField(
        ('email address'),
        unique=True,
        blank=True,
        error_messages={
            'unique': ("A user with that email already exists."),
        })
    username = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin '
                   'site.'))
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=('Designates whether this user should be treated as '
                   'active. Unselect this instead of deleting accounts.'))

    password = models.TextField(null=True, blank=True)
    is_firsttime = models.BooleanField(default=True)
    emailverified = models.BooleanField(default=False)
    profile_url=models.TextField(null=True,blank=True)
    following_count = models.IntegerField(default=0, blank=True, null=True)
    follower_count = models.IntegerField(default=0, blank=True, null=True)
    datecreated = models.DateTimeField(auto_now_add=True)

    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNTTYPE_CHOICES,
        default=PUBLIC,
    )
  
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        managed = True
        abstract = False
        db_table = 'auth_user'

    def _str_(self):
        return self.email

