# Bishasto
> The application is basically an online service backend web application like multi-vendor online service platform. Vendor will sell services or products, and the customer will taking the services or products.


#### Setup

##### Dependencies

- Python 3.8
- Celery 5.2.3
- postgres 12.5

The following steps will walk you through installation on a Mac. Linux should be similar. It's also possible to develop 
on a Windows machine, but I have not documented the steps. If you've developed Django apps on Windows, you should have little problem getting up and running.


##### Create database
``
psql -U postgres -W
CREATE DATABASE bissasto
``

###### 1st open in your system terminal, then follow the command line.

```bash
git clone https://github.com/mbrsagor/bishasto.git
cd bishasto
```

###### Then copy code from the ``env_example`` and create a new file `.env`, then paste

-------------------------------------------
```bash
|--> .env_example
|--> .env
```


#### Open PostgreSQL using terminal database:
```
psql -U postgres -W
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

> Django PayPal Payment Gateway Integration with Working Example:

[ Paypal Payment Gateway Integration](https://studygyaan.com/django/django-paypal-payment-gateway-integration-tutorial)

## Happy coding :wink:
