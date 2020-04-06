"""Zoom.us REST API Python Client -- Contacts component"""

from zoomapi import util
from zoomapi.util import Throttled
from zoomapi.components import base


class ContactsComponentV2(base.BaseComponent):
    """Component dealing with all contacts related matters"""

    @Throttled
    def list(self, **kwargs):
        util.require_keys(kwargs, "type")

        return self.get_request("/chat/users/me/contacts", params=kwargs)

    @Throttled
    def list_external(self):
        return self.get_request("/chat/users/me/contacts", params={"type": "external"})
