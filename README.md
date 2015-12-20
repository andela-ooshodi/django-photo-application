# Django Powered Photo Editor [![Build Status](https://travis-ci.org/andela-ooshodi/django-photo-application.svg)](https://travis-ci.org/andela-ooshodi/django-photo-application) [![Coverage Status](https://coveralls.io/repos/andela-ooshodi/django-photo-application/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-ooshodi/django-photo-application?branch=master)

### Challenge
Build an image editing app powered by Django

### Description
myPhotoApp is an image editing app allowing you to add different effects to your awesome image making it _"awesomer"_ 

### Getting Started
### Application Overview

##### Features
- Sign in with facebook
- Apply up to 5 effects to your image
- Share your images with your friends on facebook
- View all uploaded images on screens larger than 992px (Desktop)
- Responsive design

##### Technologies Used
- Language: Python
- Framework: Django
- Database: postgreSQL
- Social Authentication: python social auth
- Asynchronous rendering: AJAX
- Image filtering: Pillow
- Frontend framework: Materialize
- Frontend dependencies manager: Bower

## Installation
1. Clone the repository into a Virtual Environment. 
- Run `virtualenv <virtualenvname>` or `mkvirtualenv <virtualenvname>` if using virtualenv wrapper to create the virtual environment.
2. Install all the necessary requirements by running `pip install -r requirements.txt` within the virtual environment.
3. Configure your database configurations in a development.py and save in the settings folder
4. Create a .env.yml to hold all your environment variables, like your secret key, save in the same level as your README.md file (sample shown below)
5. Run `bower install` to install all front end dependencies. Please ensure you are on the same level with .bowerrc when you run this command
6. Run `python manage.py collectstatic` to copy all your static files into the staticfiles directory
7. Run `python manage.py makemigrations` and `python manage.py migrate` to create the necessary tables and everything required to run the application.
7. Run `python manage.py runserver` to run the app.
8. Run coverage `coverage run manage.py test` to know how much the app is covered by automated testing.
9. View the report of the coverage on your terminal `coverage report`.
10. Produce the html of coverage result `coverage html`.

## Sample .env.yml format
```
SECRET_KEY:
  "sample_key"
```

## myPhotoApp
Need to see the app for yourself?
[myPhotoApp](http://myphotoapplication.herokuapp.com)
