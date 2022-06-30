from django.conf import settings
from django.db import models


class Ad(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название товара", help_text="Введите название товара."
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена товара", help_text="Введите цену товара."
    )
    description = models.CharField(
        max_length=1000, null=True, blank=True,
        verbose_name="Описание товара", help_text="Введите описание товара."
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="ads", on_delete=models.CASCADE,
        verbose_name="Автор объявления", help_text="Введите автора объявления."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания объявления"
    )
    image = models.ImageField(
        upload_to="images/", null=True, blank=True,
        verbose_name="Картинка", help_text="Загрузите картинку для объявления."
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(
        max_length=1000,
        verbose_name="Комментарий", help_text="Введите комментарий."
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE,
        verbose_name="Автор комментария", help_text="Введите автора комментария."
    )
    ad = models.ForeignKey(
        Ad, related_name="comments", on_delete=models.CASCADE,
        verbose_name="Объявление", help_text="Объявление комментария."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания комментария"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        return self.text
