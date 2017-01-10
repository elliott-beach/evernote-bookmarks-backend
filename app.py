import os
import config
from flask import Flask, request, session, redirect
from flask_cors import cross_origin

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
    client = evernote.get_client()
    request_token = client.get_request_token(callbackUrl)
    # Save the request token information for later
    session['oauth_token'] = request_token['oauth_token']
    session['oauth_token_secret'] = request_token['oauth_token_secret']
    # Redirect the user to the Evernote authorization URL
    return redirect(client.get_authorize_url(request_token))

@app.route('/auth_callback')
def callback():
    try:
        client = evernote.get_client()
        access_token = client.get_access_token(
            session['oauth_token'],
            session['oauth_token_secret'],
            # The oauth_verifier will == None if user declined to authorize.
            request.args.get('oauth_verifier', '')
        )
    except KeyError:
        return redirect('/')
    session['access_token'] = access_token
    return redirect('/')

### <\Authentication> ###

@app.route('/create', methods=['POST'])
@cross_origin(origin=config.ALLOWED_ORIGIN)
def create():
    token = session.get('access_token')
    if not token:
        return 'Access Denied', 400
    title = request.form.get('title').encode('utf-8')
    content = request.form.get('content').encode('utf-8')
    note = evernote.create_note(title, content, token)
    return str(note)

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(port=port)
