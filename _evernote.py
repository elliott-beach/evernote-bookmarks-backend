from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from evernote.edam.error.ttypes import EDAMUserException

import config

# TODO move exceptions to separate file
class EvernoteError(Exception):
    pass

class NoteNotFoundError(EvernoteError):
    pass

def get_client(token=None):
    if token:
        return EvernoteClient(token=token, sandbox=config.sandbox)
    else:
        return EvernoteClient(
            consumer_key=config.consumer_key,
            consumer_secret=config.consumer_secret,
            sandbox=config.sandbox
        )

def create_notebook(name, token):
    noteStore = get_client(token=token).get_note_store()
    notebook = Types.Notebook()
    notebook.name = name
    # @Todo Handle Error "Notebook already taken"
    createdNotebook = noteStore.createNotebook(notebook)
    uid = createdNotebook.guid
    return uid

def get_notebook(name, token):
    noteStore = get_client(token=token).get_note_store()
    notebooks = noteStore.listNotebooks()
    for nb in notebooks:
        if nb.name == name:
            return nb
    raise NoteNotFoundError


def create_note_with_notebook(title, content, uid, token):
    client = get_client(token=token)
    noteStore = client.get_note_store()
    note = Types.Note()
    note.title = title
    note.notebookGuid = uid
    note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>'+ content + '</en-note>'
    try:
        return noteStore.createNote(note)
    # This error may happen if the url is malformed or has not been xml-sanitized.
    except EDAMUserException as e:
        raise


def create_note(title, content, token):
    client = get_client(token=token)
    noteStore = client.get_note_store()
    note = Types.Note()
    note.title = title
    note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>'+ content + '</en-note>'
    try:
        return noteStore.createNote(note)
    # This error may happen if the url is malformed or has not been xml-sanitized.
    except EDAMUserException as e:
        raise

