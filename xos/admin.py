# admin.py - VHSSService Django Admin

from core.admin import ReadOnlyAwareAdmin, SliceInline
from core.middleware import get_request
from core.models import User

from django import forms
from django.contrib import admin

from services.vhss.models import *

class VHSSServiceForm(forms.ModelForm):

    class Meta:
        model = VHSSService
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VHSSServiceForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['service_message'].initial = self.instance.service_message

    def save(self, commit=True):
        self.instance.service_message = self.cleaned_data.get('service_message')
        return super(VHSSServiceForm, self).save(commit=commit)

class VHSSServiceAdmin(ReadOnlyAwareAdmin):

    model = VHSSService
    verbose_name = "vHSS Service"
    verbose_name_plural = "vHSS Services"
    inlines = [SliceInline]

    list_display = ('backend_status_icon', 'name', 'service_message', 'enabled')
    list_display_links = ('backend_status_icon', 'name', 'service_message' )

    fieldsets = [(None, {
        'fields': ['backend_status_text', 'name', 'enabled', 'versionNumber', 'service_message', 'description',],
        'classes':['suit-tab suit-tab-general',],
        })]

    readonly_fields = ('backend_status_text', )
    user_readonly_fields = ['name', 'enabled', 'versionNumber', 'description',]

    extracontext_registered_admins = True

    suit_form_tabs = (
        ('general', 'vHSS Service Details', ),
        ('slices', 'Slices',),
        )

    suit_form_includes = ((
        'top',
        'administration'),
        )

    def get_queryset(self, request):
        return VHSSService.get_service_objects_by_user(request.user)

admin.site.register(VHSSService, VHSSServiceAdmin)

class VHSSTenantForm(forms.ModelForm):

    class Meta:
        model = VHSSTenant
        fields = '__all__'

    creator = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super(VHSSTenantForm, self).__init__(*args, **kwargs)

        self.fields['kind'].widget.attrs['readonly'] = True
        self.fields['kind'].initial = "vhss"

        self.fields['provider_service'].queryset = VHSSService.get_service_objects().all()

        if self.instance:
            self.fields['creator'].initial = self.instance.creator
            self.fields['tenant_message'].initial = self.instance.tenant_message

        if (not self.instance) or (not self.instance.pk):
            self.fields['creator'].initial = get_request().user
            if VHSSService.get_service_objects().exists():
                self.fields['provider_service'].initial = VHSSService.get_service_objects().all()[0]

    def save(self, commit=True):
        self.instance.creator = self.cleaned_data.get('creator')
        self.instance.tenant_message = self.cleaned_data.get('tenant_message')
        return super(VHSSTenantForm, self).save(commit=commit)


class VHSSTenantAdmin(ReadOnlyAwareAdmin):

    verbose_name = "vHSS Service Tenant"
    verbose_name_plural = "vHSS Service Tenants"

    list_display = ('id', 'backend_status_icon', 'instance', 'tenant_message')
    list_display_links = ('backend_status_icon', 'instance', 'tenant_message', 'id')

    fieldsets = [(None, {
        'fields': ['backend_status_text', 'kind', 'provider_service', 'instance', 'creator', 'tenant_message'],
        'classes': ['suit-tab suit-tab-general'],
        })]

    readonly_fields = ('backend_status_text', 'instance',)


    suit_form_tabs = (('general', 'Details'),)

    def get_queryset(self, request):
        return VHSSTenant.get_tenant_objects_by_user(request.user)

admin.site.register(VHSSTenant, VHSSTenantAdmin)

