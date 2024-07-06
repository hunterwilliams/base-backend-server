from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError("There can only be one instance of a SingletonModel.")
        return super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        instance = cls.objects.first()
        if instance:
            return instance
        else:
            instance = cls.objects.create()
            return instance


class SiteSettings(SingletonModel):
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return "Site Settings"
