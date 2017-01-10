import os
import config
from flask import Flask, request, session, redirect
from flask_cors import cross_origin


from evernote.api.client import EvernoteClient
def get_evernote_client(token=None):
    if token:
        return EvernoteClient(token=token, sandbox=True)
    else:
        return EvernoteClient(
            consumer_key=config.consumer_key,
            consumer_secret=config.consumer_secret,
            sandbox=True
        )

import _evernote as evernote

app = Flask(__name__)

# encrypt our sessions with the secret
app.secret_key = config.secret_key

@app.route('/')
def index():
    res = "Evernote Note Creator!"
    return res

### <Authentication> ###

@app.route('/auth')
def auth():
    callbackUrl = config.host + '/auth_callback'
    client = get_evernote_client()
    request_token = client.get_request_token(callbackUrl)
    # Save the request token information for later
    session['oauth_token'] = request_token['oauth_token']
    session['oauth_token_secret'] = request_token['oauth_token_secret']
    # Redirect the user to the Evernote authorization URL
    return redirect(client.get_authorize_url(request_token))

@app.route('/auth_callback')
def callback():
    try:
        client = get_evernote_client()
        client.get_access_token(
            session['oauth_token'],
            session['oauth_token_secret'],
            # The oauth_verifier will == None if user declined to authorize.
            request.args.get('oauth_verifier', '')
        )
    except KeyError:
        return redirect('/')
    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()
    return 'Notebooks: %s' % str(notebooks)

### <\Authentication> ###

@app.route('/create', methods=['POST'])
@cross_origin(origin=config.ALLOWED_ORIGIN)
def create():
    title = request.form.get('title').encode('utf-8')
    content = request.form.get('content').encode('utf-8')
    note = evernote.createNote(title, content)
    return str(note)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(port=port)
