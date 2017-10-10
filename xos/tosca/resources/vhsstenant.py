# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xosresource import XOSResource
from core.models import ServiceInstance, Service
from services.vhss.models import VHSSTenant

class XOSVHSSTenant(XOSResource):
    provides = "tosca.nodes.VHSSTenant"
    xos_model = VHSSTenant
    name_field = None
    copyin_props = ()

    def get_xos_args(self, throw_exception=True):
        args = super(XOSVHSSTenant, self).get_xos_args()

        provider_name = self.get_requirement("tosca.relationships.TenantOfService", throw_exception=throw_exception)
        if provider_name:
            args["owner"] = self.get_xos_object(Service, throw_exception=throw_exception, name=provider_name)

        return args

    def get_existing_objs(self):
        args = self.get_xos_args(throw_exception=False)
        owner = args.get("provider", None)
        if owner:
            return [ self.get_xos_object(owner=owner) ]
        return []

    def postprocess(self, obj):
        pass

    def can_delete(self, obj):
        return super(XOSVHSSTenant, self).can_delete(obj)

