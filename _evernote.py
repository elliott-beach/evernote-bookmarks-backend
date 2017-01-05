from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from evernote.edam.error.ttypes import EDAMUserException

import config


client = EvernoteClient(token=config.dev_token)
userStore = client.get_user_store()
noteStore = client.get_note_store()

def createNote(title, content):
    note = Types.Note()
    note.title = title
    note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>'+ content + '</en-note>'
    print content
    try:
        return noteStore.createNote(note)
    except EDAMUserException as e:
        raise

# test
if __name__ == "__main__":
    title = "test"
    #content = '<a href="https://console.aws.amazon.com/s3/home?region=us-west-2#&bucket=big-bucket-of-fun&prefix=">'
    content='<a href="https://url.with.ampersand/foo?boof&amp;bar">FooBar</a>'
    createNote(title, content)

