from global_dic import data
from auth import auth_login, auth_register, auth_register
from error import InputError
import uuid
import re

def valid_u_id_check(u_id):
    '''
    a function to raise input errors for invalid users
    '''
    global data
    # looping to see if u_id is a valid user, if not, input error
    found = False
    for user in data['users']:
        if u_id == user['u_id']:
            found = True
            break
    if found == False:
        raise InputError("Input 1")


def user_profile(token, u_id):
    '''
    For a valid user, returns information about their email, 
    first name, last name, and handle
    '''
    global data
    valid_u_id_check(u_id)

    # looping until we match the u_id in the global data structure
    for user in data['users']:
        if u_id == user['u_id']:
            # returning the required data
            return {
                'user': {
                    'u_id': user['u_id'],
                    'email': user['email'],
                    'name_first': user['first_name'],
                    'name_last': user['last_name'],
                    'handle_str': user['handle'],
                 },
            }


def user_profile_setname(token, name_first, name_last):
    '''
    Update the authorised user's first and last name
    '''
    global data
    # input error checking
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("Input 2")

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Input 3")
    
    # looping until we reach the user with corresponding token
    # and changing their respective first/last name
    for user in data['users']:
        if token == user['token']:
            user['first_name'] = name_first
            user['last_name'] = name_last

    return {
    }

def user_profile_setemail(token, email):
    '''
    Update the authorised user's email address
    '''
    global data
    # using the same email pattern as auth_login
    emailPattern = "^(?!.*[.]{2})[a-zA-Z0-9][a-zA-Z0-9.]+@(?!localhost)[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"
    if len(email) > 254:
        raise InputError("Input 4")
    if len(email) == 0:
        raise InputError("Input 5")
    if re.search(emailPattern, email) == None:
        raise InputError("Input 6")

    # checking if email is already being used
    for i in range(len(data["users"])):
        if (data["users"][i]["email"] == email):
            raise InputError("Input 7")

    # looping until we reach the user with corresponding token
    # and changing their email
    for user in data['users']:
        if token == user['token']:
            user['email'] = email

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name)
    '''
    global data
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Input 8")

    # checking if handle_str is already being used
    for i in range(len(data["users"])):
        if (data["users"][i]["handle"] == handle_str):
            raise InputError("Input 9")

    # looping until we reach the user with corresponding token
    # and changing their respective handle_str
    for user in data['users']:
        if token == user['token']:
            user['handle'] = handle_str

    return {
    }