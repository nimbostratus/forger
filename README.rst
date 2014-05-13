=============
Python Forger
=============

Python Forger is a tool to search and clone project patterns ("casts") for various
frameworks and libraries.

Requirements
============

Python Forge requires Python 2.7, it is not yet tested on 3.x

In order to clone git casts (which are most of the casts) Forger depends on an installed and running git client.

Installing Forger
=================

Install forger via pip::

    $ pip install forger
    or
    $ easy_install forger

Using Forger
============

Use the forger command to search for casts (a cast is a project template)::

    $ forger search flask

Display the details about a certain cast::

    $ forger show flask-minimal

Cloning a cast into a target directory::

    $ forger clone flask-minimal myshinyproject

A cast contains questions defining how your clone will look like. That questions may differ a lot between
casts, as they are part of the particular cast repository.


Creating a Cast
===============

A forger cast is a simple zip archive or git repository with an optional ```forger.json``` file.

The forger.json file
--------------------

If a file named ```forger.json``` exists the directory which contains that file is the cast root directory.
If no such file exists the repository or archive root is the cast root.

The ```forger.json``` file contains a JSON list of choices used by the cast setup. The example below shows
all possible combinations of choices::

    [
        {
            "name": "sqlalchemy",
            "question": "Include flask-sqlalchemy support?",
            "choices": ["Yes", "No"]
        },
        {
            "name": "projecttitle",
            "question": "Name of the website"
        }
    ]

Each object in the array is a single question the user will be asked. The order of the questions will be kept.
A question must consist of a *name* and a *question* entry, *choices* is optional. If *choices* exists only the
given choices will be accepted as user input.

The user input for each question will be stored in a context in a corresponding variable named *name* used to
process the cast files.

The cast files
--------------

All files in the cast repository or archive will be used for the newly generated project, with two exceptions.

1. The file ``forger.json`` will not be copied to the new project.
2. All files ending with ``.jinja`` will be processed by Jinja2 and may contain Jinja template syntax refering
   the variables defined in ``forger.json``

Each other file is copied as-is to the new project directory, its content will not be touched by forger.

Jinja2 Files
------------

Files ending with .jinja will be processed by Jinja and written to a new file with the same name, but without the
.jinja extension. A requirements.txt file which should be processed by Jinja has to be named ``requirements.txt.jinja``::

    Flask
    {% if sqlalchemy == "Yes" %}Flask-SQLAlchemy{% endif %}
