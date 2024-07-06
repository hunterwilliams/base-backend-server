from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import SiteSettings


class SiteSettingsAdmin(admin.ModelAdmin):
    model = SiteSettings

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def changelist_view(self, request, extra_context=None):
        if self.model.objects.exists():
            instance = self.model.objects.first()
            url = reverse(
                "admin:%s_%s_change"
                % (self.model._meta.app_label, self.model._meta.model_name),
                args=(instance.pk,),
            )
            return HttpResponseRedirect(url)
        else:
            url = reverse(
                "admin:%s_%s_add"
                % (self.model._meta.app_label, self.model._meta.model_name)
            )
            return HttpResponseRedirect(url)


admin.site.register(SiteSettings, SiteSettingsAdmin)
