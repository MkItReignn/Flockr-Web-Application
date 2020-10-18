import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import channel 
import flask


APP = flask.Flask(url)
# just uploading new branch

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
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

def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}

def test_channel_invite(url):
    '''
    '''
    @APP.route(url + '/channel/invite', methods=['POST'])
    resp = requests.get(url + '/channel/invite', params={'data': 'hello'})
    payload = resp.json()
    print(payload)
    


if __name__ == "__main__":
    test_channel_invite()