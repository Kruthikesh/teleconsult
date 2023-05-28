from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from apps.commons.models import BaseClass


class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=email)
        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin, BaseClass):
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(help_text='If the user an application admin', default=False)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    ALREADY_EXISTS = 'The user already exists'

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, *args, **kwargs):
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def to_dict(self):
        return {
            'email': self.email,
            'is_email_verified': self.is_email_verified,
            'is_active': self.is_active,
        }

    class Meta(BaseClass.Meta):
        db_table = 'da_base_user'
