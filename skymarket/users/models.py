from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.db import models
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField


class UserRoles:
    USER = "user"
    ADMIN = "admin"
    ROLE = [(USER, USER), (ADMIN, ADMIN)]


class User(AbstractBaseUser):

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "role"]

    first_name = models.CharField(
        validators=[MinLengthValidator(1)], max_length=64,
        verbose_name="Имя", help_text="Укажите имя (максимальная длина 64 символов)."
    )
    last_name = models.CharField(
        validators=[MinLengthValidator(1)], max_length=64,
        verbose_name="Фамилия", help_text="Укажите фамилию (максимальная длина 64 символов)."
    )
    phone = PhoneNumberField(
        max_length=15,
        verbose_name="Номер телефона", help_text="Укажите номер телефона для связи."
    )
    email = models.EmailField(
        max_length=25, unique=True,
        verbose_name="Адрес электронной почты", help_text="Укажите адрес электронной почты."
    )
    role = models.CharField(
        max_length=5, choices=UserRoles.ROLE, default=UserRoles.USER,
        verbose_name="Роль пользователя", help_text="Выберите роль пользователя."
    )
    image = models.ImageField(
        upload_to="photos/", null=True, blank=True,
        verbose_name="Аватарка пользователя", help_text="Загрузите аватарку."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен ли пользователь", help_text="Укажите активен ли пользователь."
    )

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

    def __str__(self):
        return self.email
