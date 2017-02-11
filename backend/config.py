from os import environ as environment


consumer_key = environment['consumer_key']
consumer_secret = environment['consumer_secret']
secret_key = environment['secret_key']

ALLOWED_ORIGIN = environment['origin']

if environment['sandbox'] == "True":
    sandbox = True
elif environment['sandbox'] == "False":
    sandbox = False
else:
   raise EnvironmentError("Sandbox must be either True or False")

port = int(environment.get('PORT', 5000))
dev_token = environment.get('dev_token', None)