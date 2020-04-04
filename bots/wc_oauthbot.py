import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient
from zoomapi import util
import json
from configparser import ConfigParser
from pyngrok import ngrok

def load_bot_settings():
    parser = ConfigParser()
    parser.read("bots/bot.ini")
    client_id = parser.get("OAuth", "client_id")
    client_secret = parser.get("OAuth", "client_secret")
    port = parser.getint("OAuth", "port", fallback=4001)
    browser_path = parser.get("OAuth", "browser_path")
    print(f'id: {client_id} browser: {browser_path}')

    redirect_url = ngrok.connect(port, "http")
    print("Redirect URL is", redirect_url)

    return client_id, client_secret, port, browser_path, redirect_url

def test_get_user(client):
    user_response = client.user.get(id='me')
    # json = user_response.json()
    # print('json:', json)

    json_data = json.loads(user_response.content)
    print('json_data:', json_data)

def test_apis(client):
    # test get user
    user = json.loads(client.user.get(id='me').content)
    # test list meetings
    meetings = json.loads(client.meeting.list(user_id="me").content)
    # test list channels
    channels = json.loads(client.chat_channels.list().content)["channels"]

    print ("------------------------------")
    print("user:", user)
    print ("------------------------------")
    print("meetings:", meetings)
    print ("------------------------------")
    print("channels:", channels)
    print ("------------------------------")

    # test send message to 'test' channel
    test_bot_send_message(client, "test", channels)

def test_bot_send_message(client, channel_name, channels):
    for channel in channels:
        if channel_name in channel.values():
            print("Found channel test", channel["id"])
            channel_id = to_channel=channel["id"]
    
    if not channel_id:
        print(f'Error: cannot find: {channel_name}')
    else:
        stop = False
        while not stop:
            message = input("Enter message: ")
            print(client.chat_messages.post(to_channel=channel_id, message=message))
            if message == "stop":
                stop = True

def test_list_user_channels(client):
    list_user_channel_response = client.chat_channels.list()
    json_data = list_user_channel_response.json()
    channels = json_data["channels"]
    print ("------------------------------")
    print("Succeed to List User's Channels:")
    for channel in channels:
        print_channel(channel)
        print()
    print ("------------------------------")

def test_create_channel(client):
    channel_name = "test_channel_6"
    channel_members = [{"email": "wcyang1@uci.edu"}, {"email": "jeffbalala@gmail.com"}]
    create_channel_response = client.chat_channels.create(name=channel_name, type=1, members=channel_members)
    json_data = create_channel_response.json()
    print ("------------------------------")
    print("Succeed to Create a Channel:")
    print_channel(json_data)
    print ("------------------------------")
    
def test_get_channel(client):
    channel_id = "b7c8bc2a-d208-45dd-955a-dd3ef6c2ecdb"
    get_channel_response = client.chat_channels.get(channel_id=channel_id)
    json_data = get_channel_response.json()
    print ("------------------------------")
    print("Succeed to Get a Channel:")
    print_channel(json_data)
    print ("------------------------------")

def test_update_channel(client):
    channel_id = "b7c8bc2a-d208-45dd-955a-dd3ef6c2ecdb"
    channel_name = "update_channel_6"
    update_channel_response = client.chat_channels.update(channel_id=channel_id, name=channel_name)
    print ("------------------------------")
    print("Succeed to Update a Channel")
    print ("------------------------------")

def test_delete_channel(client):
    channel_id = "b7c8bc2a-d208-45dd-955a-dd3ef6c2ecdb"
    delete_channel_response = client.chat_channels.delete(channel_id=channel_id)
    print ("------------------------------")
    print("Succeed to Delete a Channel")
    print ("------------------------------")

def test_list_channel_members(client):
    channel_id = "1cb910ea028d4dee9c960bb4e14e8fdc"
    list_channel_members_response = client.chat_channels.list_members(channel_id=channel_id)
    json_data = list_channel_members_response.json()
    members = json_data["members"]
    print ("------------------------------")
    print("Succeed to List Channel Members:")
    for member in members:
        print("email:", member["email"])
        print("name:", member["name"])
        print("role:", member["role"])
        print()
    print ("------------------------------")

def print_channel(json_data):
    print("channel id:", json_data["id"])
    print("channel jid:", json_data["jid"])
    print("channel name:", json_data["name"])
    print("channel type:", json_data["type"])

def test_channel_endpoints():
    # test_create_channel(client)
    # test_list_user_channels(client)
    # test_get_channel(client)
    # test_update_channel(client)
    # test_delete_channel(client)
    test_list_channel_members(client)

if __name__ == "__main__":
    client_id, client_secret, port, browser_path, redirect_url = load_bot_settings()
    client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)
    test_channel_endpoints()
    # test_apis(client)
    