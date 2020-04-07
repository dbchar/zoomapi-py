# zoomapi for SWE262P

[https://github.com/double-charburger/zoomapi](https://github.com/double-charburger/zoomapi)

Python wrapper around the [Zoom.us](http://zoom.us) REST API v2.

This work is based on [crista/zoomapi](https://github.com/crista/zoomapi) and [Zoomus](https://github.com/actmd/zoomus).

## Basic Info

- Group: Double Char
- Members:
  - Wen-Chia Yang
  - Junxian Chen

## Compatibility

Note, as this library heavily depends on the [requests](https://pypi.org/project/requests/) library, official compatibility is limited to the official compatibility of `requests`.

## Example Usage

### Run the bot (Milestone 1)

First please nagivate to the root directory of the project, then run:

```bash
python3 bots/botm1.py
```

There are 4 options in the main menu which looks like this:

```txt
# Main Menu #
[1] Execute a MEANINGFUL set of Chat Channel Functions
[2] Execute a single Chat Channel Function (debug only)
[3] Execute a MEANINGFUL set of Chat Message Functions
[4] Execute a single Chat Message Function (debug only)
[0] Quit
```

**We recommend using option 1 and 3 to test all the functions that we have implemented. Option 1 and option 4 are for debugging purpose only so please advance with caution.**

After selecting option 1 or 3, please follow the instructions and the bot should work fine.

### Create the client

```python
import json
from zoomapi import OAuthZoomClient

client = OAuthZoomClient('CLIENT_ID', 'CLIENT_SECRET', 'REDIRECT_URL')

user_response = client.user.get(id='me')
user = json.loads(user_response.content)
print(user)
```

What one will note is that the returned object from a call using the client is a [requests](https://pypi.org/project/requests/) `Response` object. This is done so that if there is any error working with the API that one has complete control of handling all errors. As such, to actually get the list of users in the example above, one will have to load the JSON from the content of the `Response` object that is returned.

### Using with a manage context

```python
with JWTZoomClient('API_KEY', 'API_SECRET') as client:
    user_list_response = client.users.list()
    ...
```

## Available methods

### Contacts

- client.contacts.list(...)
- client.contacts.list_external(...)

### Chat Channels

- client.chat_channels.list(...)
- client.chat_channels.create(...)
- client.chat_channels.update(...)
- client.chat_channels.delete(...)
- client.chat_channels.get(...)
- client.chat_channels.list_members(...)
- client.chat_channels.invite_members(...)
- client.chat_channels.join(...)
- client.chat_channels.leave(...)
- client.chat_channels.remove_member(...)

### Chat Messages

- client.chat_messages.list(...)
- client.chat_messages.post(...)
- client.chat_messages.update(...)
- client.chat_messages.delete(...)

### User

- client.user.create(...)
- client.user.cust_create(...)
- client.user.update(...)\*
- client.user.list(...)
- client.user.pending(...)
- client.user.get(...)
- client.user.get_by_email(...)

### Metting

- client.meeting.get(...)
- client.meeting.end(...)
- client.meeting.create(...)
- client.meeting.delete(...)
- client.meeting.list(...)
- client.meeting.update(...)

### Report

- client.report.get_account_report(...)
- client.report.get_user_report(...)

### Webinar

- client.webinar.create(...)
- client.webinar.update(...)
- client.webinar.delete(...)
- client.webinar.list(...)
- client.webinar.get(...)
- client.webinar.end(...)
- client.webinar.register(...)
