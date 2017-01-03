from flask import Flask, request

import _evernote as evernote

app = Flask(__name__)

@app.route('/create')
def create():
    title = request.args.get('title')
    content = request.args.get('content')
    note = evernote.createNote(title, content)
    return str(note)

@app.route('/')
def index():
    res = "Evernote Note Creator!"
    return res

app.run(port=3000)


