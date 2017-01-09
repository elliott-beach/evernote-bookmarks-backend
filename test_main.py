import requests
import os

port = int(os.environ.get('PORT', 5000))
HOST = 'http://localhost:%d' % port

### e2e ###
def test_create():
	response = requests.post(HOST+'/create', data={
		'title': 'title',
		'content': 'some example content'
	})
	assert response.status_code == 200
