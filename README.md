# kanban Application



To run the Project :
### Setup Backend

`cd backend`

Creating Python virtual environment
`python3 -m venv .env`

Activating the environment
`source .env/bin/activate`

Install all the requirements .
`pip install -r requirements.txt` 

To run the flask application, use
`python3 main.py`

Start celery
`sh local_workers.sh`

Start celery beat
`sh local_beat.sh`

start mailhog
`mailhog`

### Setup frontend

`cd frontend`

npm install


start vue cli
`vue serve` or `npm run serve`

------------------------------------------------------------------------------------------------------------


### Redis Setup

Install redis server globally - `brew install redis`

run redis server - `brew services start redis`

check server is running `redis-cli ping` ans with PONG

stop redis server - `brew services stop redis`