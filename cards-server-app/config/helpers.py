from django.shortcuts import resolve_url
from django.utils.safestring import SafeText
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.utils.html import format_html


def model_admin_url(obj, name: str = None) -> str:
    """
    Creates a URL to the model admin of a particular object

    via: https://stackoverflow.com/questions/6418592/django-admin-linking-to-related-objects
    """
    url = resolve_url(admin_urlname(obj._meta, SafeText("change")), obj.pk)
    return format_html('<a href="{}">{}</a>', url, name or str(obj))

