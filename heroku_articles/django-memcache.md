
Memcache is a technology that helps web apps and mobile app backends
in two main ways: *performance* and *scalability*. You should consider
using memcache when your pages are loading too slowly or your app is
having scalability issues. Even for small sites it can be a great
technology, making page loads snappy and future proofing for scale.

This article shows how to create a simple application in Django,
deploy it to Heroku, then add caching with Memcache to alleviate a
performance bottleneck.

This article mainly targets *Python 3* since *Django 2* no longer supports
*Python 2*. If you want to use Python 2 with an older version of Django this
guide should however still work.

>note
>We’ve built a sample app that can be seen running
>[here](http://memcachier-examples-django2.herokuapp.com).<br>
><a class="github-source-code" href="http://github.com/memcachier/examples-django2">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-django2)

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
explanation of these commands can be found in
[Deploying Python and Django Apps](deploying-python).

```term
$ mkdir django_queue && cd django_queue
$ python -m venv venv    # For Python 2 use `virtualenv venv`
$ source venv/bin/activate
$ pip install Django django-heroku gunicorn
$ django-admin.py startproject django_queue .
$ pip freeze > requirements.txt
$ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).

Django version 2.0, using settings 'django_queue.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Visiting [http://localhost:8000](http://localhost:8000) will show a
"hello, world" landing page.

### The Procfile

The [Procfile](procfile) lets Heroku know how to start your app. Create it in
your project root and and add the following line:

```text
web: gunicorn django_queue.wsgi --log-file -
```

### Configure Django for Heroku

Django requires some special configuration in order to work on Heroku, mainly
for the database to work and the static files to be served. Luckily, there is a
[`django-heroku`](https://github.com/heroku/django-heroku) package that takes care
of all that. So on the bottom of the file `django_queue/settings.py` add the
following lines:

```python
# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())
```

For more information about these Heroku specific settings see
[Configuring Django Apps for Heroku](django-app-configuration). *Note:
`django-heroku` only supports Python 3. For Python 2 please follow the
instructions in [Configuring Django Apps for Heroku](django-app-configuration)*

### Commit to git

Code needs to be added to a git repository before it can be deployed
to Heroku. First, edit `.gitignore` and adding the following
lines to exclude unnecessary files:

```text
venv
*.pyc
db.sqlite3
```

Then initialize a repo and make a commit:

```term
$ git init
$ git add .
$ git commit -m "Empty django app"
```

### Deploy to Heroku

Create an app using `heroku create`:

```term
$ heroku create
Creating app... done, ⬢ blooming-ridge-97247
https://blooming-ridge-97247.herokuapp.com/ | https://git.heroku.com/blooming-ridge-97247.git
```

And then deploy the app:

```term
$ git push heroku master
```

Finally, you can use the Heroku CLI to view the app in your browser:

```term
$ heroku open
```

You will see the same "hello, world" landing page you saw in local
development mode except running on the Heroku platform.

## Add functionality

The Django application we are building will show a list of items, one
per line on the page. It will have actions to add new items to the end
and remove older items from the front. Basically, it is a queue. Items
in the queue are just strings.

First, make the Django `mc_queue` app:

```term
$ python manage.py startapp mc_queue
```

Add `mc_queue` to the list of installed apps in
[`django_queue/settings.py`](https://github.com/memcachier/examples-django2/blob/master/django_queue/settings.py):

```python
INSTALLED_APPS = (
  'django.contrib.auth',
  # ...
  'mc_queue',
)
```

And create a simple model in
[`mc_queue/models.py`](https://github.com/memcachier/examples-django2/blob/master/queue/models.py):

```python
from django.db import models

class QueueItem(models.Model):
  text = models.CharField(max_length=200)
