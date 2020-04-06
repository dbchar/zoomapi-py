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
    """A bot for executing chat channel and chat message function"""

    def __init__(self):
        (
            client_id,
            client_secret,
            port,
            browser_path,
            redirect_url,
        ) = self.load_bot_settings()
        self.client = OAuthZoomClient(
            client_id, client_secret, port, redirect_url, browser_path,
        )

    """Utility functions"""

    def load_bot_settings(self):
        parser = ConfigParser()
        parser.read("bots/bot.ini")

        client_id = parser.get("OAuth", "client_id")
        client_secret = parser.get("OAuth", "client_secret")
        port = parser.getint("OAuth", "port", fallback=4001)
        browser_path = parser.get("OAuth", "browser_path")
        redirect_url = ngrok.connect(port, "http")
        return client_id, client_secret, port, browser_path, redirect_url

    def get_user_command(self):
        try:
            command = int(input("Please select a command(ex. 1): "))
            return command
        except ValueError:
            print("Invalid command, please enter a correct command!")
            return -1

    def get_user_input(self, placeholder):
        user_input = None
        while user_input is None:
            user_input = input(placeholder)
        return user_input

    def is_valid_response(self, response):
        if response.status_code > 299:
            print("Something goes wrong. Please retry.")
            return False
        return True

    """Log"""

    def print_title(self, title):
        print("------------------------------")
        print("# " + title)
        print("------------------------------")

    def print_channel_with_title(self, title, json_data):
        print("------------------------------")
        print("# " + title)
        print(f"{json_data['name']}: {json_data['id']}")
        print("------------------------------")

    def print_channels_with_title(self, title, json_array):
        print("------------------------------")
        print("# " + title)
        i = 0
        for channel in json_array["channels"]:
            print(f"[{i}] {channel['name']}: {channel['id']}")
            i += 1
        print("------------------------------")

    def print_members_with_title(self, title, json_array):
        print("------------------------------")
        print("# " + title)
        i = 0
        for member in json_array["members"]:
            print(f"[{i}] {member['name']}({member['role']}): {member['email']}")
            i += 1
        print("------------------------------")

    def print_invite_channel_memners_result_with_title(self, title, json_data):
        added_at = json_data["added_at"]
        ids = json_data["ids"]
        print("------------------------------")
        print("# " + title + " at " + added_at)
        print("Ids: " + ids)
        print("------------------------------")

    def print_join_a_channel_result_with_title(self, title, json_data):
        added_at = json_data["added_at"]
        id = json_data["id"]
        print("------------------------------")
        print("# " + title + " at " + added_at)
        print("Id: " + id)
        print("------------------------------")

    """Menu"""

    def print_main_menu(self):
        print("# Main Menu #")
        print("[1] Execute a set of Chat Channel Functions;")
        print("[2] Execute a single Chat Channel Function;")
        print("[3] Execute a set of Chat Message Functions;")
        print("[4] Execute a single Chat Message Function;")
        print("[0] Quit;")

    def print_chat_channel_menu(self):
        print("# Chat Channel Menu #", self.user["email"])
        print("[1] List user's channels;")
        print("[2] Create a channel;")
        print("[3] Get a channel;")
        print("[4] Update a channel;")
        print("[5] Delete a channel;")
        print("[6] List channel members;")
        print("[7] Invite channel members;")
        print("[8] Join a channel;")
        print("[9] Leave a channel;")
        print("[10] Remove a member;")
        print("[0] Quit;")

    def print_chat_message_menu(self):
        print("# Chat Message Menu #", self.channel["name"])
        print("[1] List channel messages;")
        print("[2] Send channel messages;")
        print("[3] Update a message;")
        print("[4] Delete a message;")
        print("[0] Quit;")

    """Bot implementations"""

    def run(self):
        print("------------------------------")
        print("# You are logged in as")
        self.print_user_info()
        print("------------------------------")

        command = -1

        while command != 0:
            self.print_main_menu()
            command = self.get_user_command()
            print("")

            if command == 1:
                self.execute_set_of_chat_channel_functions()
            elif command == 2:
                self.execute_single_chat_channel_function()
            elif command == 3:
                self.execute_set_of_chat_message_functions()
            elif command == 4:
                self.execute_single_chat_message_function()
            else:
                pass

    def execute_set_of_chat_channel_functions(self):
        print("# Executing a set of Chat Channel Functions...")

        # 1
        input("# Part 1: Test listing channels (Press Enter to continue)")
        self.list_channels()

        # 2
        input("# Part 2: Test creating a channel (Press Enter to continue)")
        self.create_a_channel()

        # 3
        input("# Part 3: Test getting a channel (Press Enter to continue)")
        self.get_a_channel()
        self.list_channels()

        # 4
        input("# Part 4: Test updating a channel (Press Enter to continue)")
        self.update_a_channel()
        self.list_channels()

        # 5
        input("# Part 5: Test listing members of a channel (Press Enter to continue)")
        self.list_channel_members()

        # 6
        input("# Part 6: Test inviting a member to a channel (Press Enter to continue)")
        self.invite_channel_members()
        self.list_channel_members()

        # 7
        input(
            "# Part 7: Test removing a member from a channel (Press Enter to continue)"
        )
        self.remove_a_channel_member()
        self.list_channel_members()

        # 8
        input("# Part 8: Test deleting a channel (Press Enter to continue)")
        self.list_channels()
        self.delete_a_channel()
        self.list_channels()

        # 9
        input("# Part 9: Test joining a channel (Press Enter to continue)")
        self.join_a_channel()
        self.list_channels()

        # 10
        input("# Part 10: Test leaving a channel (Press Enter to continue)")
        self.leave_a_channel()
        self.list_channels()

    def execute_single_chat_channel_function(self):
        command = -1

        while command != 0:
            self.print_chat_channel_menu()
            command = self.get_user_command()
            print("")

            if command == 1:
                self.list_channels()
            elif command == 2:
                self.create_a_channel()
            elif command == 3:
                self.get_a_channel()
            elif command == 4:
                self.update_a_channel()
            elif command == 5:
                self.delete_a_channel()
            elif command == 6:
                self.list_channel_members()
            elif command == 7:
                self.invite_channel_members()
            elif command == 8:
                self.join_a_channel()
            elif command == 9:
                self.leave_a_channel()
            elif command == 10:
                self.remove_a_channel_member()
            else:
                pass

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
                command = -1
                while command != 0:
                    self.print_chat_message_menu()
                    command = self.get_user_command()
                    if command == 1:
                        self.list_channel_messages()
                    elif command == 2:
                        self.send_channel_messages()
                    elif command == 3:
                        self.update_a_channel_message()
                    elif command == 4:
                        self.delete_a_channel_message()
                    else:
                        pass

    """User function"""

    def print_user_info(self):
        self.user = json.loads(self.client.user.get(id="me").content)
        print("ID =", self.user["id"])
        print("Email =", self.user["email"])
        print("Name =", self.user["first_name"] + " " + self.user["last_name"])

    """Chat massage functions"""

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

    """Chat channel functions"""

    def list_channels(self):
        self.print_title("List channels")
        # TODO(Urgent): - Need to add recursive list all channels if count is over 10
        response = self.client.chat_channels.list()
        if self.is_valid_response(response):
            self.print_channels_with_title(
                "Succeed to list all channels", response.json()
            )
            print()
        else:
            return

    def create_a_channel(self):
        self.print_title("Create a channel")
        channel_name = self.get_user_input("Please input a channel name(ex. test): ")
        # TODO: - Check email formats
        # TODO: - Add multiple email support or empty email support
        email = self.get_user_input("Please input a email(ex. test@gmail.com): ")
        channel_members = [{"email": email}]
        response = self.client.chat_channels.create(
            name=channel_name, type=1, members=channel_members
        )

        if self.is_valid_response(response):
            self.print_channel_with_title(
                "Succeed to create a channel", response.json()
            )
            print()
        else:
            return

    def get_a_channel(self):
        self.print_title("Get a channel")
        channel_id = self.get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        response = self.client.chat_channels.get(channel_id=channel_id)

        if self.is_valid_response(response):
            self.print_channel_with_title("Succeed to get a channel", response.json())
            print()
        else:
            return

    def update_a_channel(self):
        self.print_title("Update a channel")
        channel_id = self.get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        channel_name = self.get_user_input("Please input a name(ex. test): ")
        response = self.client.chat_channels.update(
            channel_id=channel_id, name=channel_name
        )

        if self.is_valid_response(response):
            print("------------------------------")
            print("Succeed to update a channel")
            print("------------------------------")
            print()
        else:
            return

    def delete_a_channel(self):
        self.print_title("Delete a channel")
        channel_id = self.get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        response = self.client.chat_channels.delete(channel_id=channel_id)

        if self.is_valid_response(response):
            print("------------------------------")
            print("Succeed to delete a channel")
            print("------------------------------")
            print()
        else:
            return

    def list_channel_members(self):
        self.print_title("List channel members")
        channel_id = self.get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        response = self.client.chat_channels.list_members(channel_id=channel_id)

        if self.is_valid_response(response):
            self.print_members_with_title(
                "Succeed to list channel members", response.json()
            )
            print()
        else:
            return

    def invite_channel_members(self):
        self.print_title("Invite channel members")
        self.list_external_contacts()

        channel_id = self.get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        # You can invite up to a max number of 5 members with a single API call
        # channel_members = [{"email": "wcyang1@uci.edu"}, {"email": "jeffbalala@gmail.com"}]
        # TODO: - Check email formats
        # TODO: - Add multiple email support or empty email support
        # TODO: - Add multiple api call if emails are over 5
        email = self.get_user_input("Please input a email(ex. test@gmail.com): ")
        channel_members = [{"email": email}]
        response = self.client.chat_channels.invite_members(
            channel_id=channel_id, members=channel_members
        )

        if self.is_valid_response(response):
            self.print_invite_channel_memners_result_with_title(
                "Succeed to invite channel members", response.json()
            )
            print()
        else:
            return

    def join_a_channel(self):
        self.print_title("Join a channel")
        channel_id = self.get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        response = self.client.chat_channels.join(channel_id=channel_id)

        if self.is_valid_response(response):
            self.print_join_a_channel_result_with_title(
                "Succeed to join a channel", response.json()
            )
            print()
        else:
            return

    def leave_a_channel(self):
        self.print_title("Leave a channel")
        channel_id = self.get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        response = self.client.chat_channels.leave(channel_id=channel_id)

        if self.is_valid_response(response):
            self.print_title("Succeed to leave a channel")
            print()
        else:
            return

    def remove_a_channel_member(self):
        self.print_title("Remove a member")
        channel_id = self.get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        member_id = self.get_user_input(
            "Please input a member id(ex. p1d-2aj2rx2mbohcae8tpw): "
        )
        response = self.client.chat_channels.remove_member(
            channel_id=channel_id, member_id=member_id
        )

        if self.is_valid_response(response):
            self.print_title("Succeed to remove a member")
            print()
        else:
            return

    def list_external_contacts(self):
        # TODO: - Create a contact component
        res = self.client.get_request(
            "/chat/users/me/contacts", params={"type": "external"}
        )
        contacts = json.loads(res.content)["contacts"]
        print("# User's external contacts")
        for contact in contacts:
            print(f"{contact['id']} {contact['email']}")


if __name__ == "__main__":
    Bot().run()
