import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient  # must be placed after the code above
# or ModuleNotFoundError: No module named 'zoomapi'

import json
from configparser import ConfigParser
from pyngrok import ngrok

parser = ConfigParser()
parser.read("bots/bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
port = parser.getint("OAuth", "port", fallback=4001)
browser_path = parser.get("OAuth", "browser_path")
print(f'id: {client_id}\nbrowser: {browser_path}')

redirect_url = ngrok.connect(port, "http")
print(f"redirect_url: {redirect_url}")

client = OAuthZoomClient(client_id, client_secret, port, redirect_url,
                         browser_path)

user_content = json.loads(client.user.get(id='me').content)
print(f"user_content: {user_content}")

meeting_content = json.loads(client.meeting.list(user_id="me").content)
print(f'meeting_content: {meeting_content}')

chat_channels_content = json.loads(client.chat_channels.list().content)
print(f"chat_channels_content: {chat_channels_content}")

# must have at least one channel in advance
# go and create a channel named "test" in Zoom client
channels = chat_channels_content["channels"]
print(f"channels: {channels}")

for channel in channels:
    print(channel)
    if "test" in channel.values():
        print("Found channel test", channel["id"])
        cid = to_channel = channel["id"]

while True:
    message = input("Enter message: ")
    if message == "stop":
        break
    response = client.chat_messages.post(to_channel=cid, message=message)
    print(response)
