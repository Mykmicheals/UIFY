from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from authemail.models import EmailUserManager, EmailAbstractUser


class User(EmailAbstractUser):
    phone_validator = RegexValidator(
        r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$", "The phone number provided is invalid")
    phone = models.CharField('phone', validators=[
                             phone_validator], max_length=15, unique=True)
    full_name = models.CharField('full_name', max_length=52, blank=True)

    objects = EmailUserManager()

    REQUIRED_FIELDS = ["phone", 'full_name']

    # def __str__(self):
    #     return self.email
