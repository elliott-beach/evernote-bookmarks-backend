import requests
import _evernote as evernote
import config
import os

# Run tests in Evernote sandbox, not production Evernote. This also us to use the dev_token.
config.sandbox = True
token = config.dev_token

# @TODO look at how Nithin Murali did his tests and write ours in the same way.
# TODO move to environment
port = int(os.environ.get('PORT', 5000))
HOST = 'http://localhost:%d' % port

# from http://stackoverflow.com/questions/2030053/random-strings-in-python
import random, string
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def test_home():
	response = requests.get(HOST)
        assert response.status_code == 200

def test_create_access():
	response = requests.post(HOST+'/create', data={
		'title': 'title',
		'content': 'some example content'
	})
	assert response.status_code == 403

def test_create_notebook():
    # Deleting a Notebook is impossible with the API, so I cannot handle the case in which
    # The Notebook has already been created.
    try:
        evernote.create_notebook("bookmarks", config.dev_token)
    except evernote.EDAMUserException as e:
        # 10 is anticipated error code if note has already been created.
        assert e.errorCode == 10

def test_create_note_with_notebook():
    # Danger -- could result in Exception if we generate a name that was generated before.
    notebook_name = randomword(30)
    uid = evernote.create_notebook(notebook_name, token)
    note = evernote.create_note_with_notebook("New Note!", "Test", uid, token)
    assert note
