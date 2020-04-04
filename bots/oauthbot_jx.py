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
    user_id = user_content["id"]
    user_email = user_content["email"]

    print("# User info")
    print("user_id =", user_id)
    print("user_email =", user_email)
    # print(f"user_content: {user_content}")

    # meeting_content = json.loads(client.meeting.list(user_id="me").content)
    # print(f"meeting_content: {meeting_content}")

    chat_channels_content = json.loads(client.chat_channels.list().content)
    # print(f"chat_channels_content: {chat_channels_content}")

    # must have at least one channel in advance
    # go and create a channel named "test" in Zoom client
    channels = chat_channels_content["channels"]

    while True:
        i = 0
        print("# Channel info of user", user_email)
        for channel in channels:
            print(f"[{i}] channel: {channel['id']} {channel['name']}")
            i += 1

        try:
            i = int(input("Please select a channel: "))
        except ValueError:
            break

        channel_id_selected = channels[i]["id"]
        channel_name_selected = channels[i]["name"]

        if channel_id_selected != None:
            while True:
                print("# You have entered the channel", channel_name_selected)
                print("[1] Print history;")
                print("[2] Send messages;")

                try:
                    j = int(input("Please select a function: "))
                except ValueError:
                    break

                if j == 1:
                    try:
                        test_channel_messages_content = json.loads(
                            client.chat_messages.list(
                                user_id=user_id, to_channel=channel_id_selected
                            ).content
                        )
                        print("# History of the channel", channel_name_selected)
                        for msg in test_channel_messages_content["messages"]:
                            print(
                                f"[{msg['date_time']}] {msg['sender']}: {msg['message']}"
                            )
                    except:
                        print(test_channel_messages_content)
                elif j == 2:
                    while True:
                        message = input("Enter message ('q' to stop): ")
                        if message == "q":
                            break
                        response = client.chat_messages.post(
                            to_channel=channel_id_selected, message=message
                        )
                        print(response)
                else:
                    break
