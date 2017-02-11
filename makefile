py = python/bin/python2
pyt = python/bin/pytest
quit = pkill python
env = env $$(cat .env | xargs)


start:
	$(env) $(py) backend/app.py &


test: start
	$(env) $(pyt) tests
	$(quit)


test-slow: start
	$(env) $(pyt) --runslow tests
	$(quit)
