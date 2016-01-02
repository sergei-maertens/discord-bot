==================
Python Discord Bot
==================


This is a toy-project to create Discord_ bots in Python. It uses a plugin
structure to add custom behaviour, and under the hood it uses `Discord.py`_.

.. _Discord: https://discordapp.com/
.. _Discord.py: https://github.com/Rapptz/discord.py


Warning
=======

This is a toy project - so tests/documentation/support will be very sparse, if any.


Dependencies
============
In its current form, the bot has hard dependencies on `Discord.py`_ (``async`` branch) and ``Django``.

The first one is obvious, the latter is not. I wanted to use Django's ORM, and
possibly later the template engine. There is also a fair chance that a small
web interface will be built around (some of) the plugins. On top of that, Django
has some convenient helper functions to set-up logging and database abstraction.

Rather than re-inventing the wheel or using SQLAlchemies ORM and start-up
machinery, I picked familiarity and simplicity.


Usage
=====

It's probably easiest to fork or clone this repo to use it and add your own
plugins.

Start with installing the depdencies through ``pip``. If you don't know how to
do that, look up some tutorials that deal with ``virtualenv`` and ``pip``.

The project depends on some environment variables, mostly to avoid leaking
secrets to the big bad outside world:

* ``EMAIL``: the e-mail address to sign in with Discord
* ``PASSWORD``: the password to sign in with Discord (who would've guessed huh)
* ``DJANGO_SETTINGS_MODULE``: used to figure out which settings to load. Set to
  ``bot.settings`` or a custom settings file. Used by Django to be able to load
  the settings.
* ``SECRET_KEY``: required by Django. See https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-SECRET_KEY

Set these envvars in your shell, or in my case, they are added to the ``supervisord``
config file (see ``discord-bot.ini``).

Create the necessary database tables::

    $ python manage.py migrate

Start the bot by executing::

    $ python main.py

That's it.
