from os import environ as environment

# @TODO set __dict__ = environ.__dict__
dev_token = environment['dev_token']
ALLOWED_ORIGIN = environment['origin']
consumer_key = environment['consumer_key']
consumer_secret = environment['consumer_secret']

host = 'http://localhost:5000'
secret_key = '@TODO'
