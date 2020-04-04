import sys, os

# add upper level folder to PATH so that zoomapi can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# must be placed after the code above
# or ModuleNotFoundError: No module named 'zoomapi'
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok


if __name__ == "__main__":
    parser = ConfigParser()
    parser.read("bots/bot.ini")
    client_id = parser.get("OAuth", "client_id")
    client_secret = parser.get("OAuth", "client_secret")
    port = parser.getint("OAuth", "port", fallback=4001)
    browser_path = parser.get("OAuth", "browser_path")
    redirect_url = ngrok.connect(port, "http")
    client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)

    user_content = json.loads(client.user.get(id="me").content)
    print(f"user_content: {user_content}")

    user_id = user_content["id"]
    print(user_id)

    # meeting_content = json.loads(client.meeting.list(user_id="me").content)
    # print(f"meeting_content: {meeting_content}")

    chat_channels_content = json.loads(client.chat_channels.list().content)
    print(f"chat_channels_content: {chat_channels_content}")

    # must have at least one channel in advance
    # go and create a channel named "test" in Zoom client
    channels = chat_channels_content["channels"]

    for channel in channels:
        print(channel)
        if "test" in channel.values():
            test_channel_id = to_channel = channel["id"]
            print("Found channel test", test_channel_id)

    test_channel_messages_content = json.loads(
        client.chat_messages.list(user_id=user_id, to_channel=test_channel_id).content
    )
    print(test_channel_messages_content)

    while True:
        message = input("Enter message ('q' to stop): ")
        if message == "q":
            break
        response = client.chat_messages.post(to_channel, message)
        print(response)
