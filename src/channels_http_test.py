import pytest
import requests
import json
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
from error import InputError, AccessError

@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

###################
# Global variables
###################

authorised_user = {
    "email": "validEmail@gmail.com",
    "password": "valid_password",
    "name_first": "Phil",
    "name_last": "Knight",
}

second_user = {
    "email": "validEmail2@gmail.com",
    "password": "valid_password2",
    "name_first": "Donald",
    "name_last": "Trump",
}

###################
# Helper functions
###################

def register_user(url, user):
    # Registers a new user
    r = requests.post(f"{url}/auth/register", json = user)
    return r.json()

def login_user(url, user):
    # Registers a new user
    requests.post(f"{url}/auth/login", json = {
        "email": user['email'], 
        "password": user['password']
    })

def create_channel(url, token, name, is_public):
    # Creates a new channel
    new_channel = {
        "token": token,
        "name": name,
        "is_public": is_public,
    }
    r = requests.post(f"{url}/channels/create", json = new_channel)
    payload = r.json()
    payload["name"] = new_channel["name"]
    return payload

def invite_channel(url, token, channel_id, u_id):
    # Invites a user to a channel
    invite = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id,
    }
    r = requests.post(f"{url}/channel/invite", json = invite)
    return r.json()

###################
# channels/list
###################

def test_list_empty(url):
    '''
    No channels are created
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    r = requests.get(f"{url}/channels/list", params = {"token": user_1['token']})
    payload = r.json()
    assert payload['channels'] == []

def test_list_public(url):
    '''
    Public channels are created
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "TSM 0-6", True)
    # Create user_2 and their channel
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    channel_2 = create_channel(url, user_2['token'], "TSM Wins Worlds", True)
    # user_2 invites user_1 to channel_2
    invite_channel(url, user_2['token'], channel_2['channel_id'], user_1['u_id'])
    # Check the list of channels for user_1
    r = requests.get(f"{url}/channels/list", params = {"token": user_1['token']})
    payload = r.json()
    assert payload['channels'] == [
        {"channel_id": 0, "name": channel_1["name"]}, 
        {"channel_id": 1, "name": channel_2["name"]}
    ]

def test_list_private(url):
    '''
    A private channel is created 
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    # Create user_2 and their channel
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    private_channel = create_channel(url, user_2['token'], "TSM Wins Worlds", False)
    # user_2 invites user_1 to channel_2
    invite_channel(url, user_2['token'], private_channel['channel_id'], user_1['u_id'])
    # Check the list of channels for user_1
    r = requests.get(f"{url}/channels/list", params = {"token": user_1['token']})
    payload = r.json()
    assert payload['channels'] == [{"channel_id": 0, "name": private_channel["name"]}]
   
def test_list_mix(url):
    '''
    Create a mix of public/private channels
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and create a private and public channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    public_channel_1 = create_channel(url, user_1['token'], "TSM 0-6", True)
    public_channel_2 = create_channel(url, user_1['token'], "Donald", True)
    public_channel_3 = create_channel(url, user_1['token'], "Timmy", True)
    private_channel_1 = create_channel(url, user_1['token'], "TSM Wins Worlds", False)
    private_channel_2 = create_channel(url, user_1['token'], "L9", False)
    private_channel_3 = create_channel(url, user_1['token'], "Philgee", False)
    # Check the list of channels for user_1
    r = requests.get(f"{url}/channels/list", params = {"token": user_1['token']})
    payload = r.json()
    assert payload['channels'] == [
        {"channel_id": 0, "name": public_channel_1["name"]},
        {"channel_id": 1, "name": public_channel_2["name"]},
        {"channel_id": 2, "name": public_channel_3["name"]},
        {"channel_id": 3, "name": private_channel_1["name"]},
        {"channel_id": 4, "name": private_channel_2["name"]},
        {"channel_id": 5, "name": private_channel_3["name"]}
    ]

def test_list_uninvited(url):
    '''
    Create a user that is not invited to any public/private channels
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create uuninvited_user
    uninvited_user = register_user(url, authorised_user)
    login_user(url, authorised_user)
    # Create user_2 and their channels
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    create_channel(url, user_2['token'], "Donald", True)
    create_channel(url, user_2['token'], "Timmy", True)
    create_channel(url, user_2['token'], "TSM Wins Worlds", False)
    create_channel(url, user_2['token'], "L9", False)
    
    # Check the list of channels for uninvited_user
    r = requests.get(f"{url}/channels/list", params = {"token": uninvited_user['token']})
    payload = r.json()
    assert payload['channels'] == []

###################
# channels/listall
###################

def test_listall_empty(url):
    '''
    No channels are created
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    r = requests.get(f"{url}/channels/listall", params={"token": user_1['token']})
    payload = r.json()
    assert payload['channels'] == []

