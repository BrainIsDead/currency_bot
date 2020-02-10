# currency_bot
## Installation

This project requires Python 3.7 and Django 2.2.8

The recommended way to install this project is to use Pipenv. The included Pipfile will set up a virtual environment with Python 3.7.x and Django 2.2.8

```$ pipenv shell```

```$ pipenv install```

Alternatively you can use the provided requirements.txt file to install Django with pip.

```pip install -r requirements.txt```

Then we have to create a database by running the migrations. By default, the project uses a file-based SQLite database. Change into the directory mysite and use the migrate management command.

```$ cd src```

```$ python manage.py migrate```

Now you are ready to start the application:

```$ python manage.py runserver```

## Setup 

```settings.py``` already exists bot TOKEN, but you can change it to yours

## Bot information

#### Url:

http://t.me/TestCurrencyBot

#### Token to access the HTTP API:

1035111087:AAGVZ0pvnck_rivetrgvGcKYFgW5g4hP6iU
