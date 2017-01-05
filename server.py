from flask import Flask, request
from xml.sax.saxutils import escape

import _evernote as evernote

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create():
    title = request.form.get('title').encode('utf-8')
    content = request.form.get('content').encode('utf-8')
    note = evernote.createNote(title, content)
    return str(note)

@app.route('/')
def index():
    res = "Evernote Note Creator!"
    return res

app.run(port=3000)

