from os import environ as environment

dev_token = environment['dev_token']
consumer_key = environment['consumer_key']
consumer_secret = environment['consumer_secret']
secret_key = environment['secret_key']

ALLOWED_ORIGIN = environment['origin']
sandbox = False
