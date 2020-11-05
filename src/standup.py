'''
standup functionality.
once standups are finished, all messages sent to standup/send are packaged together in a single messaged
and posted by the user who begun the standup/
'''

from global_dic import data
from threading import Timer
from datetime import datetime
from error import InputError, AccessError
from utils import check_token, decode_token
from channel_helper import check_channel


# DICT HAS NOT BEEN UPDATED. FUNCTION WILL NOT WORK UNTIL THEN
def standup_end(channel_id):

    message_list = data['standups']['channel_id']['message']

    if len(message_list) > 0:
        standups[channel_id]['message_id'] = get_message_id()   
        standups[channel_id]['message'] = '\n'.join(message_list)
        channels[channel_id]['messages'].insert(0, standups.pop(channel_id))   
    else:
        standup.pop(channel_id)


def standup_start(token, channel_id, length):
    '''
    Function which starts standup
    '''
    # check if user's token is valid
    check_token(token)

    # check if channel_id is valid
    if check_channel(channel_id) is False:
        raise InputError("Input error as channel_id is not valid")

    if length <= 0:
        raise InputError("Input error standup length is too short")



    # check if standup is active alrady

    curr_time = datetime.now()
    time_finish = int(curr_time.timestamp() + length)

    # creates a message template
    # standup[chan.._id] contains this template

    # standup_end...     standup = Timer(length, standup_end, args=[channel_id])

    standup = Timer(length, FUNCTION args=[channel_id])
    standup.start()

    return {'time_finish': time_finish}


def standup_active(token, channel_id):
    '''
    Function which checks if standup is active
    will return a timestamp of when standup will finish
    '''
    # check if user's token is valid
    check_token(token)

    # check if channel_id is valid
    if check_channel(channel_id) is False:
        raise InputError("Input error as channel_id is not valid")

    # check if standup is active alrady
    # get standup from dict and check channel_id

    try:
        time_finish = data['standup']['channel_id']['time_created']
    except KeyError:
        time_finish = None

    return {'is_active': 'is_active', 'time_finish': 'time_finish'}


def standup_send(token, channel_id, message):
    '''
    Function which sends message during standup
    '''
    # check if user's token is valid
    check_token(token)

    # check if channel_id is valid
    if check_channel(channel_id) is False:
        raise InputError("Input error as channel_id is not valid")

    # check if message is over 1000 characters long
    if len(message) > 1000:
        raise InputError("Input error message too long")

    # Check if standup is active
    # if not active then inputerror

    # get user handle_str

    # add messages to standup
    # standup['channel_id']['message'].append(f'{handle}: {message}')


    return 0