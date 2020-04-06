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
        ids = json_data["id"]
        print("------------------------------")
        print("# " + title + " at " + added_at)
        print("Id: " + id)
        print("------------------------------")

    """Menu"""

    def print_main_menu(self):
        print("[1] Execute a set of Chat Channel Functions;")
        print("[2] Execute a single Chat Channel Function;")
        print("[3] Execute a set of Chat Message Functions;")
        print("[4] Execute a single Chat Message Function;")
        print("[0] Quit;")

    def print_chat_channel_menu(self):
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
        print("Execute a set of Chat Channel Functions\n")

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
                self.invite_channel_members_2()
            elif command == 8:
                self.join_a_channel()
            elif command == 9:
                self.leave_a_channel()
            elif command == 10:
                self.remove_a_channel_member()
            else:
                pass

    def execute_set_of_chat_message_functions(self):
        print("Execute a set of Chat Message Functions\n")

    def execute_single_chat_message_function(self):
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

    def invite_channel_members_2(self):
        self.print_title("Invite channel members")
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
        response = self.client.chat_channels.join_channel(channel_id=channel_id)

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
        response = self.client.chat_channels.leave_channel(channel_id=channel_id)

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
        response = client.chat_channels.remove_member(
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

    def invite_channel_members(self):
        self.list_external_contacts()
        email = input("Please input a user email: ")
        res = self.client.chat_channels.invite_members(
            channel_id=self.channel["id"], members=[{"email": email}]
        )
        print(res)
        print(res.json())


if __name__ == "__main__":
    Bot().run()
