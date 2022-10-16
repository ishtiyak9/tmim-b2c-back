import os
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from user.config import GenderType, UserType, LanguageType


class Country(models.Model):
    name = models.CharField(max_length=100, blank=True)
    iso3 = models.CharField(max_length=3, blank=True)
    iso2 = models.CharField(max_length=2, blank=True)
    phone_code = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        db_table = 'country'
        verbose_name_plural = 'Countries'


class City(models.Model):
    name = models.CharField(max_length=100, blank=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        db_table = 'city'
        verbose_name_plural = 'Cities'


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # if not username:
        #     raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, blank=True, null=True, unique=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    about_me = models.CharField(max_length=200, blank=True, null=True)
    self_name = models.CharField(max_length=200, blank=True, null=True)
    partner_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GenderType.CHOICES, blank=True)
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/users/images/', blank=True)
    cover_photo = models.ImageField(blank=True, null=True)
    user_type = models.CharField(max_length=10, blank=True, choices=UserType.CHOICES)
    language = models.CharField(max_length=2, choices=LanguageType.CHOICES, default=LanguageType.EN)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)
    area = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_approved = models.BooleanField(_('verified'), default=False,
                                      help_text=_('Designates whether this user is verified'))
    is_subscribed = models.BooleanField(_('subscribed'), default=False,
                                        help_text=_('Designates whether this user\'s store is subscribed'))
    is_deleted = models.BooleanField(_('Archived'), default=False,
                                     help_text=_('Designates whether this user is archived'))

    date_joined = models.DateTimeField(_('date joined'), blank=True, null=True)

    wedding_date = models.DateField(blank=True, null=True)
    planning_type = models.ForeignKey('guest.OccasionType', related_name="planning_type", on_delete=models.CASCADE,
                                      blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = 'Users'

    # def delete(self, *args, **kwargs):
    #     if os.path.isfile(self.image.path):
    #         os.remove(self.image.path)

    #     super(User, self).delete(*args, **kwargs)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('api:password_reset:reset-password-confirm'),
                                                   reset_password_token.key)

    send_mail(
        "Password Reset for {title}".format(title="Tmmim"),
        email_plaintext_message,
        "haris.dipto@gmail.com",
        [reset_password_token.user.email]
    )
