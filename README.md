# Bishasto
> The application is basically online service backend web application.


#### Setup

##### Dependencies

- Python 3.8.5
- Django 4.0.1
- Celery 5.2.3
- postgres  12.5

The following steps will walk you thru installation on a Mac. Linux should be similar. It's also possible to develop 
on a Windows machine, but I have not documented the steps. If you've developed django apps on Windows, you should have little problem getting up and running.


##### Create database
``
psql postgres
CREATE DATABASE bissasto
``

###### 1st open in your system terminal then follow the command line.

```bash
git clone https://github.com/mbrsagor/bishasto.git
cd bishasto
```

###### Then copy code from the ``env_example`` and create new file `.env` then pasts

-------------------------------------------
```bash
|--> env_example
|--> .env
```

Run the application in your local development server:

```bash
virtualenv venv --python=python3.8
source venv/bin/activate
pip install -r requirements.txt
./manage.py makemigrations user
./manage.py migrate user
./manage.py migrate
./ manage.py migrate django_celery_results
./manage.py createsuperuser
./mangae.py runserver
```

> Starting the worker process:
```bash
celery -A bishasto worker -l INFO
celery --help
```

## Happy coding :wink:
