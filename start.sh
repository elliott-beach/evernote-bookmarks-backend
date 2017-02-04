source python/bin/activate
export $(cat .env | xargs)
python backend/app.py &
