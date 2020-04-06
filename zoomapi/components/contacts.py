"""Zoom.us REST API Python Client -- Contacts component"""

from zoomapi import util
from zoomapi.components import base


class ContactsComponentV2(base.BaseComponent):
    """Component dealing with all contacts related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, "type")

        return self.get_request("/chat/users/me/contacts", params=kwargs)

    def list_external(self):
        return self.get_request("/chat/users/me/contacts", params={"type": "external"})
