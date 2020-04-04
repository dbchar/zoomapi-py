"""Zoom.us REST API Python Client -- Chat Messages component"""

from zoomapi import util
from zoomapi.components import base
import requests


class ChatMessagesComponentV2(base.BaseComponent):
    """Component dealing with all chat messages related matters"""

    def list(self, **kwargs) -> requests.Response:
        """
        https://marketplace.zoom.us/docs/api-reference/zoom-api/chat-messages/getchatmessages#request-parameters

        Use params=kwargs

        Examples:

        https://api.zoom.us/v2/chat/users/{user_id}/messages?to_channel={some_channel_id}

        https://api.zoom.us/v2/chat/users/{user_id}/messages?to_contact={some_contact_id}
        """
        util.require_keys(kwargs, "user_id")
        return self.get_request(
            "/chat/users/{}/messages".format(kwargs.get("user_id")), params=kwargs
        )

    def post(self, **kwargs) -> requests.Response:
        """
        https://marketplace.zoom.us/docs/api-reference/zoom-api/chat-messages/sendachatmessage#request-body

        Use data=kwargs

        Examples:

        https://api.zoom.us/v2/chat/users/me/messages

        body: {
            "message": {some_message},
            "to_channel": {some_channel_id}
        }

        body: {
            "message": {some_message},
            "to_contact": {some_contact_id}
        }
        """
        util.require_keys(kwargs, "message")
        return self.post_request("/chat/users/me/messages", data=kwargs)

    def update(self, **kwargs) -> requests.Response:
        """
        https://marketplace.zoom.us/docs/api-reference/zoom-api/chat-messages/editmessage#request-body

        Use data=kwargs
        """
        util.require_keys(kwargs, "message_id")
        return self.put_request(
            "/chat/users/me/messages/{}".format(kwargs.get("message_id")), data=kwargs
        )

    def delete(self, **kwargs) -> requests.Response:
        """
        https://marketplace.zoom.us/docs/api-reference/zoom-api/chat-messages/deletechatmessage#request-parameters

        Use params=kwargs
        """
        util.require_keys(kwargs, "message_id")
        return self.delete_request(
            "/chat/users/me/messages/{}".format(kwargs.get("message_id")), params=kwargs
        )
