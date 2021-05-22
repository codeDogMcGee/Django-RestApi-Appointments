# Appointments-Django

###Python Version 3.9.5

This project will be used as the boilerplate for a production custom appointments app for a nail salon. It is split into
two pieces that will run independently in production, an api and a website.

### API
REST API using Django Rest Framework that interacts with the website using JSON serialized models and stores the data in a database. 
While debugging Django's default database SQLite is used. In production this will likely be some other SQL-like db like SQL or PostgreSQL.

### Website
Django website that lets a user make an appointment, or an employee change an appointment, etc. (not yet created)