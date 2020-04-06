import sys, os

# add upper level folder to PATH so that zoomapi can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# must be placed after the code above
# or ModuleNotFoundError: No module named 'zoomapi'
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok
import time


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

    """
    chat massage functions
    """

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

    """
    chat channel functions
    """

    def list_channels(self):
        # must have at least one channel in advance
        # go and create a channel named "test" in Zoom client
        self.channels = json.loads(self.client.chat_channels.list().content)["channels"]

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

    """
    Function Menu
    """

    def run(self):
        command = -1

        while command != 0:
            self.print_main_menu()
            command = self.get_user_command()

            if command == 1:
                self.execute_set_of_chat_channel_functions()
            elif command == 2:
                self.execute_single_chat_channel_function()
            elif command == 3:
                self.execute_set_of_chat_message_functions()
            elif command == 4:
                self.execute_single_chat_message_function()
            else:
                break

    def print_main_menu(self):
        print("# Main Menu #")
        print("[1] Execute a set of Chat Channel Functions;")
        print("[2] Execute a single Chat Channel Function;")
        print("[3] Execute a set of Chat Message Functions;")
        print("[4] Execute a single Chat Message Function;")
        print("[0] Quit;")

    def get_user_command(self):
        try:
            command = int(input("Please select a command(ex. 1): "))
            return command
        except ValueError:
            print("Invalid command, please enter a correct command!")
            return -1

    def execute_set_of_chat_channel_functions(self):
        print("Execute a set of Chat Channel Functions\n")

    def execute_single_chat_channel_function(self):
        print("Execute a single Chat Channel Function\n")

    def execute_set_of_chat_message_functions(self):
        print("# Executing a set of Chat Message Functions...")

        # 0
        self.list_channels()
        try:
            i = int(input("First, please select a channel:\n"))
        except ValueError:
            print(f"{i} is not a number.")
            return
        self.channel = self.channels[i % len(self.channels)]
        print("You have selected channel", self.channel["name"])

        # 1
        input("# Part 1: Test sending messages (Press Enter to continue)")
        msg = input("Then, please send a message to the channel:\n")
        response = self.client.chat_messages.post(
            to_channel=self.channel["id"], message=msg
        )
        print("The response is", response)
        if response.status_code > 299:  # OK status codes start with 2
            print("Something goes wrong. Please retry.")
            return
        mid = response.json()["id"]

        # 2
        input("# Part 2: Test listing messages (Press Enter to continue)")
        print("Then please review the message history.")
        self.list_channel_messages()
        print(f'Did you see "{msg}" there? Great.')

        # 3
        input("# Part 3: Test updating messages (Press Enter to continue)")
        print(f'Then we are going to update "{msg}".')
        msg = input("Please input a new message:\n")
        response = self.client.chat_messages.update(
            message_id=mid, message=msg, to_channel=self.channel["id"],
        )
        print("The response is", response)
        if response.status_code > 299:  # OK status codes start with 2
            print("Something goes wrong. Please retry.")
            return
        time.sleep(1)
        self.list_channel_messages()
        print(f'Did you see "{msg}" there? Great.')

        # 4
        input("# Part 4: Test removing messages (Press Enter to continue)")
        print(f'Then we are going to delete "{msg}".')
        response = self.client.chat_messages.delete(
            message_id=mid, to_channel=self.channel["id"],
        )
        print("The response is", response)
        time.sleep(1)
        self.list_channel_messages()
        print(f'Did you see "{msg}" gone? Great.')

        print("# Execution finished.")

    def execute_single_chat_message_function(self):
        while True:
            self.list_channels()

            try:
                i = int(input("Please select a channel: "))
            except ValueError:
                break

            self.channel = self.channels[i]
            if self.channel["id"] != None:
                while True:
                    print("# Chat Message Menu #", self.channel["name"])
                    print("[1] Print message history;")
                    print("[2] Send messages;")
                    print("[3] Update a message;")
                    print("[4] Delete a message;")

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
                    else:
                        break


if __name__ == "__main__":
    Bot().run()
