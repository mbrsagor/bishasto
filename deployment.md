# Bishasto deployment

> Bishasto webapp deployment VPS on staging or production server without CI/CD and Docker container.

##### Please follow the below instructions:

###### Install the Packages from the Ubuntu Repositories
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
sudo apt install python3-virtualenv
```

###### Create the PostgreSQL Database and User
```bash
sudo -u postgres psql
```

```postgresql
CREATE DATABASE bishasto;
CREATE USER dev WITH PASSWORD '12345';
ALTER ROLE dev SET client_encoding TO 'utf8';
ALTER ROLE dev SET default_transaction_isolation TO 'read committed';
ALTER ROLE dev SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE bishasto TO dev;
\q
```

###### Create a Python Virtual Environment & run project
```bash
git clone https://github.com/mbrsagor/bishasto.git
cd bishasto
virtualenv venv --python=python3.8
source venv/bin/activate
pip install -r requirements.txt
```

##### If not install gunicorn
```bash
pip install django gunicorn
```

###### Configuration settings.py file:
```.dotenv
SECRET_KEY='django-insecure-%4#+g@c%hi=7&)x&c*tu6n)nbpgg%31!y95x2aa@q!$y+v(_%7'
DEBUG=True
ALLOWED_HOSTS='127.0.0.1:8000'

# Database config
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bishasto
DB_USERNAME=sagor
DB_PASSWORD=12345
```


###### Complete Initial Project Setup

```bash
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py collectstatic
sudo ufw allow 8000
```

###### Testing Gunicorn’s Ability to Serve the Project.
````bash
cd Dailydi
gunicorn --bind 0.0.0.0:8000 bishasto.wsgi
````
###### Deactivated virtualenv
```bash
deactivate
```

#### Create a Gunicorn systemd Service File
````bash
sudo nano /etc/systemd/system/gunicorn.service
````
```bash
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/bishasto
ExecStart=/home/ubuntu/bishasto/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/bishasto/bishasto.sock DailyDi.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

###### Check for the Gunicorn Socket File
````bash
sudo systemctl status gunicorn
````

Next, check for the existence of the bishasto.sock file within your project directory:
````bash
ls
````

If the systemctl status command indicated that an error occurred or if you do not find the bishasto.sock file in the directory, it’s an indication that Gunicorn was not able to start correctly. Check the Gunicorn process logs by typing:
````bash
sudo journalctl -u gunicorn
````

If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process by typing:

````bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
````

###### Configure Nginx to Proxy Pass to Gunicorn
```bash
sudo nano /etc/nginx/sites-available/bishasto
```
````nginx configuration
server {
    listen 80;
    server_name 54.193.166.128;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/bishasto;
    }

    location /media/ {
        root /home/ubuntu/bishasto;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/bishasto/bishasto.sock;
    }
}
````

```bash
sudo ln -s /etc/nginx/sites-available/bishasto /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```
##### Troubleshooting Nginx and Gunicorn:
```bash
sudo tail -F /var/log/nginx/error.log
```

> https://medium.com/@mudasirhaji/set-up-a-cicd-pipeline-using-jenkinsfile-and-docker-on-aws-ec2-555eb56d50c2