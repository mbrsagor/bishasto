# taskManager
> Django Baceknd `task management` API based project.


### Setup

#### Dependencies

- Python 3.8.5
- Django 3.1.4
- postgres  12.5

The following steps will walk you thru installation on a Mac. Linux should be similar. It's also possible to develop 
on a Windows machine, but I have not documented the steps. If you've developed django apps on Windows, you should have little problem getting up and running.


##### Create database
``CREATE DATABASE taskmanager``

###### 1st open in your system terminal then follow the command line.

```bash
git clone https://github.com/mbrsagor/taskManager.git
cd taskManager
```

###### Then copy code from the ``env_example`` and create new file `.env` then pasts

Run the application in your local development server:

```bash
virtualenv venv --python=python3.8
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./mangae.py runserver
```

N:B: If any kid of `psql` connection fail you may follow the below command line.

```pip install psycopg2-binary```
