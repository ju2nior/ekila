### MNLV WEBSITE README

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com:MNLVM/ekila-website.git
    $ cd ekila-website

Activate the virtualenv for your project.

Install project dependencies:

    $ pip install -r requirements.txt

Update project depencies after dependent bot:
```
    $ pip install -r requirements.txt --update
```

Install pre-commit hook:
```
    $ pre-commit install
```

Create a file local_settings.py add your config there:
NB: Don't touch settings.py if not necessary, avoid push static files

Then simply apply the migrations:

    $ python manage.py migrate

You can now run the development server:

    $ python manage.py runserver

To discover app urls:

    $ python manage.py show_urls
