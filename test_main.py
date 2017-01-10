import requests
import config
import os

port = int(os.environ.get('PORT', 5000))
HOST = 'http://localhost:%d' % port

def test_create_access():
	response = requests.post(HOST+'/create', data={
		'title': 'title',
		'content': 'some example content'
	})
	assert response.status_code == 400
