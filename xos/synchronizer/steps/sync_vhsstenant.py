import os
import sys
from django.db.models import Q, F
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible
from synchronizers.new_base.modelaccessor import *

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

class SyncVHSSTenant(SyncInstanceUsingAnsible):

    provides = [VHSSTenant]

    observes = VHSSTenant

    requested_interval = 0

    template_name = "vhsstenant_playbook.yaml"

    service_key_name = "/opt/xos/configurations/mcord/mcord_private_key"

    #Gets the attributes that are used by the Ansible template but are not
    #part of the set of default attributes.

    def __init__(self, *args, **kwargs):
        super(SyncVHSSTenant, self).__init__(*args, **kwargs)

    def fetch_pending(self, deleted):

        if (not deleted):
            objs = VHSSTenant.get_tenant_objects().filter(
                Q(enacted__lt=F('updated')) | Q(enacted=None), Q(lazy_blocked=False))
        else:

            objs = VHSSTenant.get_deleted_tenant_objects()

        return objs

    def get_extra_attributes(self, o):
        fields = {}
        fields['tenant_message'] = o.tenant_message
        return fields

    def delete_record(self, port):
        pass
