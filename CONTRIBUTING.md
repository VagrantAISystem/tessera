# Contributing

This document describes how to get Tessera up and running for development so
you can get hacking on Tessera.

## Dependencies

Tessera has a few dependencies:

1. Python Interpreter Ver 3+
2. pip and virtualenv
3. pytest
4. Docker and docker-compose

Installing python is platform / distribution specific so I'll just direct you
the excellent already written documentation
[here](https://wiki.python.org/moin/BeginnersGuide/Download)

Installing pip documentation can be found
[here](https://pip.pypa.io/en/stable/installing/)

*NOTE:* On some OS's like Ubuntu you will need to use the command pip3 instead
of pip

Install virtualenv: `pip install virtualenv`

Installing docker documentation can be found
[here](https://www.docker.com/products/overview) note that this dependency is
optional and I will document how to get Tessera up and running without docker
as well in case you do not want to install it.

Install docker-compose: `pip install docker-compose`

### Dependencies (Without Docker)

If not using Docker you need the following additional dependencies with links
to relevant install documentation:

1. [Postgres SQL Database](https://wiki.postgresql.org/wiki/Detailed_installation_guides)
2. [Redis](http://redis.io/topics/quickstart)
3. [RabbitMQ](https://www.rabbitmq.com/download.html)
4. [Celery](http://www.celeryproject.org/install/)

## Quick Start (With Docker)

If you're using docker and docker-compose you can start Tessera with one
command: `docker-compose up`

This will load the current source tree into a docker container running all the
dependencies pre wired up and will also live reload any python code changes!

By default this will listen on port 8080 so you can get a list of routes from
http://localhost:8080/api

A couple quick notes however:

1. Sometimes when starting for the first time docker-compose doesn't wait on
   dependencies correctly and the Tessera image will start before postgres has
   started building the database, simply restart the docker-compose image again
   and this should resolve the issue.
2. Any syntax errors (i.e. if you save often) will cause the app to completely
   crash which is normal behavior for the flask development server, simply
   restart the docker-compose image, I'm working on a fix for this using
   systemd but who knows when I'll get it done since this is a minor
   inconvenience.

You're ready to read the contribution guidelines [below](#guidelines)!

## Quick Start (Without Docker)

This guide will be more comprehensive and will give you a better idea of all
the technologies that Tessera is using.

Assuming that you have cloned Tessera and installed all the dependencies above
you now need to set up the virtualenv using the following command:

`virtualenv --python=/usr/bin/python3 venv`

Update the --python path so it points at your python3 installation depending on
your platform. Now activate the virtualenv using source:

`source venv/bin/activate`

Install the libraries Tessera needs to run use the following
command in the Tessera directory:

`pip install -r requirements.txt`

I'm going to assume you have started the services Redis, Postgres, and RabbitMQ
since these are all platform specific and well documented on the respective
websites.

Create the tessera database using the following command:

`psql -c "CREATE DATABASE tessera_dev;"`

Now you need to set up a few environment variables to configure TESSERA run the
following in your shell, I recommend creating a shell script you can source to
store this for later:

```bash
export TESSERA_DB_URL="postgres://username:password@localhost:5432/tessera_dev"
export TESSERA_REDIS_HOST="localhost"
export TESSERA_REDIS_PORT="6379"
export TESSERA_DEBUG="True"
```

Now start the celery worker, you'll want to do this in a different terminal or
fork it using the `&`:

`celery -A tessera.celery worker`

Once all that set up is in place you can finally start Tessera:

`python run.py`

This will start Tessera in development mode which will live reload your code
changes, one important note is that the flask development server will crash if
you have a syntax error when saving your file so you'll have to restart with
the above command if that happens.

You're ready to read the contribution guidelines [below](#guidelines)!

## Contribution Guidelines
<div id="guidelines"></div>

I'm going to reiterate this first since it's important. We have a [Code of
Conduct](https://github.com/chasinglogic/tessera/blob/master/code_of_conduct.md). 

Follow it.

1. Anything that can be unit tested should be. Anything that can not be unit
   tested should be integration tested.

   We use pytest for our tests and they are all placed in the tests directory.
   For any code you write make sure you add a test to the appropriate
   directory.

   To run the tests simply run `pytest tests/` and to filter to just your tests
   run `pytest -k name_of_my_test tests/`

2. May your commit messages be short and when they are not use the space below.
   A model commit message looks like this:

   ```
   Capitalized, short (50 chars or less) summary

   More detailed explanatory text, if necessary.  Wrap it to about 72
   characters or so.  In some contexts, the first line is treated as the
   subject of an email and the rest of the text as the body.  The blank
   line separating the summary from the body is critical (unless you omit
   the body entirely); tools like rebase can get confused if you run the
   two together.

   Write your commit message in the imperative: "Fix bug" and not "Fixed bug"
   or "Fixes bug."  This convention matches up with commit messages generated
   by commands like git merge and git revert.

   Further paragraphs come after blank lines.

   - Bullet points are okay, too

   - Typically a hyphen or asterisk is used for the bullet, followed by a
  single space, with blank lines in between, but conventions vary here

   - Use a hanging indent

   ```

3. Follow PEP8, but not religiously. We like the code to look nice and PEP8
   generally does that but you'll see a few areas where we break the 80 column
   and various other rules. Generally speaking stick to PEP8 unless it makes
   your code hard to read. Code is for humans not machines so exercise best
   judgement.

4. Your tests should pass. Travis is reporting build failures because a lot of
   our tests don't pass yet but YOUR tests should pass even if the rest of the
   suite does not.

5. We follow
   [git-flow](http://nvie.com/posts/a-successful-git-branching-model/) so
   please branch responsibly. All pull requests should be made against
   [Develop](https://github.com/chasinglogic/tessera/tree/develop)

6. If you add dependencies put them in the requirements.txt. If I pull down
   your branch and it fails to run because I can't install deps with
   requirements.txt I will not accept your pull request until resolved.

7. If you have a question, *ask*! We don't mind answering any questions you may
   have.

That's it! If you have any further questions or want some more real time
interaction we have a slack and if you'd like an invite you can send an email
to tesserafoss@gmail.com until we get the heroku thing set up!