def test_listall_individual(url):
    '''
    Two users creates a public channel each but have not invited each other 
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "TSM 0-6", True)
    # Create user_2 and their channel
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    channel_2 = create_channel(url, user_2['token'], "TSM Wins Worlds", True)
    # Check the list of channels for user_1
    r = requests.get(f"{url}/channels/listall", params = {"token": user_1['token']})
    payload = r.json()
    assert payload['channels'] == [
        {"channel_id": 0, "name": channel_1["name"]}, 
        {"channel_id": 1, "name": channel_2["name"]}
    ]

def test_listall_public(url):
    '''
    A user creates many public channels but user_2 is not invited to any of them
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and creates many public channels
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    public_channel_1 = create_channel(url, user_1['token'], "TSM 0-6", True)
    public_channel_2 = create_channel(url, user_1['token'], "Donald", True)
    public_channel_3 = create_channel(url, user_1['token'], "Timmy", True)
    public_channel_4 = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    public_channel_5 = create_channel(url, user_1['token'], "L9", True)
    public_channel_6 = create_channel(url, user_1['token'], "Philgee", True)

    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    # Check the list of channels for user_2
    r = requests.get(f"{url}/channels/list", params = {"token": user_2['token']})
    payload = r.json()
    assert payload['channels'] == [
        {"channel_id": 0, "name": public_channel_1["name"]},
        {"channel_id": 1, "name": public_channel_2["name"]},
        {"channel_id": 2, "name": public_channel_3["name"]},
        {"channel_id": 3, "name": public_channel_4["name"]},
        {"channel_id": 4, "name": public_channel_5["name"]},
        {"channel_id": 5, "name": public_channel_6["name"]}
    ]

def test_listall_mix(url):
    '''
    Both users creates public/private channels but have not invited each other
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and create a private and public channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    public_channel_1 = create_channel(url, user_1['token'], "TSM 0-6", True)
    private_channel_1 = create_channel(url, user_1['token'], "L9", False)
    # Create user_2 and create a private and public channel
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    public_channel_2 = create_channel(url, user_2['token'], "Donald", True)
    create_channel(url, user_2['token'], "TSM Wins Worlds", False)
    # Check the list of channels for user_1
    r = requests.get(f"{url}/channels/list", params = {"token": user_1['token']})
    payload = r.json()
    assert payload['channels'] == [
        {"channel_id": 0, "name": public_channel_1["name"]},
        {"channel_id": 1, "name": private_channel_1["name"]},
        {"channel_id": 2, "name": public_channel_2["name"]}
    ]

def test_listall_uninvited(url):
    '''
    Create two different users with one user creating a private channel
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "TSM 0-6", True)
    # Create user_2 and their channel
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    create_channel(url, user_2['token'], "TSM Wins Worlds", False)
    # Check the list of channels for user_1
    r = requests.get(f"{url}/channels/listall", params = {"token": user_1['token']})
    payload = r.json()
    assert payload['channels'] == [
        {"channel_id": 0, "name": channel_1["name"]}
    ]

###################
# channels/creates
###################

def test_creates_long(url):
    '''
    Channel names that are too long (over 20 characters)
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user) 
    login_user(url, authorised_user)       
    with pytest.raises(InputError):
        create_channel(url, user_1['token'], "ThisIsATestForALongChannelName", True)
    with pytest.raises(InputError):
        create_channel(url, user_1['token'], "The Kanye East experience", True)

def test_creates_success(url):
    '''
    Acceptable channel names
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user)   
    login_user(url, authorised_user)     
    channel_1 = create_channel(url, user_1['token'], "Chicken Nuggets", True)
    assert channel_1['channel_id'] == 0
    channel_2 = create_channel(url, user_1['token'], "TSM Legends", True)
    assert channel_2['channel_iq'] == 1

def test_creates_empty(url):
    '''
    Channel names that are empty or white spaces
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user)   
    login_user(url, authorised_user)     
    with pytest.raises(InputError):
        create_channel(url, user_1['token'], "      ", True)
    with pytest.raises(InputError):
        create_channel(url, user_1['token'], "", True)

def test_creates_integer(url):
    '''
    Channel name only consists of integers
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user)   
    login_user(url, authorised_user)     
    channel_num = create_channel(url, user_1['token'], "2020", True)
    assert channel_num['channel_id'] == 0

def test_creates_special(url):
    '''
    Channel name only consists of special characters
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user)    
    login_user(url, authorised_user)    
    channel_special = create_channel(url, user_1['token'], "#*$@*!", True)
    assert channel_special['channel_id'] == 0

def test_creates_mix(url):
    '''
    Channel name consists of a combination of all types
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user) 
    login_user(url, authorised_user)       
    channel_mix = create_channel(url, user_1['token'], "COVID-19", True)
    assert channel_mix['channel_id'] == 0

def test_creates_public(url):
    '''
    Create a public channel
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user)   
    login_user(url, authorised_user)     
    channel_public = create_channel(url, user_1['token'], "Yummy", True)
    assert channel_public['channel_id'] == 0

def test_creates_private(url):
    '''
    Create a private channel
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")
    user_1 = register_user(url, authorised_user)    
    login_user(url, authorised_user)    
    channel_private = create_channel(url, user_1['token'], "Tummy", False)
    assert channel_private['channel_id'] == 0
