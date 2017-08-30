from xosresource import XOSResource
from core.models import Tenant, Service
from services.vhss.models import VHSSTenant

class XOSVHSSTenant(XOSResource):
    provides = "tosca.nodes.VHSSTenant"
    xos_model = VHSSTenant
    name_field = "service_specific_id"
    copyin_props = ()

    def get_xos_args(self, throw_exception=True):
        args = super(XOSVHSSTenant, self).get_xos_args()

        provider_name = self.get_requirement("tosca.relationships.TenantOfService", throw_exception=True)
        if provider_name:
            args["provider_service"] = self.get_xos_object(Service, throw_exception=True, name=provider_name)

        return args

    def get_existing_objs(self):
        args = self.get_xos_args(throw_exception=False)
        return VHSSTenant.get_tenant_objects().filter(provider_service=args["provider_service"], service_specific_id=args["service_specific_id"])
        return []

    def can_delete(self, obj):
        return super(XOSVHSSTenant, self).can_delete(obj)

