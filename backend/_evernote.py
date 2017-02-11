import functools
import time

from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from evernote.edam.error.ttypes import EDAMUserException, EDAMSystemException

from evernoteExceptions import NoteBookNotFoundError
import config


ERR_RATE_LIMIT = 19


def auth_client():
    return EvernoteClient(
            consumer_key=config.consumer_key,
            consumer_secret=config.consumer_secret,
            sandbox=config.sandbox
        )

#http://stackoverflow.com/questions/11420464/python-catch-exceptions-inside-a-class
def catch_rate_limit_exception(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except EDAMSystemException as e:
            if e.errorCode != ERR_RATE_LIMIT: raise
            print 'Sleeping for %d seconds until rate limit is passed.' % e.rateLimitDuration
            time.sleep(e.rateLimitDuration)
            return f(*args, **kwargs)
    return func


class NoteClient(object):

    def __init__(self, token):
        self.client = EvernoteClient(token=token, sandbox=config.sandbox)
        self.noteStore = self.client.get_note_store()

    
    def create_notebook(self, name):
        notebook = Types.Notebook()
        notebook.name = name
        createdNotebook = self.noteStore.createNotebook(notebook)
        uid = createdNotebook.guid
        return uid

    
    def get_notebook(self, name):
        notebooks = self.noteStore.listNotebooks()
        for nb in notebooks:
            # Notebook names are not case sensitive.
            if nb.name.lower() == name.lower():
                return nb
        raise NoteBookNotFoundError


    def create_note(self, title,content, notebook_uid=None):
        note = Types.Note()
        note.title = title
        if notebook_uid is not None:
            note.notebookGuid = notebook_uid
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>'+ content + '</en-note>'
        try:
            return self.noteStore.createNote(note)
        # This error may occur if the url is malformed or has not been xml-sanitized.
        except EDAMUserException as e:
            raise

    def create_note_check_rate_limit(self, title, content, notebook_uid=None):
        """create note and sleep for required time if rateLimitException occurs"""
        try:
            self.create_note(title, content, notebook_uid=notebook_uid)
        except EDAMSystemException as e:
            if e.errorCode != ERR_RATE_LIMIT: raise
            print 'Sleeping for %d seconds until rate limit is passed.' % e.rateLimitDuration
            time.sleep(e.rateLimitDuration)
            self.create_note(title, content, notebook_uid=notebook_uid)


    def send_bookmarks(self, bookmarks, notebook_uid):
        """ Send array of bookmarks to Evernote, handling rateLimitExceptions """
         # @TODO handle case when Evernote API Rate Limit goes over
        for b in bookmarks:
            title = b['title']
            content = b['content']
            self.create_note_check_rate_limit(title, content, notebook_uid=notebook_uid)




