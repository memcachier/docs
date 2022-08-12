
Memcache is a technology that improves the performance and scalability of web
apps and mobile app backends. You should consider
using Memcache when your pages are loading too slowly or your app is
having scalability issues. Even for small sites, Memcache can make page loads
snappy and help future-proof your app.

This guide shows how to create a simple
[Django 4.0](https://www.djangoproject.com/) application, deploy it on DigitalOcean's App Platform,
then add Memcache to alleviate a performance bottleneck.

>note
>The sample app in this guide can be seen running
>[here](https://memcachier-django-tasklist.herokuapp.com/) and you can
>view the [source code on GitHub](https://github.com/memcachier/examples-django-tasklist-do).

## Prerequisites
Before you complete the steps in this guide, make sure you have all of the
following:

* Familiarity with Python (and ideally Django)
* A DigitalOcean user account ([signup is free and instant](https://cloud.digitalocean.com/registrations/new))
* Python and the [DigitalOcean CLI](https://docs.digitalocean.com/reference/doctl/) installed on your computer

## Create a Django application

The following commands will create an empty Django app. A detailed
explanation of these commands can be found in
[Deploying Python and Django Apps](deploying-python).

```term
$ mkdir django_memcache && cd django_memcache
$ python -m venv venv    # For Python 2 use `virtualenv venv`
$ source venv/bin/activate
(venv) $ pip install django gunicorn psycopg2-binary dj-database-url
(venv) $ pip freeze > requirements.txt
(venv) $ django-admin startproject django_tasklist .
(venv) $ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).

Django version 2.0, using settings 'django_tasklist.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Visiting [http://localhost:8000](http://localhost:8000) will show a
"hello, world" landing page.

### Configure Django for DigitalOcean App Platform

For the Django app to work on DigitalOcean, some App Platform specific configuration is
required. For more information about this configuration, please consult the 
[official documentation](https://docs.digitalocean.com/tutorials/app-deploy-django-app/). 
In summary, open `django_tasklist/settings.py and do the followig:

1. Add the following imports at the beginning of the file:
   ```python
   import os
   import sys
   import dj_database_url
   from django.core.management.utils import get_random_secret_key
   ```
   These allow you to read environment variables, read command line arguments, 
   process database URLs, and generate random security keys.
2. Avoid using a hardcoded secret key:
   ```python
   SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
   ```
3. Set the debug directive:
   ```python
   DEBUG = os.getenv("DEBUG", "True") == "True"
   ```
4. Set allowed hosts:
   ```python
   ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
   ```
5. Configure database access:
    ```python
    DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "True") == "True"
    if DEVELOPMENT_MODE is True:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        }
    elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
        if os.getenv("DATABASE_URL", None) is None:
            raise Exception("DATABASE_URL environment variable not defined")
        DATABASES = {
            "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
        }
    ```
    This configuration introduces the `DEVELOPMENT_MODE` environment variable to control
    which database type of database should be used (SQLite for development, PostgreSQL for production).
  <!-- 6. Add directives to the end of the file to configure static files location:
     ```python
     STATIC_URL = "/static/"
     STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
     ``` -->

Save and close `settings.py` and let us move to deploying our Django skeleton app to App Platform.

### Push your App to GitHub

DigitalOcean App Platform deploys your code from GitHub repositories so 
our code needs to be added to a git repository. First, create a `.gitignore` file
and adding the following lines to exclude unnecessary files:

```text
venv
*.pyc
db.sqlite3
spec.yaml
```

Then initialize a git repository and make a commit:

```term
$ git init
$ git add .
$ git commit -m "Empty Django app"
```

Go to your [GitHub](https://github.com/) profile and create a new repository called django-tasklist. 
Make sure to create an empty repository without a README or license file.

Now, push our empty Django app to GitHub:

```term
$ git remote add origin git@github.com:<YOUR_GITHUB_USERNAME>/django-tasklist.git
$ git branch -M main
$ git push -u origin main
```

With your Django code on GitHub it is now time to deploy the app to DigitalOcean’s App Platform.

### Deploy on DigitalOcean App Platform

To deploy the app to App Platform we first need to create a spec. The spec is a YAML file that contains
the configuration of your app.

```yaml
# spec.yaml

name: django-tasklist

# Choose the region you want
region: nyc

# Configure the Django web service
services:
- name: django-tasklist-ws
  instance_size_slug: basic-xs
  instance_count: 1
  environment_slug: python
  github:
    branch: main
    deploy_on_push: true
    repo: <YOUR_GITHUB_USERNAME>/django-tasklist
  source_dir: /
  http_port: 8080
  routes:
  - path: /
  run_command: gunicorn --worker-tmp-dir /dev/shm django_tasklist.wsgi

  # Set environment variables for this web service
  envs:
  - key: DJANGO_ALLOWED_HOSTS
    scope: RUN_AND_BUILD_TIME
    value: ${APP_DOMAIN}
  - key: DATABASE_URL
    scope: RUN_AND_BUILD_TIME
    value: ${db.DATABASE_URL}  # gets the value from `db` configured below
  - key: DEBUG
    scope: RUN_AND_BUILD_TIME
    value: "False"
  - key: DEVELOPMENT_MODE
    scope: RUN_AND_BUILD_TIME
    value: "False"
  - key: DJANGO_SECRET_KEY
    scope: RUN_AND_BUILD_TIME
    type: SECRET
    value: <RANDOM_SECRET_KEY>

# Attach a PostgreSQL database
databases:
- engine: PG
  name: db
  num_nodes: 1
  size: basic-xxs
  version: "12"
```

Make sure to set the correct GitHub repository name as well as the `<RANDOM_SECRET_KEY>` and safe you spec as `spec.yaml`. 
Now you can create and deploy the app using DigitalOcean's command line tool `doctl`:

```term
$ doctl apps create --spec spec.yaml
```

This will create your App Platform app and start deployment. 
You can check the deployment status on your DigitalOcean [dashboard](https://cloud.digitalocean.com/apps).
It will take a while so in the meantime let's continue adding the tasklist functionality.

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


### Try Your Tasklist App on App Platform

To deploy our latest code to App Platform we only need to push it to GitHub:

```term
$ git add .
$ git commit -m "Task list functionality"
$ git push origin main
```

Now that our task list app is deployed on App Platform there is one more step needed
before we can use it. We need to run the database migration to make sure all our tables exist.
Unfortunately, this cannot be done from your command line. To run the migrations, visit the
[apps dashboard](https://cloud.digitalocean.com/apps), select the `django-tasklist` app, click
the *Console* tab, and enter the following command:

```term
$ python manage.py migrate
```

Now you can click on *Live App* and play around with the task list.

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
[MemCachier add-on](https://marketplace.digitalocean.com/add-ons/memcachier)
on the DigitalOcean marketplace. Currently, there is no `doctl` command yet to
provision add-ons so we have to do this from within the browser. 
Visit the [MemCachier add-on page](https://marketplace.digitalocean.com/add-ons/memcachier)
to add the addon. Give it a descriptive name, e.g. `django-tasklist`, and select the
same region as the app lives in. This is important to make sure caching operations are
as fast as they are supposed to be.

Visit the add-on page to view the configuration variables. Your cache will have three, namely
`MEMCACHIER_USERNAME`, `MEMCACHIER_PASSWORD`, and `MEMCACHIER_SERVERS`. To use the newly
provisioned cache in our Django app, we need to set these three variables in our `django-tasklist` app.
There are two ways to do this:

1. Visit your app's dashboard on [App Platform](https://cloud.digitalocean.com/apps/), go to the
   *Settings* tab, click on the `django-tasklist-ws` component, and edit the environment variables.
2. Add the variables to the spec file we used before:
   ```
   # spec.yaml
   #...
   - key: MEMCACHIER_USERNAME
     scope: RUN_AND_BUILD_TIME
     value: <YOUR_CACHE_USERNAME>
   - key: MEMCACHIER_PASSWORD
     scope: RUN_AND_BUILD_TIME
     value: <YOUR_CACHE_PASSWORD>
   - key: MEMCACHIER_SERVERS
     scope: RUN_AND_BUILD_TIME
     value: <YOUR_CACHE_SERVERS>
   #...
   ```
   *Note, if you no longer have the spec (you should not commit it to GitHub because it contains secrets), 
   you can always get it via `doctl apps spec get <APP_ID>`.*

   Then, from your command line, to the following:
   - `doctl apps list` to find the ID for the `django-tasklist` app.
   - `doctl apps update <APP_ID> --spec spec.yaml` to update your apps configuration.

Now that your cache's credentials are accessible from your app, let's configure it.

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
and production.  If the `MEMCACHIER_*` environment variables exist,
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
django-bmemcached==0.3.0
...
```

Finally, commit and deploy these changes:

```term
$ git commit -am "Connecting to memcache."
$ git push origin main
```

>note
>[`pylibmc`](https://www.memcachier.com/documentation/django) can be used as an alternative to `django-bmemcached`.

### Verify Memcache configuration

Verify that you've configured memcache correctly before you move
forward.

To do this, visit the dashboard of your app on DigitalOcean. Once the app has deployed from
your previous push to GitHub, run the Django shell in the *Console* tab with 
`python manage.py shell`. In the shell, run a quick test to make sure your cache is configured
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

In addition, you can also see the effects of this test on your cache on your MemCachier dashboard.
For this, visit your add-on in the [Marketplace Add-Ons page](https://cloud.digitalocean.com/add-ons/)
and click on *Dashboard*.

On the MemCachier dashboard you can now see that your cache contains one item, got one `set` command,
and two `get` commands, one of which was a `miss` and one was a `hit`. This should result in a `hit rate`
of 50%.

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
in the cache.  If it does not, a database query is executed and the
cache is updated.  Subsequent pageloads will not need to perform the
database query.  The `time.sleep(2)` only exists to simulate a slow
query.

Deploy and test this new functionality:

```term
$ git commit -am 'Add caching with MemCachier'
$ git push origin main
```

Once deployed, open your app. To see what's going on in your cache, 
also open the MemCachier dashboard.

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
    in the cache.  If this option is not specified, the default `TIMEOUT`
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
    first pageload to avoid having to go to the database.

You can use option 2, 3, or 4 to make sure the cache will not ever be
out-of-date.
As usual, commit and deploy your changes:

```term
$ git commit -am "Keep Memcache up to date."
$ git push origin main
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
> In a production application, do not cache fragments that include forms with CSRF tokens.

To cache a rendered set of task entries, we use a `{% cache timeout key %}` statement in
`mc_tasklist/templates/index.html`:

```html
{% load cache %}
<!-- ... -->

<table class="table table-striped">
  {% for task in tasks %}
    {% cache None 'task-fragment' task.id %}
    <tr>
      <!-- ... -->
    </tr>
    {% endcache %}
  {% endfor %}
</table>

<!-- ... -->
```

Here the timeout is `None` and the key is a list of strings that will be
concatenated. As long as task IDs are never reused, this is all there is to
caching rendered snippets. The PostgreSQL database we use on DigitalOcean does not
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
$ git push origin main
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
$ git push origin main
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

On App Platform, it's not advisable to store session information on disk, because
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

* [MemCachier Add-on Page](https://marketplace.digitalocean.com/add-ons/memcachier)
* [MemCachier Documentation](https://www.memcachier.com/documentation)
* [Deploying Django Apps on App Platform](https://docs.digitalocean.com/tutorials/app-deploy-django-app/)
* [The Django Tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/)
* [Django Caching Documentation](https://docs.djangoproject.com/en/dev/topics/cache/)
