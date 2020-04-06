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
import re


class Bot:
    """A bot for executing chat channel and chat message function"""

    def __init__(self):
        (
            client_id,
            client_secret,
            port,
            browser_path,
            redirect_url,
        ) = self.__load_bot_settings()
        self.__client = OAuthZoomClient(
            client_id, client_secret, port, redirect_url, browser_path,
        )

    """Utility functions"""

    def __load_bot_settings(self):
        parser = ConfigParser()
        parser.read("bots/bot.ini")

        client_id = parser.get("OAuth", "client_id")
        client_secret = parser.get("OAuth", "client_secret")
        port = parser.getint("OAuth", "port", fallback=4001)
        browser_path = parser.get("OAuth", "browser_path")
        redirect_url = ngrok.connect(port, "http")
        return client_id, client_secret, port, browser_path, redirect_url

    def __get_user_command(self):
        try:
            command = int(input("Please select a command(ex. 1): "))
            return command
        except ValueError:
            print("Invalid command, please enter a correct command!")
            return -1

    def __get_user_input(self, placeholder):
        user_input = None
        while user_input is None:
            user_input = input(placeholder)
        return user_input

    def __get_valid_user_input_email(self):
        user_input = None
        while user_input is None or not self.__is_valid_email(user_input):
            user_input = input("Please input a email(ex. test@gmail.com): ")
        return user_input

    def __is_valid_email(self, email):
        regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        if not re.search(regex, email):
            print("Email format is invalid")
            return False
        return True

    def __get_valid_user_input_email_list(self):
        max_email_number = 5
        print(
            "You can enter at most "
            + str(max_email_number)
            + " email addresses ('q' to quit)"
        )

        email_list = []

        while len(email_list) < max_email_number:
            user_input = input(
                "Enter email "
                + str(len(email_list) + 1)
                + "('q' to quit or 'Enter' to continue): "
            )
            if user_input.lower() == "q":
                break
            elif len(user_input) == 0:
                email = self.__get_valid_user_input_email()
                email_list.append(email)
            else:
                print("user_input:", user_input)
                print("Please input 'q' to quit or 't' to continue\n")

        return email_list

    def __is_valid_response(self, response):
        if response.status_code > 299:
            print("Something goes wrong. Please retry.\n")
            return False
        return True

    """Log"""

    def __print_title(self, title):
        print("------------------------------")
        print("# " + title)
        print("------------------------------")

    def __print_channel_with_title(self, title, json_data):
        print("------------------------------")
        print("# " + title)
        print(f"{json_data['name']}: {json_data['id']}")
        print("------------------------------")

    def __print_channels_with_title(self, title, json_array):
        print("------------------------------")
        print("# " + title)
        i = 0
        for channel in json_array["channels"]:
            print(f"[{i}] {channel['name']}: {channel['id']}")
            i += 1
        print("------------------------------")

    def __print_members_with_title(self, title, json_array):
        print("------------------------------")
        print("# " + title)
        i = 0
        for member in json_array["members"]:
            print(f"[{i + 1}] {member['name']}({member['role']}): {member['email']}")
            i += 1
        print("------------------------------")

    def __print_invite_channel_memners_result_with_title(self, title, json_data):
        added_at = json_data["added_at"]
        ids = json_data["ids"]
        print("------------------------------")
        print("# " + title + " at " + added_at)
        print("Ids: " + ids)
        print("------------------------------")

    def __print_join_a_channel_result_with_title(self, title, json_data):
        added_at = json_data["added_at"]
        id = json_data["id"]
        print("------------------------------")
        print("# " + title + " at " + added_at)
        print("Id: " + id)
        print("------------------------------")

    """Menu"""

    def __print_main_menu(self):
        print("# Main Menu #")
        print("[1] Execute a MEANINGFUL set of Chat Channel Functions;")
        print("[2] Execute a single Chat Channel Function (debug only);")
        print("[3] Execute a MEANINGFUL set of Chat Message Functions;")
        print("[4] Execute a single Chat Message Function (debug only);")
        print("[0] Quit;")

    def __print_chat_channel_menu(self):
        print("# Chat Channel Menu #", self.__user["email"])
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

    def __print_chat_message_menu(self):
        print("# Chat Message Menu #", self.__channel["name"])
        print("[1] List channel messages;")
        print("[2] Send channel messages;")
        print("[3] Update a message;")
        print("[4] Delete a message;")
        print("[0] Quit;")

    """Bot implementations"""

    def __execute_set_of_chat_channel_functions(self):
        print("# Executing a set of Chat Channel Functions...")

        # 1
        input("# Part 1: Test listing channels (Press Enter to continue)")
        self.__list_channels()

        # 2
        input("# Part 2: Test creating a channel (Press Enter to continue)")
        name = self.__get_user_input("Please input a name for the channel: ")
        res = self.__client.chat_channels.create(name=name, type=1)
        if not self.__is_valid_response(res):
            return
        cid = res.json()["id"]

        # 3
        input("# Part 3: Test getting a channel (Press Enter to continue)")
        self.__get_a_channel_by_id(channel_id=cid)

        # 4
        input("# Part 4: Test updating a channel (Press Enter to continue)")
        name = self.__get_user_input("Please input a name for the channel: ")
        res = self.__client.chat_channels.update(channel_id=cid, name=name)
        if not self.__is_valid_response(res):
            return
        time.sleep(1)
        self.__get_a_channel_by_id(channel_id=cid)

        # 5
        input("# Part 5: Test listing members of a channel (Press Enter to continue)")
        self.__list_channel_members_by_id(cid)

        # 6
        input("# Part 6: Test inviting a member to a channel (Press Enter to continue)")
        self.__list_external_contacts()
        email = self.__get_valid_user_input_email()
        self.__client.chat_channels.invite_members(
            channel_id=cid, members=[{"email": email}]
        )
        time.sleep(1)
        self.__list_channel_members_by_id(cid)

        # 7
        input(
            "# Part 7: Test removing a member from a channel (Press Enter to continue)"
        )
        self.__list_channel_members_by_id(cid)
        time.sleep(1)
        self.__list_external_contacts()
        mid = self.__get_user_input("Please input a member id (not email): ")
        self.__client.chat_channels.remove_member(channel_id=cid, member_id=mid)
        time.sleep(1)
        self.__list_channel_members_by_id(cid)

        # 8
        input("# Part 8: Test deleting a channel (Press Enter to continue)")
        self.__list_channels()
        time.sleep(1)
        print("Deleting", cid)
        self.__client.chat_channels.delete(channel_id=cid)
        time.sleep(1)
        self.__list_channels()

        # 9
        print("By default we are testing with our channel 'test-leave-join'.")
        input("# Part 9: Test leaving a channel (Press Enter to continue)")
        cid = "1cb910ea028d4dee9c960bb4e14e8fdc"
        print("Leaving channel", cid)
        self.__client.chat_channels.leave(channel_id=cid)
        time.sleep(1)
        self.__list_channels()

        # 10
        input("# Part 10: Test joining a channel (Press Enter to continue)")
        print("Joining channel", cid)
        self.__client.chat_channels.join(channel_id=cid)
        time.sleep(1)
        self.__list_channels()

    def __execute_single_chat_channel_function(self):
        command = -1

        while command != 0:
            self.__print_chat_channel_menu()
            command = self.__get_user_command()
            print("")

            if command == 1:
                self.__list_channels()
            elif command == 2:
                self.__create_a_channel()
            elif command == 3:
                self.__get_a_channel(None)
            elif command == 4:
                self.__update_a_channel()
            elif command == 5:
                self.__delete_a_channel()
            elif command == 6:
                self.__list_channel_members(None)
            elif command == 7:
                self.__invite_channel_members()
            elif command == 8:
                self.__join_a_channel()
            elif command == 9:
                self.__leave_a_channel()
            elif command == 10:
                self.__remove_a_channel_member()
            else:
                pass

    def __execute_set_of_chat_message_functions(self):
        print("# Executing a set of Chat Message Functions...")

        # 0
        self.__list_channels()
        try:
            i = int(input("First, please select a channel:\n"))
        except ValueError:
            print(f"{i} is not a number.")
            return
        self.__channel = self.__channels[i % len(self.__channels)]
        print("You have selected channel", self.__channel["name"])

        # 1
        input("# Part 1: Test sending messages (Press Enter to continue)")
        msg = input("Then, please send a message to the channel:\n")
        response = self.__client.chat_messages.post(
            to_channel=self.__channel["id"], message=msg
        )
        print("The response is", response)
        if response.status_code > 299:  # OK status codes start with 2
            print("Something goes wrong. Please retry.")
            return
        mid = response.json()["id"]

        # 2
        input("# Part 2: Test listing messages (Press Enter to continue)")
        print("Then please review the message history.")
        self.__list_channel_messages()
        print(f'Did you see "{msg}" there? Great.')

        # 3
        input("# Part 3: Test updating messages (Press Enter to continue)")
        print(f'Then we are going to update "{msg}".')
        msg = input("Please input a new message:\n")
        response = self.__client.chat_messages.update(
            message_id=mid, message=msg, to_channel=self.__channel["id"],
        )
        print("The response is", response)
        if response.status_code > 299:  # OK status codes start with 2
            print("Something goes wrong. Please retry.")
            return
        time.sleep(1)
        self.__list_channel_messages()
        print(f'Did you see "{msg}" there? Great.')

        # 4
        input("# Part 4: Test removing messages (Press Enter to continue)")
        print(f'Then we are going to delete "{msg}".')
        response = self.__client.chat_messages.delete(
            message_id=mid, to_channel=self.__channel["id"],
        )
        print("The response is", response)
        time.sleep(1)
        self.__list_channel_messages()
        print(f'Did you see "{msg}" gone? Great.')

        print("# Execution finished.")

    def __execute_single_chat_message_function(self):
        while True:
            self.__list_channels()
            try:
                i = int(input("Please select a channel: "))
            except ValueError:
                break
            self.__channel = self.__channels[i]
            if self.__channel["id"] != None:
                command = -1
                while command != 0:
                    self.__print_chat_message_menu()
                    command = self.__get_user_command()
                    if command == 1:
                        self.__list_channel_messages()
                    elif command == 2:
                        self.__send_channel_messages()
                    elif command == 3:
                        self.__update_a_channel_message()
                    elif command == 4:
                        self.__delete_a_channel_message()
                    else:
                        pass

    """User function"""

    def __print_user_info(self):
        self.__user = json.loads(self.__client.user.get(id="me").content)
        print("ID =", self.__user["id"])
        print("Email =", self.__user["email"])
        print("Name =", self.__user["first_name"] + " " + self.__user["last_name"])

    """Chat massage functions"""

    def __list_channel_messages(self):
        try:
            test_channel_messages_content = json.loads(
                self.__client.chat_messages.list(
                    user_id=self.__user["id"], to_channel=self.__channel["id"]
                ).content
            )
            print("# History of the channel", self.__channel["name"])
            for msg in test_channel_messages_content["messages"]:
                print(
                    f"[{msg['date_time']}] {msg['sender']}: {msg['message']} id={msg['id']}"
                )
        except:
            print(test_channel_messages_content)
        finally:
            # self.client.refresh_token()
            pass

    def __send_channel_messages(self):
        while True:
            message = input("Enter message ('q' to stop): ")
            if message == "q":
                break
            response = self.__client.chat_messages.post(
                to_channel=self.__channel["id"], message=message
            )
            print(response)

    def __update_a_channel_message(self):
        self.__list_channel_messages()
        message_id = input("Enter message id: ")
        message_new = input("Enter new message content: ")
        response = self.__client.chat_messages.update(
            message_id=message_id, message=message_new, to_channel=self.__channel["id"],
        )
        print(response)

    def __delete_a_channel_message(self):
        self.__list_channel_messages()
        message_id = input("Enter message id: ")
        response = self.__client.chat_messages.delete(
            message_id=message_id, to_channel=self.__channel["id"],
        )
        print(response)

    """Chat channel functions"""

    def __list_channels(self):
        self.__print_title("List channels")
        response = self.__client.chat_channels.list()
        if self.__is_valid_response(response):
            self.__channels = response.json()["channels"]
            self.__print_channels_with_title(
                "Succeed to list all channels", response.json()
            )
            print()
        else:
            return

    def __create_a_channel(self):
        self.__print_title("Create a channel")
        channel_name = self.__get_user_input("Please input a channel name(ex. test): ")
        email_list = self.__get_valid_user_input_email_list()
        channel_members = []
        for email in email_list:
            channel_member = {"email": email}
            channel_members.append(channel_member)
        response = self.__client.chat_channels.create(
            name=channel_name, type=1, members=channel_members
        )

        if self.__is_valid_response(response):
            self.__print_channel_with_title(
                "Succeed to create a channel", response.json()
            )
            print()
        else:
            return

    def __get_a_channel(self, channel_id):
        self.__print_title("Get a channel")
        if channel_id is None:
            channel_id = input(
                "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
            )
        response = self.__client.chat_channels.get(channel_id=channel_id)

        if self.__is_valid_response(response):
            self.__print_channel_with_title("Succeed to get a channel", response.json())
            print()
        else:
            return

    def __get_a_channel_by_id(self, channel_id):
        self.__print_title("Get a channel")
        response = self.__client.chat_channels.get(channel_id=channel_id)
        if self.__is_valid_response(response):
            self.__print_channel_with_title("Succeed to get a channel", response.json())
            print()

    def __update_a_channel(self):
        self.__print_title("Update a channel")
        channel_id = self.__get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        channel_name = self.__get_user_input("Please input a name(ex. test): ")
        response = self.__client.chat_channels.update(
            channel_id=channel_id, name=channel_name
        )

        if self.__is_valid_response(response):
            print("------------------------------")
            print("Succeed to update a channel")
            print("------------------------------")
            print()
        else:
            return

    def __delete_a_channel(self):
        self.__print_title("Delete a channel")
        channel_id = self.__get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        response = self.__client.chat_channels.delete(channel_id=channel_id)

        if self.__is_valid_response(response):
            print("------------------------------")
            print("Succeed to delete a channel")
            print("------------------------------")
            print()
        else:
            return

    def __list_channel_members(self, channel_id):
        self.__print_title("List channel members")
        if channel_id is None:
            channel_id = input(
                "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
            )
        response = self.__client.chat_channels.list_members(channel_id=channel_id)

        if self.__is_valid_response(response):
            self.__print_members_with_title(
                "Succeed to list channel members", response.json()
            )
            print()
        else:
            return

    def __list_channel_members_by_id(self, channel_id):
        self.__print_title("List channel members")
        response = self.__client.chat_channels.list_members(channel_id=channel_id)

        if self.__is_valid_response(response):
            self.__print_members_with_title(
                "Succeed to list channel members", response.json()
            )
            print()

    def __invite_channel_members(self):
        self.__print_title("Invite channel members")
        self.__list_external_contacts()

        channel_id = self.__get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        email_list = self.__get_valid_user_input_email_list()
        channel_members = []
        for email in email_list:
            channel_member = {"email": email}
            channel_members.append(channel_member)
        response = self.__client.chat_channels.invite_members(
            channel_id=channel_id, members=channel_members
        )

        if self.__is_valid_response(response):
            self.__print_invite_channel_memners_result_with_title(
                "Succeed to invite channel members", response.json()
            )
            print()
        else:
            return

    def __join_a_channel(self):
        self.__print_title("Join a channel")
        channel_id = self.__get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        response = self.__client.chat_channels.join(channel_id=channel_id)

        if self.__is_valid_response(response):
            self.__print_join_a_channel_result_with_title(
                "Succeed to join a channel", response.json()
            )
            print()
        else:
            return

    def __leave_a_channel(self):
        self.__print_title("Leave a channel")
        channel_id = self.__get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        response = self.__client.chat_channels.leave(channel_id=channel_id)

        if self.__is_valid_response(response):
            self.__print_title("Succeed to leave a channel")
            print()
        else:
            return

    def __remove_a_channel_member(self):
        self.__print_title("Remove a member")
        channel_id = self.__get_user_input(
            "Please input a channel id(ex. 45dcf4e6-3ad5-433c-8081-764c1866c46a): "
        )
        member_id = self.__get_user_input(
            "Please input a member id(ex. p1d-2aj2rx2mbohcae8tpw): "
        )
        response = self.__client.chat_channels.remove_member(
            channel_id=channel_id, member_id=member_id
        )

        if self.__is_valid_response(response):
            self.__print_title("Succeed to remove a member")
            print()
        else:
            return

    def __list_external_contacts(self):
        res = self.__client.contacts.list_external()
        contacts = res.json()["contacts"]
        print("# User's external contacts")
        for contact in contacts:
            print(f"{contact['id']} {contact['email']}")

    """Main"""

    def run(self):
        print("------------------------------")
        print("# You are logged in as")
        self.__print_user_info()
        print("------------------------------")

        command = -1

        while command != 0:
            self.__print_main_menu()
            command = self.__get_user_command()
            print("")

            if command == 1:
                self.__execute_set_of_chat_channel_functions()
            elif command == 2:
                self.__execute_single_chat_channel_function()
            elif command == 3:
                self.__execute_set_of_chat_message_functions()
            elif command == 4:
                self.__execute_single_chat_message_function()
            else:
                pass

if __name__ == "__main__":
    Bot().run()
