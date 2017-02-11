import requests
import datetime
import pytest
import os
from os import path
import sys

# Add backend directory to path.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from backend import config, _evernote as evernote
config.sandbox=True
token = config.dev_token

MAX_API_CALLS_ALLOWED = 100

# some tests are really slow.
# http://doc.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)

# This class relies on a Python server ( `python app.py &` ) running in the background.
class TestServer(object):

    def setup_class(self):
        port = int(os.environ.get('PORT', 5000))
        self.HOST = 'http://localhost:%d' % port

    def test_home(self):
        response = requests.get(self.HOST)
        assert response.status_code == 200


    def test_create_access(self):
        response = requests.post(self.HOST+'/create', data={
    		'title': 'title',
    		'content': 'some example content'
    	})
        assert response.status_code == 403

def raiseRateLimitException(*args, **kwargs):
    """ dummy function to mock a real rateLimitException """
    raise evernote.EDAMSystemException(errorCode=19, rateLimitDuration=10)

class TestAPIClient(object):


    def setup_class(self):
        self.client = evernote.NoteClient(token)

        # This line is flaky and sometimes raises errors.
        # Possible error codes:
        # Errno. 19 occurs when rate limit is breached, which can sometimes happen even on sandbox mode for some reason.
        # Errno. 10 occurs if note with same name has already been created.
        self.uid = self.client.create_notebook("bookmarks")


    def teardown_class(self):
        self.client.noteStore.expungeNotebook(self.uid)



    def test_get_notebook(self):
        notebook = self.client.get_notebook("bookmarks")
        assert notebook.name == "bookmarks"


    def test_notebook_case(self):
        assert self.uid == self.client.get_notebook("Bookmarks").guid


    def test_get_notebook_nonexistant(self):
        with pytest.raises(evernote.NoteBookNotFoundError):
            self.client.get_notebook("this_does_not_exist")


    def test_create_note(self):
        uid = self.client.create_note("New Note!", "Test", notebook_uid=self.uid)  
        assert uid

    @slow
    def test_api_limit(self):
        # It appears that teh duplicateNotebookLimiter exception is more strict than other API exceptions.
        with pytest.raises(evernote.EDAMSystemException):
            for i in range(MAX_API_CALLS_ALLOWED):
                self.client.create_note('spam', '')

    @slow
    def test_create_bookmarks(self):
        fakeBookmark = {
            "title": "example",
            "content": "http://example.com"
        }
        fakeBookmarks = [ fakeBookmark ] * MAX_API_CALLS_ALLOWED
        # we are testing that NO error occurs
        self.client.send_bookmarks(fakeBookmarks, self.uid)


