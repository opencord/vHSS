import os
import sys
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible
from synchronizers.new_base.modelaccessor import *
from xos.logger import Logger, logging

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

logger = Logger(level=logging.INFO)

class SyncVHSSTenant(SyncInstanceUsingAnsible):

    provides = [VHSSTenant]

    observes = VHSSTenant

    requested_interval = 0

    template_name = "sync_vhss.yaml"

    service_key_name = "/opt/xos/synchronizers/mcord/mcord_private_key"

    watches = [ModelLink(ServiceDependency,via='servicedependency'), ModelLink(ServiceMonitoringAgentInfo,via='monitoringagentinfo')]

    def __init__(self, *args, **kwargs):
        super(SyncVHSSTenant, self).__init__(*args, **kwargs)

    def get_vhss(self, o):
        if not o.provider_service:
            return None

        vhss = VHSSService.objects.filter(id=o.provider_service.id)

        if not vhss:
            return None

        return vhss[0]

    # Gets the attributes that are used by the Ansible template but are not
    # part of the set of default attributes.
    def get_extra_attributes(self, o):
        fields = {}
        fields['tenant_message'] = o.tenant_message
        vhss = self.get_vhss(o)
        fields['service_message'] = vhss.service_message
        return fields

    def delete_record(self, port):
        # Nothing needs to be done to delete an exampleservice; it goes away
        # when the instance holding the exampleservice is deleted.
        pass

    def handle_service_monitoringagentinfo_watch_notification(self, monitoring_agent_info):
        if not monitoring_agent_info.service:
            logger.info("handle watch notifications for service monitoring agent info...ignoring because service attribute in monitoring agent info:%s is null" % (monitoring_agent_info))
            return

        if not monitoring_agent_info.target_uri:
            logger.info("handle watch notifications for service monitoring agent info...ignoring because target_uri attribute in monitoring agent info:%s is null" % (monitoring_agent_info))
            return

        objs = VHSSTenant.objects.all()
        for obj in objs:
            if obj.provider_service.id != monitoring_agent_info.service.id:
                logger.info("handle watch notifications for service monitoring agent info...ignoring because service attribute in monitoring agent info:%s is not matching" % (monitoring_agent_info))
                return

            instance = self.get_instance(obj)
            if not instance:
               logger.warn("handle watch notifications for service monitoring agent info...: No valid instance found for object %s" % (str(obj)))
               return

            logger.info("handling watch notification for monitoring agent info:%s for ExampleTenant object:%s" % (monitoring_agent_info, obj))

            #Run ansible playbook to update the routing table entries in the instance
            fields = self.get_ansible_fields(instance)
            fields["ansible_tag"] =  obj.__class__.__name__ + "_" + str(obj.id) + "_monitoring"
            fields["target_uri"] = monitoring_agent_info.target_uri

            template_name = "monitoring_agent.yaml"
            super(SyncVHSSTenant, self).run_playbook(obj, fields, template_name)
        pass
