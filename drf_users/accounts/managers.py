from typing import Any, Type, Union
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    """
    Менеджер для переопределенной модели юзера.
    """

    use_in_migrations = True

    def create_user(self, id: str, password: str, **kwargs: Union[str, Any]) -> Type[BaseUserManager]:

        """
        Метод менеджера для создания обычного пользователя.
        """

        if not id:
            raise ValueError("Please, input id")

        id = self.normalize_email(id)
        user = self.model(id=id, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, id: str, password: str, **params: Union[str, Any]) -> Type[BaseUserManager]:

        """
        Метод менеджера для создания суперюзера.
        """

        params.setdefault("is_staff", True)
        params.setdefault("is_superuser", True)
        params.setdefault("is_active", True)

        if params.get("is_staff") is not True:
            raise ValueError("superuser must have a is_staff=True")
        if params.get("is_superuser") is not True:
            raise ValueError("superuser must have a is_superuser=True")

        return self.create_user(id, password, **params)