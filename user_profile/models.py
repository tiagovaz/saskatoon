from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from main.models import Person

class AuthUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(username=username, email=self.normalize_email(email),
                          )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AuthUser(AbstractBaseUser, PermissionsMixin):
    person = models.OneToOneField(Person,null=True)

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')

    ### Redefine the basic fields that would normally be defined in User ###
    email = models.EmailField(verbose_name='email address', unique=True, max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    ### Our own fields ###


    objects = AuthUserManager()
    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email
