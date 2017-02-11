from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from evernote.edam.error.ttypes import EDAMUserException, EDAMSystemException

from evernoteExceptions import NoteBookNotFoundError
import config


def auth_client():
    return EvernoteClient(
            consumer_key=config.consumer_key,
            consumer_secret=config.consumer_secret,
            sandbox=config.sandbox
        )


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

    def send_bookmarks(self, bookmarks, notebook_uid):
        """ Send array of bookmarks to Evernote, handling rateLimitExceptions """
         # @TODO handle case when Evernote API Rate Limit goes over
        for b in bookmarks:
            title = b['title']
            content = b['content']
            self.note_client.create_note(title, content, notebook_uid=notebook_uid)


