from core.models.plcorebase import *
from models_decl import VHSSService_decl
from models_decl import VHSSTenant_decl

class VHSSService(VHSSService_decl):
   class Meta:
        proxy = True 

class VHSSTenant(VHSSTenant_decl):
   class Meta:
        proxy = True 

   def __init__(self, *args, **kwargs):
       vhssservice = VHSSService.get_service_objects().all()
       if vhssservice:
           self._meta.get_field(
                   "provider_service").default = vhssservice[0].id
       super(VHSSTenant, self).__init__(*args, **kwargs)

   def save(self, *args, **kwargs):
       super(VHSSTenant, self).save(*args, **kwargs)
       # This call needs to happen so that an instance is created for this
       # tenant is created in the slice. One instance is created per tenant.
       model_policy_vhsstenant(self.pk)

   def delete(self, *args, **kwargs):
       # Delete the instance that was created for this tenant
       self.cleanup_container()
       super(VHSSTenant, self).delete(*args, **kwargs)

def model_policy_vhsstenant(pk):
    # This section of code is atomic to prevent race conditions
    with transaction.atomic():
        # We find all of the tenants that are waiting to update
        tenant = VHSSTenant.objects.select_for_update().filter(pk=pk)
        if not tenant:
            return
        # Since this code is atomic it is safe to always use the first tenant
        tenant = tenant[0]
        tenant.manage_container()
