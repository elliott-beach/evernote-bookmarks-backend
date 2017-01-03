from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types

import config


client = EvernoteClient(token=config.dev_token)
userStore = client.get_user_store()
noteStore = client.get_note_store()

def createNote(title, content):
    note = Types.Note()
    note.title = title
    note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>'+ content + '</en-note>'
    return noteStore.createNote(note)