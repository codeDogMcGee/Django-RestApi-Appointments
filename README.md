# Django-REST API-Appointments

## REST API using Django Rest Framework. 
This project will be used as the boilerplate for a custom appointments web app for a nail salon in Denver, Colorado.

### __Endpoints__
Admin Only Endpoints:
```
settings/
users/
users/<str:group_name>/   # POST here to create a user
```

Authenticated users can only GET, PUT, and DELETE their own profile:
```
user/<int:pk>/
```

Appointments endpoints, accessable by authenticated users:
```
appointments/
appointments/<int:pk>/
past-appointments/
past-appointments/<int:pk>/
```

Other:
```
groups/
```

### __Create a Django environment__
```
python -m venv venv
venv\venv\activate.bat
(venv) pip install -r requirements.txt
```
To activate the Python on Linux:
```
source venv/venv/activate
```
### __Build the project__
```
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser
```

### __Run the server__
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


### __Django Website Front-End__
Django website that connects to the appointments API and lets users view and make appointments (This is being replaced with a React front-end). 
![Make appointment](images/make_appointment.PNG)
![View appointments](images/user_appointments.PNG)