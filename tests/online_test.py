import requests
import os
from os import path
import sys

# add backend directory to path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from backend import config, _evernote as evernote
config.sandbox=True
token = config.dev_token

# @TODO look at how Nithin Murali did his tests and write ours in the same way.
# TODO move to environment
port = int(os.environ.get('PORT', 5000))
HOST = 'http://localhost:%d' % port

# from http://stackoverflow.com/questions/2030053/random-strings-in-python
import random, string
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


class TestServer(object):

    def test_home(self):
        response = requests.get(HOST)
        assert response.status_code == 200

    def test_create_access(self):
        response = requests.post(HOST+'/create', data={
    		'title': 'title',
    		'content': 'some example content'
    	})
        assert response.status_code == 403

    # @TODO
    # def test_create_authorized():
    #     """ Test functionality of create method when we are logged in"""
    #     session = requests.session()
    #     response = requests.post(HOST+'/create', data={
    #         'title': 'title',
    #         'content': 'some example content'
    #     })
    #     assert response.status_code == 403

def check_create_notebook():
    try:
        evernote.create_notebook("bookmarks", config.dev_token)
    except evernote.EDAMSystemException as e:
        # 19 code occurs when rate limit is breached, which can sometimes happen on sandbox for some reason?
        assert e.errorCode == 19
        raise
    except evernote.EDAMUserException as e:
        # 10 is anticipated error code if note has already been created
        assert e.errorCode == 10


class TestAPIClient(object):

    def setup_class(self):
        check_create_notebook()

    def teardown_class(self):
        uid = evernote.get_notebook("bookmarks", token).guid
        evernote.get_client(token).get_note_store().expungeNotebook(uid)


    def test_get_notebook(self):
        notebook = evernote.get_notebook("bookmarks", config.dev_token)
        assert notebook.name == "bookmarks"

    def test_notebook_case(self):
        assert evernote.get_notebook("bookmarks", config.dev_token).guid == evernote.get_notebook("Bookmarks", config.dev_token).guid

    def test_get_notebook_err(self):
        try:
            evernote.get_notebook("this_does_not_exist", config.dev_token)
        except evernote.NoteBookNotFoundError:
            pass
        else:
            assert False

    def test_create_note_with_notebook(self):
        # Danger -- could result in Exception if we generate a name that was generated before.
        notebook_name = randomword(30)
        uid = evernote.create_notebook(notebook_name, token)
        note = evernote.create_note_with_notebook("New Note!", "Test", uid, token)
        assert note


