import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """
    Contains user authentication data and permissions to do with system access
    """

    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    # photo = models.ImageField()
    joined_date = models.DateTimeField(_("joined date"), auto_now_add=True)
    is_active = models.BooleanField(_("active status"), default=True)

    from user_manager.managers import UserManager

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def is_staff(self):
        """
        Whether or not the user has access to django admin
        """
        return self.is_superuser

    def get_profile(self):
        try:
            if self.profile:
                return self.profile
        except:
            return None

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Contains additional information about the user
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)

    def get_name(self):
        """
        Returns the first_name joined to the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return str(self.get_name())
