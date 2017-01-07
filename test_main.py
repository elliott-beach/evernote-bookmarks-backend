import requests
import os

from app import app

port = int(os.environ.get('PORT', 5000))
HOST = 'http://localhost:%d' % port

# start the server!
#app.run(port=port)

def test_create():
	response = requests.post(HOST+'/create', data={
		'title': 'title',
		'content': 'some example content'
	})
	assert response.status_code == 200
