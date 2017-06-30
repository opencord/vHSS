# models.py -  VHSSService Models

from core.models import Service, TenantWithContainer, Image
from django.db import models, transaction

MCORD_KIND = "EPC"  # added from vBBU

# these macros are currently not used, names hard-coded manually
SERVICE_NAME = 'vhss'
SERVICE_NAME_VERBOSE = 'VHSS Service'
SERVICE_NAME_VERBOSE_PLURAL = 'VHSS Services'
TENANT_NAME_VERBOSE = 'VHSS Service Tenant'
TENANT_NAME_VERBOSE_PLURAL = 'VHSS Service Tenants'


class VHSSService(Service):
    KIND = MCORD_KIND

    class Meta:
        proxy = True
        app_label = "vhss"
        verbose_name = "VHSS Service"


class VHSSTenant(TenantWithContainer):
    KIND = 'vhss'

    class Meta:
        verbose_name = "VHSS Service Tenant"

    tenant_message = models.CharField(max_length=254, help_text="vHSS message")
    image_name = models.CharField(max_length=254, help_text="Name of VM image")

    def __init__(self, *args, **kwargs):
        vhss_services = VHSSService.get_service_objects().all()
        if vhss_services:
            self._meta.get_field('provider_service').default = vhss_services[0].id
        super(VHSSTenant, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(VHSSTenant, self).save(*args, **kwargs)
        model_policy_vhsstenant(self.pk)  # defined below

    def delete(self, *args, **kwargs):
        self.cleanup_container()
        super(VHSSTenant, self).delete(*args, **kwargs)

    @property
    def image(self):
        img = self.image_name.strip()
        if img.lower() != "default":
            return Image.objects.get(name=img)
        else:
            return super(VHSSTenant, self).image


def model_policy_vhsstenant(pk):
    with transaction.atomic():
        tenant = VHSSTenant.objects.select_for_update().filter(pk=pk)
        if not tenant:
            return
        tenant = tenant[0]
        tenant.manage_container()

