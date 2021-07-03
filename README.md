# Django-REST API-Appointments

## REST API using Django Rest Framework
This project will be used as the boilerplate for a custom appointments web app for a nail salon in Denver, Colorado. A React front-end is under development and can be found [here](https://github.com/codeDogMcGee/React-Appointments).

### __Python Version__
Python 3.9.5

### __Database__
PostgreSQL 13

### __Environment__
Create a _.env_ file in the project's root directory with the following settings:
```
DATABASE_ENGINE=postgresql_psycopg2  # for postgres using psycopg2, or use django.db.backends.sqlite3
DATABASE_NAME=db_name
DATABASE_USER=username
DATABASE_PASSWORD=password
DATABASE_HOST=db  # if local, else some ip address for Amazon RDS, or other hosted DB
DATABASE_PORT=port

DJANGO_SECURITY_KEY=django_security_key
DJANGO_ALLOWED_HOSTS=*  # add a comma-seperated list of IP's for more security
DJANGO_LOGLEVEL=INFO

DJANGO_DEBUG_MODE=True
```

### __Build with Docker-Compose__
To build a development environment that uses a local PostgreSQL instance:
```
docker-compose -f docker-compose.yml build
```
Or, to build an instance that can run on an AWS EC2 instance using an RDS Postgres instance:
```
docker-compose -f docker-compose.aws.yml build
```
Then to run the container:
```
docker-compose -f docker-compose.yml up
```
Add a '-d' flag to run headless. Then use 'docker-compose -f docker-compose.yml down' to kill the process.

_Note: this will start a new project so you will need to shell into the Docker environment to initialize the database and setup a superuser upon first use. See __Build the Project__ section below._

### __Endpoints__
Admin Only Endpoints:
```
settings/
users/
users/<str:group_name>/   # POST here to create a user
```

To receive an API token, post valid login information to:
```
api-token-auth/
```

Authenticated users can only GET, PUT, and DELETE their own profile:
```
user/<int:pk>/
```
Authenticated users can also get their own profile without any additional information:
```
user/self/
```

Appointments endpoints, accessable by authenticated users:
```
appointments/
appointments/<int:pk>/
past-appointments/
past-appointments/<int:pk>/
```
Past appointments are read-only and are managed by api.utils.manage_appointments.py.

Management only endpoints:
```
schedules/
schedule/<int:pk>/
menu/
menu/<int:pk>/
```

Other:
```
groups/
```

### __Create a Local Django Environment__
```
python -m venv venv
venv\venv\activate.bat
(venv) pip install -r requirements.txt
```
To activate the Python on Linux:
```
source venv/venv/activate
```
### __Build the Project__
```
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser
```

### __Run the Server__
```
python manage.py runserver 8080
```

### __Authentication__
Token authentication is used, so users must have a token to be able to access the api. Tokens can be generated via command-line:
```
python manage.py drf_create_token username
```
A registered user can also request a token via the __api-token-auth/__ endpoint buy submitting a POST request like:
```
{
    "username": "username",
    "password": "password"
}
```

### __Groups__
For authentication purposes there are 3 user groups: __Customers__, __Employees__, and __Management__. When creating users with the _users/group_name/_ endpoint that user is automatically
added the group.


