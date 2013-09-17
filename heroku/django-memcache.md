---
title: Scaling a Django Application with Memcache
id: 793
markdown_flavour: maruku


Memcache is a technology that helps web apps and mobile app backends
in two main ways: performance and scalability. You should consider
using memcache when your pages are loading too slowly or your app is
having scalability issues. Even for small sites it can be a great
technology, making page loads snappy and future proofing for scale.

This article shows how to create a simple application in Django,
deploy it to Heroku, then add caching with Memcache to alleviate a
performance bottleneck.

<div class="note" markdown="1">
The source code for this example is available [on
GitHub](https://github.com/memcachier/examples-django2) and can be
seen running at
[memcachier-examples-django2.herokuapp.com](http://memcachier-examples-django2.herokuapp.com).
</div>

## Overview

Memcache is an in-memory, distributed cache. The primary API for
interacting with it are `SET(key, value)` and `GET(key)` operations.
Memcache is like a hashmap (or dictionary) that is spread across
multiple servers, where operations are still performed in constant
time.

The most common usage of memcache is to cache expensive database
queries and HTML renders such that these expensive operations don’t
need to happen over and over again.

## Create an empty Django app

The following commands will create an empty Django app. A detailed
explanation of these commands can be found in the
[Django article](django).

    :::term
    $ mkdir django_queue && cd django_queue
    $ virtualenv venv --distribute
    $ source venv/bin/activate
    $ pip install Django psycopg2 dj-database-url
    $ django-admin.py startproject django_queue .
    $ pip freeze > requirements.txt
    $ python manage.py runserver
    Validating models...
    
    0 errors found
    Django version 1.4, using settings 'django_queue.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Visiting [http://localhost:8000](http://localhost:8000) will show a
"hello, world" landing page:

![Django Hello World](https://img.skitch.com/20120702-jp8um6diqaedf347rbeee28mga.jpg)

### Configure the database

Configure the application to use [Heroku's Postgres
database](heroku-postgresql). Edit the file, `django_queue/settings.py`
and replace the existing `DATABASES` setting with the following lines
instead:

    :::python
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

This will use PostgreSQL both on Heroku and on your local machine. If
you'd prefer to use SQLite locally for less setup, then you acn
instead put the follwing line in `django_queue/settings.py`:

    :::python
    # use sqlite for local development (when DATABASE_URL isn't
    # defined, as that is # what dj_database_url is looking for).
    curdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    sqlite_db = 'sqlite://localhost/' + curdir + '/../queue.sqlite'
    
    DATABASES = {'default': dj_database_url.config(default=sqlite_db)}

### Commit to git

Code needs to be added to a git repository before it can be deployed
to Heroku. First, edit `.gitignore` and adding the following
lines to exclude unnecessary files:

    :::term
    venv
    *.pyc

Then initialize a repo and make a commit:

    :::term
    $ git init
    $ git add .
    $ git commit -m "empty django app"

### Deploy to Heroku

Create an app using `heroku create`:

    :::term
    $ heroku create
    Creating empty-beach-6144... done, stack is cedar
    http://empty-beach-6144.herokuapp.com/ | git@heroku.com:empty-beach-6144.git
    Git remote heroku added

And then deploy the app:

    :::term
    $ git push heroku master

Finally, you can use the Heroku CLI to view the app in your browser:

    :::term
    $ heroku open

You will see the same "hello, world" landing page you saw in local
development mode except running on the Heroku platform.

## Add functionality

The Django application we are building will show a list of items, one
per line on the page. It will have actions to add new items to the end
and remove older items from the front. Basically, it is a queue. Items
in the queue are just strings.

First, make the Django `queue` app:

    :::term
    $ python manage.py startapp queue

Add `queue` to the list of installed apps in
[`django_queue/settings.py`](https://github.com/memcachier/examples-django2/blob/master/django_queue/settings.py):

    :::python
    INSTALLED_APPS = (
      'django.contrib.auth',
      # ...
      'queue',
    )

And create a simple model in
[`django_queue/queue/models.py`](https://github.com/memcachier/examples-django2/blob/master/queue/models.py):

    :::python
    from django.db import models
    
    class QueueItem(models.Model):
      text = models.CharField(max_length=200)

Use `syncdb` to create the `queue_queueitems` table locally, along with
all other default Django tables:

<p class="callout" markdown="1">You will be prompted to create a
superuser.  Respond with "no" and hit return.</p>

    :::term
    $ python manage.py syncdb

Next, setup routes in `django_queue/urls.py` for remove, add, and index
methods.  View the source in
[Github](https://github.com/memcachier/examples-django2/blob/master/django_queue/urls.py)
for `urls.py`.

Add corresponding views in
[`queue/views.py`](https://github.com/memcachier/examples-django2/blob/master/queue/views.py):

    :::python
    from django.http import HttpResponse
    from django.core.context_processors import csrf
    from django.shortcuts import render_to_response, redirect
    from queue.models import QueueItem
    
    def index(request):
      queue = QueueItem.objects.order_by("id")
      c = {'queue': queue}
      c.update(csrf(request))
      return render_to_response('index.html', c)
    
    def add(request):
      item = QueueItem(text=request.POST["text"])
      item.save()
      return HttpResponse("<li>%s</li>" % item.text)
    
    def remove(request):
      items = QueueItem.objects.order_by("id")[:1]
      if len(items) != 0:
        items[0].delete()
      return redirect("/")

And create a template, `templates/index.html`, that has display code.
View the source for this file in
[Github](https://github.com/memcachier/examples-django2/blob/master/templates/index.html).

Lastly, configure the `templates` directory in
`django_queue/settings.py`.  See `settings.py` in
[Github](https://github.com/memcachier/examples-django2/blob/master/django_queue/settings.py)
for an example `templates` setting.

Visit `http://localhost:8000` again and play with the basic queue app.
A screenshot has been included below:

![Simple Queue App](https://img.skitch.com/20120703-e1keudyecu3c2rwd8xmphahtyq.jpg)

### Commit your changes

When the app is working, commit your changes:

    :::term
    $ git add .
    $ git commit -m "Basic queue app"

### Deploy to Heroku

And deploy these changes to Heroku:

    :::term
    $ git push heroku master

Finally, sync your database on Heroku to create the `queue_queueitem`
table, and restart the Heroku app:

    :::term
    $ heroku run python manage.py syncdb
    $ heroku restart

View the app in your browser:

    :::term
    $ heroku open

## Start using memcache

As previously mentioned, memcache is most effective at caching
expensive database queries and HTML renders.  The only potentially
expensive operation in the queue app is the `SELECT` statement made to
the database to fetch the queue.  This example will continue by using
memcache to cache the `SELECT` statement.

### Provision on Heroku

Provision the [MemCachier](https://addons.heroku.com/memcachier)
add-on to use in the application deployed to Heroku:

    :::term
    $ heroku addons:add memcachier:dev

This will provision a new memcache instance for you and expose a set
of [config vars](config-vars) containing your memcache credentials.

### Configure Django with MemCachier

To have your application operate correctly in both development and
production mode, add the following to `django_queue/settings.py`:

    :::python
    def get_cache():
      import os
      try:
        os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
        os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
        os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
        return {
          'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'TIMEOUT': 500,
            'BINARY': True,
            'OPTIONS': { 'tcp_nodelay': True }
          }
        }
      except:
        return {
          'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
          }
        }
    
    CACHES = get_cache()

This change to `settings.py` configures the cache for both development
and production.  If the `MEMCACHIER_*` environment variables exist,
the cache will be setup with `django-pylibmc-sasl`, connecting to
MemCachier. Whereas, if the `MEMCACHIER_*` environment variables
don't exist -- hence development mode -- Django's simple in-memory
cache is used instead.

Next, you need to modify your `requirements.txt` file to include
`django-pylibmc-sasl`.

### Libraries

As `libmemcached` is required to install django-pylibmc-sasl you'll
need to install it locally (which is a platform-dependant process).

In Ubuntu:

    :::term
    $ sudo apt-get install libmemcached-dev

In OS X:

    :::term
    $ brew install libmemcached

Then, install the `django-pylibmc-sasl` Python modules:

<div class="callout" markdown="1">`/opt/local` may not be where
libmemcached was installed.  Replace `/opt/local` with the correct
directory if needed.</div>

    :::term
    $ LIBMEMCACHED=/opt/local pip install pylibmc
    $ pip install django-pylibmc-sasl

Update your `requirements.txt` file with the new dependencies:

    :::term
    $ pip freeze > requirements.txt
    $ cat requirements.txt
    ...
    pylibmc==1.2.3
    django-pylibmc-sasl==0.2.4

Finally, commit and deploy these changes:

    :::term
    $ git commit -a -m "Connecting to memcache."
    $ git push heroku master

### Verify memcache config

Verify that you've configured memcache correctly before you move
forward.

To do this, run the Django shell.  On your local machine run `python
manage.py shell` and in Heroku run `heroku run python manage.py
shell`.  Run a quick test to make sure your cache is configured
properly:

    :::python
    >>> from django.core.cache import cache
    >>> cache.get("foo")
    >>> cache.set("foo", "bar")
    True
    >>> cache.get("foo")
    'bar'

`bar` should be printed to the screen when `foo` is fetched from the
cache.  If you don't see `bar` your cache is not configured correctly.

### Modify the application

With a proper connection to memcache, the queue database query code can
be modified to check the cache first.  Below is a new version of the
`index` view in `django_queue/queue/views.py`:

    :::python
    from django.core.cache import cache
    from django.core.context_processors import csrf
    import time
    
    QUEUE_KEY = "queue"
    
    def index(request):
      queue = cache.get(QUEUE_KEY)
      if not queue:
        time.sleep(2) # simulate a slow query.
        queue = QueueItem.objects.order_by("id")
        cache.set(QUEUE_KEY, queue)
      c = {'queue': queue}
      c.update(csrf(request))
      return render_to_response('index.html', c)

The above code first checks the cache to see if the `queue` key exists
in the cache.  If it does not, a database query is executed and the
cache is updated.  Subsequent pageloads will not need to perform the
database query.  The `time.sleep(2)` queue exists to simulate a slow
query.

You may notice that there's a bug in this code.  Visit
`http://localhost:8000`.  Notice that adding a new item to the queue
properly appends the new item to the `<ul>`.  However, if you refresh
the page, you'll notice that the queue is out of date.  The queue is out
of date because the memcache value hasn't been updated yet.

### Keep memcache up-to-date

There are many techniques for dealing with an out-of-date cache.
First and easiest, the `cache.set` method can take an optional third
argument, which is the time in seconds that the cache key should stay
in the cache.  If this option is not specified, the default `TIMEOUT`
value in `settings.py` will be used instead.

You could modify the `cache.set` method to look like this:

    :::python
    cache.set(QUEUE_KEY, queue, 5)

But this functionality isn't ideal.  The user experience associated
with adding and removing will be bad -- the user should not need to
wait a few seconds for their queue to be updated.  Instead, a better
strategy is to invalidate the `queue` key when you know the cache is
out of date -- namely, to modify the `add` and `remove` views to
delete the `queue` key.  Below are the new methods:

    :::python
    def add(request):
      item = QueueItem(text=request.POST["text"])
      item.save()
      cache.delete(QUEUE_KEY)
      return HttpResponse("<li>%s</li>" % item.text)
    
    def remove(request):
      items = QueueItem.objects.order_by("id")[:1]
      if len(items) != 0:
        items[0].delete()
        cache.delete(QUEUE_KEY)
      return redirect("/")

Note the calls to `cache.delete`.  This function explicitly deletes
the `queue` key from the cache.

Better yet, instead of deleting the `queue` key, the value should be
updated to reflect the new queue.  Updating the value instead of
deleting it will allow the first pageload to avoid having to go to the
database.  Here's a better version of the same code:

    :::python
    def add(request):
      item = QueueItem(text=request.POST["text"])
      item.save()
      cache.set(QUEUE_KEY, _get_queue())
      return HttpResponse("<li>%s</li>" % item.text)
    
    def remove(request):
      items = QueueItem.objects.order_by("id")[:1]
      if len(items) != 0:
        items[0].delete()
        cache.set(QUEUE_KEY, _get_queue())
      return redirect("/")
      
    def _get_queue():
      return QueueItem.objects.order_by("id")

Now the cache will not ever be out-of-date, and the value associated
with the `queue` key will be updated immediately when the queue is
changed.

As usual, commit and deploy your changes:

    :::term
    $ git commit -a -m "Using memcache in queue views."
    $ git push heroku master

## Further reading and resources

This article has barely scratched the surface of what is possible with
memcache in Django.  For example, Django has built-in support to cache
[views](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-view-cache)
and
[fragments](https://docs.djangoproject.com/en/dev/topics/cache/#template-fragment-caching).
Furthermore, much of the basic Django setup was glossed over in this
article.  Please refer to the below resources to learn more about
Django, memcache, or Heroku:

* [MemCachier Add-on Page](https://addons.heroku.com/memcachier)
* [MemCachier Documentation](https://devcenter.heroku.com/articles/memcachier)
* [Advance Memcache Usage](https://devcenter.heroku.com/articles/advanced-memcache)
* [Getting Started with Django in Heroku](https://devcenter.heroku.com/articles/django)
* [The Django Tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/)
* [Django Caching Documentation](https://docs.djangoproject.com/en/dev/topics/cache/)

