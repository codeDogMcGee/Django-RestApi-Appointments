# Appointments-Django

###Python Version 3.9.5

This project will be used as the boilerplate for a production custom appointments app for a nail salon. It is split into
two pieces that will run independently in production, an api and a website.

### Website
Django website that lets a user make an appointment, or an employee change an appointment, etc.

### API
API using Django Rest Framework that interacts with the website and stores the data in a database. For debugging
Django's default SQLite is used as the db, but in production this will likely be some other SQL-like db like PostgreSQL.