Memcache is a technology that improves the performance and scalability of web
apps and mobile app backends. You should consider
using Memcache when your pages are loading too slowly or your app is
having scalability issues. Even for small sites, Memcache can make page loads
snappy and help future-proof your app.

This guide shows how to create a simple
[Django 2.1](https://www.djangoproject.com/) application, deploy it to Heroku,
then add Memcache to alleviate a performance bottleneck.

This article mainly targets _Python 3_ since _Django 2+_ no longer supports
_Python 2_. If you want to use Python 2 with an older version of Django this
guide should however still work.

> note
> The sample app in this guide can be seen running
> [here](https://memcachier-django-tasklist.herokuapp.com/). You can
> [view the source code](http://github.com/memcachier/examples-django-tasklist) or deploy
> it with this Heroku Button:
>
> [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-django-tasklist)

## Prerequisites

Before you complete the steps in this guide, make sure you have all of the
following:

- Familiarity with Python (and ideally Django)
- A Heroku user account ([signup is free and instant](https://signup.heroku.com/signup/dc))
- Familiarity with the steps in [Getting Started with Python on Heroku](getting-started-with-python)
- Python and the [Heroku CLI](heroku-cli) installed on your computer

## Create a Django application for Heroku

The following commands will create an empty Django app. A detailed
explanation of these commands can be found in
[Deploying Python and Django Apps](deploying-python).

```term
$ mkdir django_memcache && cd django_memcache
$ python -m venv venv    # For Python 2 use `virtualenv venv`
$ source venv/bin/activate
(venv) $ pip install Django django-on-heroku gunicorn
(venv) $ django-admin.py startproject django_tasklist .
(venv) $ pip freeze > requirements.txt
(venv) $ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).

Django version 2.0, using settings 'django_tasklist.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Visiting [http://localhost:8000](http://localhost:8000) will show a
"hello, world" landing page.

### Configure Django for Heroku

For the Django app to work on Heroku, some Heroku specific configuration is
required:

1. Add a [`Procfile`](procfile) to let Heroku know how to start your app:

   ```term
   $ echo "web: gunicorn django_tasklist.wsgi --log-file -" > Procfile
   ```

2. Add the Heroku specific configuration to the settings which the Django app
   requires in order to work on Heroku, mainly for the database to work and
   the static files to be served. Luckily, there is a
   [`django-on-heroku`](https://github.com/pkrefta/django-on-heroku) package that
   takes care of all that. So on the bottom of the file
   `django_tasklist/settings.py` add the following lines:

   ```python
   # Configure Django App for Heroku.
   import django_heroku
   django_heroku.settings(locals())
   ```

   For more information about these Heroku specific settings see
   [Configuring Django Apps for Heroku](django-app-configuration). _Note:
   `django-on-heroku` only supports Python 3. For Python 2 please follow the
   instructions in [Configuring Django Apps for Heroku](django-app-configuration)._

### Deploy on Heroku

Our code needs to be added to a git repository before it can be deployed
to Heroku. First, edit `.gitignore` and adding the following
lines to exclude unnecessary files:

```text
venv
*.pyc
db.sqlite3
```

Then initialize a git repository and make a commit:

```term
$ git init
$ git add .
$ git commit -m "Empty django app"
```

Now, create a Heroku app using `heroku create`:

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

## Add task list functionality

The Django application we are building is a task list. In addition to displaying
the list, it will have actions to add new tasks and to remove them.

First, make the Django `mc_tasklist` app:

```term
(venv) $ python manage.py startapp mc_tasklist
```

Add `mc_tasklist` to the list of installed apps in `django_tasklist/settings.py`:

```python
INSTALLED_APPS = (
    'django.contrib.admin',
    # ...
    'mc_tasklist',
)
```

Now we can add the task list functionality in four steps:

1. Create a simple `Task` model in `mc_tasklist/models.py`:

   ```python
   from django.db import models

   class Task(models.Model):
       name = models.TextField()
   ```

   Use `makemigrations` and `migrate` to create a migration for the
   `mc_tasklist` app as well as create the `mc_tasklist_tasks` table
   locally, along with all other default Django tables:

   ```term
   (venv) $ python manage.py makemigrations mc_tasklist
   (venv) $ python manage.py migrate
   ```

2. Setup the routes for add, remove, and index methods in `django_tasklist/urls.py`:

   ```python
   # ...
   from mc_tasklist import views
   urlpatterns = [
       # ...
       path('add', views.add),
       path('remove', views.remove),
       path('', views.index),
   ]
   ```

3. Add corresponding view controllers in `mc_tasklist/views.py`:

   ```python
   from django.template.context_processors import csrf
   from django.shortcuts import render, redirect
   from mc_tasklist.models import Task

   def index(request):
       tasks = Task.objects.order_by("id")
       c = {'tasks': tasks}
       c.update(csrf(request))
       return render(request, 'index.html', c)

   def add(request):
       item = Task(name=request.POST["name"])
       item.save()
       return redirect("/")

   def remove(request):
       item = Task.objects.get(id=request.POST["id"])
       if item:
           item.delete()
       return redirect("/")
   ```

4. Create a template with display code in `mc_tasklist/templates/index.html`:

   ```html
   <!DOCTYPE html>
   <head>
     <meta charset="utf-8">
     <title>MemCachier Django tutorial</title>
     <!-- Fonts -->
     <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css"
           rel='stylesheet' type='text/css' />
     <!-- Bootstrap CSS -->
     <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
           rel="stylesheet" />
   </head>

   <body>
     <div class="container">
       <!-- New Task Card -->
       <div class="card">
         <div class="card-body">
           <h5 class="card-title">New Task</h5>

           <form action="add" method="POST">
             {% csrf_token %}
             <div class="form-group">
               <input type="text" class="form-control" placeholder="Task Name"
                      name="name" required>
             </div>
             <button type="submit" class="btn btn-default">
               <i class="fa fa-plus"></i> Add Task
             </button>
           </form>
         </div>
       </div>

       <!-- Current Tasks -->
       {% if tasks %}
       <div class="card">
         <div class="card-body">
           <h5 class="card-title">Current Tasks</h5>

           <table class="table table-striped">
             {% for task in tasks %}
             <tr>
               <!-- Task Name -->
               <td class="table-text">{{ task.name }}</td>
               <!-- Delete Button -->
               <td>
                 <form action="remove" method="POST">
                   {% csrf_token %}
                   <input type="hidden" name="id" value="{{ task.id }}">
                   <button type="submit" class="btn btn-danger">
                     <i class="fa fa-trash"></i> Delete
                   </button>
                 </form>
               </td>
             </tr>
             {% endfor %}
           </table>
         </div>
       </div>
       {% endif %}
     </div>

     <!-- Bootstrap related JavaScript -->
     <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
     <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
     <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
   </body>
   </html>
   ```

   Django will automatically check each apps `templates` folder for templates.

Execute `(venv) $ python manage.py runserver` and visit `http://localhost:8000` again
to play with the basic task list app by adding and removing a few tasks.

Locally we use a SQLite database to store the task list. On Heroku we need to  
provision a database:

```term
$ heroku addons:create heroku-postgresql:mini
```

Now deploy the task list to Heroku:

```term
$ git add .
$ git commit -m "Task list functionality"
$ git push heroku master
```

Finally, migrate your database on Heroku to create the `mc_tasklist_tasks`
table, and restart the Heroku app:

```term
$ heroku run python manage.py migrate
$ heroku restart
```

View the app with `heroku open` and add a few tasks to make sure the app also
works on Heroku.

## Add caching to Django

Memcache is an in-memory, distributed cache. Its primary API consists of two
operations: `SET(key, value)` and `GET(key)`.
Memcache is like a hashmap (or dictionary) that is spread across
multiple servers, where operations are still performed in constant
time.

The most common use for Memcache is to cache the results of expensive database
queries and HTML renders so that these expensive operations don’t
need to happen over and over again.

### Provision a Memcache

To use Memcache in Django, you first need to provision an actual Memcached
cache. You can easily get one for free with the
[MemCachier add-on](https://elements.heroku.com/addons/memcachier):

```term
$ heroku addons:create memcachier:dev
```

This will provision a new Memcache instance for you and expose a set
of [config variables](config-vars) containing your MemCachier credentials.

### Configure Django with MemCachier

Configure your cache by adding the following to the end of
`django_tasklist/settings.py`:

```python
def get_cache():
  import os
  try:
    servers = os.environ['MEMCACHIER_SERVERS']
    username = os.environ['MEMCACHIER_USERNAME']
    password = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        # TIMEOUT is not the connection timeout! It's the default expiration
        # timeout that should be applied to keys! Setting it to `None`
        # disables expiration.
        'TIMEOUT': None,
        'LOCATION': servers,
        'OPTIONS': {
          'username': username,
          'password': password,
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

This configures the cache for both development
and production. If the `MEMCACHIER_*` environment variables exist,
the cache will be setup with [`django-bmemcached`](https://github.com/jaysonsantos/django-bmemcached), connecting to
MemCachier. Whereas, if the `MEMCACHIER_*` environment variables
don't exist -- hence development mode -- Django's simple in-memory
cache is used instead.

### Install dependencies

Install the `django-bmemcached` Python modules:

```term
(venv) $ pip install django-bmemcached
```

Update your `requirements.txt` file with the new dependencies:

```term
(venv) $ pip freeze > requirements.txt
(venv) $ cat requirements.txt
...
django-bmemcached==0.2.4
```

Finally, commit and deploy these changes:

```term
$ git commit -am "Connecting to memcache."
$ git push heroku master
```

> note
> [`pylibmc`](https://devcenter.heroku.com/articles/memcachier#django) can be used as an alternative to `django-bmemcached`.

### Verify Memcache configuration

Verify that you've configured memcache correctly before you move
forward.

To do this, run the Django shell. On your local machine run `(venv) $ python manage.py shell` and in Heroku run `heroku run python manage.py shell`. Run a quick test to make sure your cache is configured
properly:

```python
>>> from django.core.cache import cache
>>> cache.get("foo")
>>> cache.set("foo", "bar")
>>> cache.get("foo")
'bar'
```

Exit with `Ctrl-d`. After the second `get` command, `bar` should be printed to
the screen when `foo` is fetched from the cache. If you don't see `bar` your
cache is not configured correctly.

### Cache expensive database queries

Memcache is often used to cache expensive database queries. This simple
example doesn't include any expensive queries, but for the sake of learning, let's
assume that getting all tasks from the database is an expensive operation.

The task list database query code in `mc_tasklist/views.py` can be modified
to check the cache first like so:

```python
# ...
from django.core.cache import cache
import time

TASKS_KEY = "tasks.all"

def index(request):
    tasks = cache.get(TASKS_KEY)
    if not tasks:
        time.sleep(2)  # simulate a slow query.
        tasks = Task.objects.order_by("id")
        cache.set(TASKS_KEY, tasks)
    c = {'tasks': tasks}
    c.update(csrf(request))
    return render(request, 'index.html', c)
# ...
```

The above code first checks the cache to see if the `tasks.all` key exists
in the cache. If it does not, a database query is executed and the
cache is updated. Subsequent pageloads will not need to perform the
database query. The `time.sleep(2)` only exists to simulate a slow
query.

Deploy and test this new functionality:

```term
$ git commit -am 'Add caching with MemCachier'
$ git push heroku master
$ heroku open
```

To see what's going on in your cache, open the MemCachier dashboard:

```term
$ heroku addons:open memcachier
```

The first time you loaded your task list, you should have gotten an increase
for the `get misses` and `set` commands. Every subsequent reload of the task list
should increase `get hits` (refresh the stats in the dashboard).

Our cache is working, but there is still a major problem. Add a new task and see
what happens. No new task appears on the current tasks list! The new task was
created in the database, but the app is serving the stale task list from the
cache.

### Keep Memcache up-to-date

There are many techniques for dealing with an out-of-date cache.

1. **Expiration:**
   The easiest way to make sure the cache does not get stale is by setting
   an expiration time. The `cache.set` method can take an optional third
   argument, which is the time in seconds that the cache key should stay
   in the cache. If this option is not specified, the default `TIMEOUT`
   value in `settings.py` will be used instead.

   You could modify the `cache.set` method to look like this:

   ```python
   cache.set(TASKS_KEY, tasks, 5)
   ```

   But this functionality only works when it is known for how long the cached value
   is valid. In our case however, the cache gets stale upon user interaction (add,
   remove a task).

2. **Delete cached value:**
   A straight forward strategy is to invalidate the `tasks.all` key when you know
   the cache is out of date -- namely, to modify the `add` and `remove` views to
   delete the `tasks.all` key:

   ```python
   # ...
   def add(request):
       item = Task(name=request.POST["name"])
       item.save()
       cache.delete(TASKS_KEY)
       return redirect("/")

   def remove(request):
       item = Task.objects.get(id=request.POST["id"])
       if item:
           item.delete()
           cache.delete(TASKS_KEY)
       return redirect("/")
   ```

3. **Key based expiration:**
   Another technique to invalidate stale data is to change the key:

   ```python
   # ...
   import random
   import string

   def _hash(size=16, chars=string.ascii_letters + string.digits):
       return ''.join(random.choice(chars) for _ in range(size))

   def _new_tasks_key():
       return 'tasks.all.' + _hash()

   TASKS_KEY = _new_tasks_key()

   # ...

   def add(request):
       item = Task(name=request.POST["name"])
       item.save()
       global TASKS_KEY
       TASKS_KEY = _new_tasks_key()
       return redirect("/")

   def remove(request):
       item = Task.objects.get(id=request.POST["id"])
       if item:
           item.delete()
           global TASKS_KEY
           TASKS_KEY = _new_tasks_key()
       return redirect("/")
   ```

   The upside of key based expiration is that you do not have to interact with
   the cache to expire the value. The LRU eviction of Memcache will clean out
   the old keys eventually.

4. **Update cache:**
   Instead of invalidating the key the value can also be updated to reflect
   the new task list:

   ```python
   # ...
   def add(request):
       item = Task(name=request.POST["name"])
       item.save()
       cache.set(TASKS_KEY, Task.objects.order_by("id"))
       return redirect("/")

   def remove(request):
       item = Task.objects.get(id=request.POST["id"])
       if item:
           item.delete()
           cache.set(TASKS_KEY, Task.objects.order_by("id"))
       return redirect("/")
   ```

   Updating the value instead of deleting it will allow the
   first pageload to avoid having to go to the database

You can use option 2, 3, or 4 to make sure the cache will not ever be
out-of-date.
As usual, commit and deploy your changes:

```term
$ git commit -am "Keep Memcache up to date."
$ git push heroku master
```

Now when you add a new task, all the tasks you've added since implementing
caching will appear.

## Use Django's integrated caching

Django also has a few built in ways to use your Memcache to improve performance.
These mainly target the rendering of HTML which is an expensive operation that
is taxing for the CPU.

### Caching and CSRF

You cannot cache any views or fragments that contain forms with CSRF tokens
because the token changes with each request. For the sake of learning how to
use Django's integrated caching we will disable Django's CSRF middleware.
Since this task list is public, this is not a big deal but **do not do this
in any serious production application**.

Comment `CsrfViewMiddleware` in `django_tasklist/settings.py`:

```python
MIDDLEWARE = [
    # ...
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]
```

### Cache template fragments

Django allows you to cache rendered template fragments. This is
similar to snippet caching in Flask, or caching rendered partials in
Laravel. To enable fragment caching add `{% load cache %}` to the top of your
template.

> warning
> Do not cache fragments that include forms with CSRF tokens.

To cache a rendered set of task entries, we use a `{% cache timeout key %}` statement in
`mc_tasklist/templates/index.html`:

```html
{% load cache %}
<!-- ... -->

<table class="table table-striped">
  {% for task in tasks %} {% cache None 'task-fragment' task.id %}
  <tr>
    <!-- ... -->
  </tr>
  {% endcache %} {% endfor %}
</table>

<!-- ... -->
```

Here the timeout is `None` and the key is a list of strings that will be
concatenated. As long as task IDs are never reused, this is all there is to
caching rendered snippets. The PostgreSQL database we use on Heroku does not
reuse IDs, so we're all set.

If you use a database that _does_ reuse IDs, you need to delete
the fragment when its respective task is
deleted. You can do this by adding the following code to the task deletion
logic:

```python
from django.core.cache.utils import make_template_fragment_key
key = make_template_fragment_key("task-fragment", vary_on=[str(item.id)])
cache.delete(key)
```

Let's see the effect of caching the fragments in our application:

```term
$ git commit -am 'Cache task entry fragment'
$ git push heroku master
```

You should now observe an additional `get hit` for each task in your list whenever
you reload the page (except the first reload).

### Cache entire views

We can go one step further and cache entire views instead of fragments. This
should be done with care, because it can result in unintended side effects
if a view frequently changes or contains forms for user input. In our task list
example, both of these conditions are true because the task list changes each
time a task is added or deleted, and the view contains forms to add and delete
a task.

> warning
> Do not cache views that include forms with CSRF tokens.

You can cache the task list view with the ` @cache_page(timeout)` decorator in
`mc_tasklist/views.py`:

```python
# ...
from django.views.decorators.cache import cache_page

@cache_page(None)
def index(request):
    # ...

# ...
```

Because the view changes whenever we add or remove a task, we need to delete the
cached view whenever this happens. This is not straight forward. We need to
learn the key when the view is cached in order to be then able to delete it:

```python
# ...
from django.utils.cache import learn_cache_key

VIEW_KEY = ""

@cache_page(None)
def index(request):
    # ...
    response = render(request, 'index.html', c)
    global VIEW_KEY
    VIEW_KEY = learn_cache_key(request, response)
    return response

def add(request):
    # ...
    cache.delete(VIEW_KEY)
    return redirect("/")

def remove(request):
    item = Task.objects.get(id=request.POST["id"])
    if item:
        # ...
        cache.delete(VIEW_KEY)
    return redirect("/")
```

To see the effect of view caching, deploy your application:

```term
$ git commit -am 'Cache task list view'
$ git push heroku master
```

On the first refresh, you should see the `get hits` counter increase according
to the number of tasks you have, as well as an additional `get misses` and `set cmds`,
which correspond to the view that is now cached. Any subsequent reload will
increase the `get hits` counter by just two, because the entire view is retrieved
with two `get` commands.

Note that view caching does _not_ obsolete the caching of
expensive operations or template fragments. It is good
practice to cache smaller operations within cached larger operations, or smaller
fragments within larger fragments. This technique (called Russian doll caching)
helps with performance if a larger operation, fragment, or view is removed
from the cache, because the building blocks do not have to be recreated from
scratch.

## Using Memcache for session storage

On Heroku, it's not advisable to store session information on disk, because
dynos have an ephemeral filesystem that doesn't persist across restarts.

Memcache works well for storing information for short-lived sessions that time
out. However, because Memcache is a cache and therefore not persistent,
long-lived sessions are better suited to permanent storage options, such as
your database.

For short-lived sessions configure `SESSION_ENGINE` to use the cache backend in
`django_tasklist/settings.py`:

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
```

For long-lived sessions Django allows you to use a write-through cache, backed
by a database. This is the best option for performance while guaranteeing
persistence. To use the write-through cache, configure the `SESSION_ENGINE` in
`django_tasklist/settings.py` like so:

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
```

For more information on how to use sessions in Django, please see the
[Django Session Documentation](https://docs.djangoproject.com/en/dev/topics/http/sessions/)

## Further reading and resources

- [MemCachier Add-on Page](https://elements.heroku.com/addons/memcachier)
- [MemCachier Documentation](https://devcenter.heroku.com/articles/memcachier)
- [Advance Memcache Usage](https://devcenter.heroku.com/articles/advanced-memcache)
- [Configuring Django Apps for Heroku](django-app-configuration)
- [The Django Tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/)
- [Django Caching Documentation](https://docs.djangoproject.com/en/dev/topics/cache/)
