from service import XOSService
from services.vhss.models import VHSSService

class XOSVHSSService(XOSService):
    provides = "tosca.nodes.VHSSService"
    xos_model = VHSSService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key", "private_key_fn", "versionNumber"]
