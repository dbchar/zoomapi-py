import sys, os

# add upper level folder to PATH so that zoomapi can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# must be placed after the code above
# or ModuleNotFoundError: No module named 'zoomapi'
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok


class Bot:
    def __init__(self):
        parser = ConfigParser()
        parser.read("bots/bot.ini")

        client_id = parser.get("OAuth", "client_id")
        client_secret = parser.get("OAuth", "client_secret")
        port = parser.getint("OAuth", "port", fallback=4001)
        browser_path = parser.get("OAuth", "browser_path")
        redirect_url = ngrok.connect(port, "http")

        self.client = OAuthZoomClient(
            client_id, client_secret, port, redirect_url, browser_path,
        )
        self.user = json.loads(self.client.user.get(id="me").content)
        print("# User info")
        print("user_id =", self.user["id"])
        print("user_email =", self.user["email"])

    def list_channel_messages(self):
        try:
            test_channel_messages_content = json.loads(
                self.client.chat_messages.list(
                    user_id=self.user["id"], to_channel=self.channel["id"]
                ).content
            )
            print("# History of the channel", self.channel["name"])
            for msg in test_channel_messages_content["messages"]:
                print(
                    f"[{msg['date_time']}] {msg['sender']}: {msg['message']} id={msg['id']}"
                )
        except:
            print(test_channel_messages_content)
        finally:
            # self.client.refresh_token()
            pass

    def send_channel_messages(self):
        while True:
            message = input("Enter message ('q' to stop): ")
            if message == "q":
                break
            response = self.client.chat_messages.post(
                to_channel=self.channel["id"], message=message
            )
            print(response)

    def update_a_channel_message(self):
        self.list_channel_messages()
        message_id = input("Enter message id: ")
        message_new = input("Enter new message content: ")
        response = self.client.chat_messages.update(
            message_id=message_id, message=message_new, to_channel=self.channel["id"],
        )
        print(response)

    def delete_a_channel_message(self):
        self.list_channel_messages()
        message_id = input("Enter message id: ")
        response = self.client.chat_messages.delete(
            message_id=message_id, to_channel=self.channel["id"],
        )
        print(response)

    def list_channels(self):
        i = 0
        print("# Channel info of user", self.user["email"])
        for channel in self.channels:
            print(f"[{i}] channel: {channel['id']} {channel['name']}")
            i += 1

    def list_external_contacts(self):
        res = self.client.get_request(
            "/chat/users/me/contacts", params={"type": "external"}
        )
        contacts = json.loads(res.content)["contacts"]
        print("# User's external contacts")
        for contact in contacts:
            print(f"{contact['id']} {contact['email']}")

    def invite_channel_members(self):
        self.list_external_contacts()
        email = input("Please input a user email: ")
        res = self.client.chat_channels.invite_members(
            channel_id=self.channel["id"], members=[{"email": email}]
        )
        print(res)
        print(res.json())

    def run(self):
        # must have at least one channel in advance
        # go and create a channel named "test" in Zoom client
        self.channels = json.loads(self.client.chat_channels.list().content)["channels"]

        while True:
            self.list_channels()

            try:
                i = int(input("Please select a channel: "))
            except ValueError:
                break

            self.channel = self.channels[i]
            if self.channel["id"] != None:
                while True:
                    print("# You have entered the channel", self.channel["name"])
                    print("[1] Print history;")
                    print("[2] Send messages;")
                    print("[3] Update a message;")
                    print("[4] Delete a message;")
                    print("[5] Invite a member;")

                    try:
                        j = int(input("Please select a function: "))
                    except ValueError:
                        break

                    if j == 1:
                        self.list_channel_messages()
                    elif j == 2:
                        self.send_channel_messages()
                    elif j == 3:
                        self.update_a_channel_message()
                    elif j == 4:
                        self.delete_a_channel_message()
                    elif j == 5:
                        self.invite_channel_members()
                    else:
                        break


if __name__ == "__main__":
    Bot().run()
