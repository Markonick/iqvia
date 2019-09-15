# iqvia
A simple Flask API with a Celery beat scheduler, dockerised


PREREQUISITES
-------------
i) Docker

ii) docker-compose

iii) pipenv

This solution can run in pipenv mode without celery/redis.

All you need to do is a

    pipenv shell

and then

    pip install -r requirements.txt
  
this should create an iqvia virtual environment to work within

TESTING
-------

To run the functional tests do

    pytest -v

FULL APP WITH CELERY BEAT
-------------------------

In order to run the celery tasks, we need to run 5 docker containers.

i) Flask backend

ii) Celery beat

iii) Celery worker

iv) Redis

v) Flower (task monitor)

To start the app, do a

    docker-compose up --build
    
This should kick-off all containers. You can observe the supported API endpoints at

    http://localhost:5000/
    
and the Flower monitor at 

    http://127.0.0.1:5555/tasks
    