```

Use `makemigrations` and `migrate` to create the `mc_queue_queueitems` table
locally, along with all other default Django tables:

```term
$ python manage.py makemigrations mc_queue
$ python manage.py migrate
```

Next, setup routes in
[`django_queue/urls.py`](https://github.com/memcachier/examples-django2/blob/master/django_queue/urls.py)
for add, remove, and index methods:

```python
# ...
from mc_queue import views
urlpatterns = [
    # ...
    path('add', views.add),
    path('remove', views.remove),
    path('', views.index),
]
```

Add corresponding views in
[`mc_queue/views.py`](https://github.com/memcachier/examples-django2/blob/master/queue/views.py):

```python
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from mc_queue.models import QueueItem

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
```

And create a template, `mc_queue/templates/index.html`, that has display code.
View the source for this file in
[Github](https://github.com/memcachier/examples-django2/blob/master/mc_queue/templates/index.html). Django will automatically check each apps `templates` folder for templates.

```term
$ mkdir mc_queue/templates
$ wget -O mc_queue/templates/index.html https://raw.githubusercontent.com/memcachier/examples-django2/master/mc_queue/templates/index.html
```

Execute `python manage.py runserver` and visit `http://localhost:8000` again
and play with the basic queue app. A screenshot has been included below:

![Simple Queue App](https://s3.amazonaws.com/heroku-devcenter-files/article-images/1445331522-queue.png 'App Screenshot')

### Commit your changes

When the app is working, commit your changes:

```term
$ git add .
$ git commit -m "Basic queue app"
```

### Deploy to Heroku

And deploy these changes to Heroku:

```term
$ git push heroku master
```

Finally, migrate your database on Heroku to create the `mc_queue_queueitem`
table, and restart the Heroku app:

```term
$ heroku run python manage.py makemigrations mc_queue
$ heroku run python manage.py migrate
$ heroku restart
```

View the app in your browser:

```term
$ heroku open
```

## Start using memcache

As previously mentioned, memcache is most effective at caching
expensive database queries and HTML renders.  The only potentially
expensive operation in the queue app is the `SELECT` statement made to
the database to fetch the queue.  This example will continue by using
memcache to cache the `SELECT` statement.

### Provision on Heroku

Provision the [MemCachier](https://elements.heroku.com/addons/memcachier)
add-on to use in the application deployed to Heroku:

```term
$ heroku addons:create memcachier:dev
```

This will provision a new memcache instance for you and expose a set
of [config vars](config-vars) containing your memcache credentials.

### Configure Django with MemCachier

> callout
> As of Django 1.11 we can use its native `pylibmc` backend. For older versions
> of Django you will need to install `django-pylibmc`. See an
> [older version](https://github.com/memcachier/docs/blob/8a9437cc2285d034b8fe2c3e38423489be32ce17/heroku_articles/django-memcache.md#start-using-memcache)
> of this article for more information.

To have your application operate correctly in both development and
production mode, add the following to `django_queue/settings.py`:

```python
def get_cache():
  import os
  try:
    servers = os.environ['MEMCACHIER_SERVERS']
    username = os.environ['MEMCACHIER_USERNAME']
    password = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        # TIMEOUT is not the connection timeout! It's the default expiration
        # timeout that should be applied to keys! Setting it to `None`
        # disables expiration.
        'TIMEOUT': None,
        'LOCATION': servers,
        'OPTIONS': {
          'binary': True,
          'username': username,
          'password': password,
          'behaviors': {
            # Enable faster IO
            'no_block': True,
            'tcp_nodelay': True,
            # Keep connection alive
            'tcp_keepalive': True,
            # Timeout settings
            'connect_timeout': 2000, # ms
            'send_timeout': 750 * 1000, # us
            'receive_timeout': 750 * 1000, # us
            '_poll_timeout': 2000, # ms
            # Better failover
            'ketama': True,
            'remove_failed': 1,
            'retry_timeout': 2,
            'dead_timeout': 30,
          }
        }
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()
```

This change to `settings.py` configures the cache for both development
and production.  If the `MEMCACHIER_*` environment variables exist,
the cache will be setup with `pylibmc`, connecting to
MemCachier. Whereas, if the `MEMCACHIER_*` environment variables
don't exist -- hence development mode -- Django's simple in-memory
cache is used instead.

### Libraries

To install `pylibmc` the C library `libmemcached` is required. Heroku comes with
`libmemcached` installed so you wont need to worry about it. However, if you
want to test `pylibmc` locally you'll need to install it (which is a
platform-dependant process).

In Ubuntu:

```term
$ sudo apt-get install libmemcached-dev
```

We also have a detailed
[blog post](http://blog.memcachier.com/2014/11/05/ubuntu-libmemcached-and-sasl-support/)
on installing libmemcached on Ubuntu if you run into any issues.

In OS X:

```term
$ brew install libmemcached
```

> callout
> Libmemcached can be built with, or without, support for SASL
> authentication. SASL authentication is the mechanism your client
> uses to authenticate with MemCachier servers using a username and
> password we provide. You should confirm that your build of
> libmemcached supports SASL. To do this, please follow our
> [guide](http://blog.memcachier.com/2014/11/05/ubuntu-libmemcached-and-sasl-support/).

Then, install the `pylibmc` Python modules:

```term
$ pip install pylibmc
```

> callout
> If pylibmc installation is unable to find `libmemcached` you may need to
> specify it: `LIBMEMCACHED=/opt/local pip install pylibmc` if `libmemcached`
> was installed in `/opt/local`. Replace `/opt/local` with the correct
> directory if needed.

Update your `requirements.txt` file with the new dependencies (if you did not
install `pylibmc` locally, just add `pylibmc==1.5.2` to your
`requirements.txt`):

```term
$ pip freeze > requirements.txt
$ cat requirements.txt
...
pylibmc==1.5.2
```

Finally, commit and deploy these changes:

```term
$ git commit -a -m "Connecting to memcache."
$ git push heroku master
```

### Verify memcache config

Verify that you've configured memcache correctly before you move
forward.

To do this, run the Django shell. On your local machine run `python
manage.py shell` and in Heroku run `heroku run python manage.py
shell`.  Run a quick test to make sure your cache is configured
properly:

```python
>>> from django.core.cache import cache
>>> cache.get("foo")
>>> cache.set("foo", "bar")
>>> cache.get("foo")
'bar'
```

Exit with `ctrl-d`. After the second `get` command, `bar` should be printed to
the screen when `foo` is fetched from the cache. If you don't see `bar` your
cache is not configured correctly.

### Modify the application

With a proper connection to memcache, the queue database query code can
be modified to check the cache first.  Below is a new version of the
`index` view in `mc_queue/views.py`:

```python
# ...
from django.core.cache import cache
import time

QUEUE_KEY = "queue"

def index(request):
  queue = cache.get(QUEUE_KEY)
  if not queue:
    time.sleep(2)  # simulate a slow query.
    queue = QueueItem.objects.order_by("id")
    cache.set(QUEUE_KEY, queue)
  c = {'queue': queue}
  c.update(csrf(request))
  return render_to_response('index.html', c)
# ...
```

The above code first checks the cache to see if the `queue` key exists
in the cache.  If it does not, a database query is executed and the
cache is updated.  Subsequent pageloads will not need to perform the
database query.  The `time.sleep(2)` only exists to simulate a slow
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

```python
cache.set(QUEUE_KEY, queue, 5)
```

But this functionality isn't ideal.  The user experience associated
with adding and removing will be bad -- the user should not need to
wait a few seconds for their queue to be updated.  Instead, a better
strategy is to invalidate the `queue` key when you know the cache is
out of date -- namely, to modify the `add` and `remove` views to
delete the `queue` key.  Below are the new methods:

```python
# ...
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
```

Note the calls to `cache.delete`.  This function explicitly deletes
the `queue` key from the cache.

Better yet, instead of deleting the `queue` key, the value should be
updated to reflect the new queue.  Updating the value instead of
deleting it will allow the first pageload to avoid having to go to the
database.  Here's a better version of the same code:

```python
# ...
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
```

Now the cache will not ever be out-of-date, and the value associated
with the `queue` key will be updated immediately when the queue is
changed.

As usual, commit and deploy your changes:

```term
$ git commit -a -m "Using memcache in queue views."
$ git push heroku master
```

## Further reading and resources

This article has barely scratched the surface of what is possible with
memcache in Django.  For example, Django has built-in support to cache
[views](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-view-cache)
and
[fragments](https://docs.djangoproject.com/en/dev/topics/cache/#template-fragment-caching).
Furthermore, much of the basic Django setup was glossed over in this
article.  Please refer to the below resources to learn more about
Django, memcache, or Heroku:

* [MemCachier Add-on Page](https://elements.heroku.com/addons/memcachier)
* [MemCachier Documentation](https://devcenter.heroku.com/articles/memcachier)
* [Advance Memcache Usage](https://devcenter.heroku.com/articles/advanced-memcache)
* [Configuring Django Apps for Heroku](django-app-configuration)
* [The Django Tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/)
* [Django Caching Documentation](https://docs.djangoproject.com/en/dev/topics/cache/)
