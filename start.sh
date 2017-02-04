source python/bin/activate
export $(cat .env | xargs)
python app.py &
