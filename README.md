# Tele Consult Dr API Backend 

API server that serves necessary data to the functionalities of the tele consult dr project

### Postgres DB Setup

```
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql

# During the Postgres installation, an operating system user named postgres was created to correspond to the postgres PostgreSQL administrative user. We need to change to this user to perform administrative tasks
sudo su - postgres

# You should now be in a shell session for the postgres user. Log into a Postgres session by typing
psql

# Create database and user
CREATE DATABASE doctor_app;
CREATE USER doctor_app_user WITH PASSWORD 'DoctorAppBackendDatabase1@';

# Setting encodings to UTF-8, timezones and transaction isolations
ALTER ROLE doctor_app_user SET client_encoding TO 'utf8';
ALTER ROLE doctor_app_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE doctor_app_user SET timezone TO 'UTC';

# Grant all permissions for the created user
GRANT ALL PRIVILEGES ON DATABASE doctor_app TO doctor_app_user;

# Exit
\q
exit
```

### Project Setup

```
sudo apt-get update
sudo apt-get install python3-dev git
sudo apt-get install build-essential libssl-dev libffi-dev
sudo apt-get install libjpeg-dev libfreetype6-dev zlib1g-dev
sudo apt-get install virtualenv
sudo apt-get install --upgrade pip

cd doctor-app-backend
virtualenv --python=python3.8 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Django Migrations

```bash
python manage.py migrate
```

### Create Django Superuser

```bash
python manage.py createsuperuser 
```

### Run Django app
```bash
python manage.py runserver 
```

NOTE: A user logging into the app is treated as a patient and all the doctors are added through admin site for now.
### Chekout the app in : https://play.google.com/store/apps/details?id=com.teleconsultdr.dr_kirans_ortho

