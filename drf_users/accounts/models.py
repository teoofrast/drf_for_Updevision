import re

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from .managers import UserManager


def validate_id(id_value):
    """Проверяет, является ли ID email или номером телефона."""
    if not re.match(r"[^@]+@[^@]+\.[^@]+", id_value) and not re.match(r'^\+?[1-9][0-9]{7,14}$', id_value):
        raise ValidationError("ID должен быть email или номером телефона.")


class CustomUser(AbstractUser):
    username = None
    id = models.CharField(max_length=150, unique=True, primary_key=True, validators=[validate_id])

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def access_token(self) -> str:
        """
        Позволяет получить токен доступа из экземпляра модели User.
        :return: str
        """
        return str(RefreshToken.for_user(self).access_token)

    @property
    def refresh_token(self) -> str:
        """
        Позволяет получить рефереш токен из экземпляра модели User.
        :return: str
        """
        return str(RefreshToken.for_user(self))

    @property
    def id_type(self):

        if re.match(r'[^@]+@[^@]+\.[^@]+' ,self.id):
            return "email"
        elif re.match(r'^\+?[1-9][0-9]{7,14}$',self.id):
            return "phone"

    def __str__(self):
        return self.id
