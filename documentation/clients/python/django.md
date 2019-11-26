
## Django

**IF(direct)**
<div class="alert alert-info">
We’ve built a small Django example here:
<a href="https://github.com/memcachier/examples-django-tasklist">MemCachier Django sample app</a>.
<br>
Related tutorials:
<ul>
  <li><a href="https://devcenter.heroku.com/articles/django-memcache">Scaling a Django Application with Memcache on Heroku</a></li>
  <li><a href="https://blog.memcachier.com/2018/06/27/django-docker-ecs-tutorial/">MemCachier with Django, Docker and AWS Elastic Container Service</a></li>
  <li><a href="https://blog.memcachier.com/2018/10/15/django-on-pythonanywhere-tutorial/">How to scale a Django Application on PythonAnywhere with Memcache</a></li>
</ul>
</div>

<p class="alert alert-info">
We recommend the <a
href="https://github.com/jaysonsantos/django-bmemcached">django-bmemcached</a> 
Django backend, as it uses the <a href="https://github.com/jaysonsantos/python-binary-memcached">python-binary-memcached</a>
memcache client which is a pure Python library. However, if you prefer, you can
try the <code>pylibmc</code> memcache client which has a larger ecosystem. 
However, it can sometimes be difficult to install locally as it relies on the 
C <code>libmemcached</code> library. 
</p>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Django example.
><a class="github-source-code" href="https://github.com/memcachier/examples-django-tasklist">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-django-tasklist).
><br>
>We also have a tutorial on using Django and MemCachier together
>[here](https://devcenter.heroku.com/articles/django-memcache).

>callout
>We recommend the [django-bmemcached](ttps://github.com/jaysonsantos/django-bmemcached) 
>Django backend, as it uses the [python-binary-memcached](https://github.com/jaysonsantos/python-binary-memcached)
>memcache client which is a pure Python library. However, if you prefer, you can
>try the <code>pylibmc</code> memcache client which has a larger ecosystem. However, it can sometimes be difficult to install locally
>as it relies on the C <code>libmemcached</code> library. 
**ENDIF**

Here we explain how you setup and install MemCachier with Django. Please
see the [Django caching
guide](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-site-cache)
for how you effectively use MemCachier. Django supports
whole site caching, per-view caching and fragement caching.

MemCachier has been tested with the `python-binary-memcached` memcache client. This is a great
client, fully-featured, high-performance and Python 2 & 3 support. Older Django versions
require `django-pylibmc` to work with MemCachier. Please follow the instructions
in this [example](http://github.com/memcachier/examples-django) if you wish to
use an older version.

Install `django-bmemcached`:

```term
$ pip install django-bmemcached
```

Be sure to update your `requirements.txt` file with these new requirements
(note that your versions may differ than what’s below):

```text
django-bmemcached==0.2.4
```

**IF(heroku)**
>callout
>Note: The above `django-bmemcached` requirements must be added directly to your
>`requirements.txt` file. They shouldn't be placed in an included pip
>requirement file.
**ENDIF**

Next, configure your settings.py file the following way:

```python
servers = os.environ['MEMCACHIER_SERVERS']
username = os.environ['MEMCACHIER_USERNAME']
password = os.environ['MEMCACHIER_PASSWORD']

CACHES = {
    'default': {
        # Use django-bmemcached
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
```

**IF(direct)**
<p class="alert alert-info">
The values for <code>MEMCACHIER_SERVERS</code>, <code>MEMCACHIER_USERNAME</code>, and
<code>MEMCACHIER_PASSWORD</code> are listed on your
<a href="https://www.memcachier.com/caches">cache overview page</a>. Make sure to add them
to your environment.
</p>
**ENDIF**

After this, you can start writing cache code in your Django app:

```python
from django.core.cache import cache
cache.set("foo", "bar")
print cache.get("foo")
```

You may also be interested in the
[django-heroku-memcacheify](http://github.com/rdegges/django-heroku-memcacheify)
pip, which fully configures MemCachier with one line of code for any Django app
the pip supports.

**IF(direct)**
<p class="alert alert-info">
If using <code>pylibmc</code> instead of <code>django-bmemcached</code>, a confusing error message you may get from <code>pylibmc</code> is
<b>MemcachedError: error 37 from memcached_set: SYSTEM ERROR (Resource
temporarily unavailable)</b>. This indicates that you are trying to store a
value larger than 1MB. MemCachier has a hard limit of 1MB for the size of
key-value pairs. To work around this, either consider sharding the data or
using a different technology. The benefit of an in-memory key-value store
diminishes at 1MB and higher.
</p>
**ENDIF**

**IF(heroku)**
>note
>If using `pylibmc` instead of `django-bmemcached`, a confusing error message you may get from `pylibmc` is
>**MemcachedError: error 37 from memcached_set: SYSTEM ERROR (Resource
>temporarily unavailable)**. This indicates that you are trying to
>store a value larger than 1MB. MemCachier has a hard limit of 1MB for
>the size of key-value pairs. To work around this, either consider
>sharding the data or using a different technology. The benefit of an
>in-memory key-value store diminishes at 1MB and higher.
**ENDIF**


### Template fragment caching

Django allows you to cache rendered template fragments. To enable fragment
caching, add `{% load cache %}` to the top of each template caching is used in.
The control statement to cache a fragment has the form
`{% cache timeout key ... %}` where all additional parameters after the key
are just appended to the key. In practice this may look as follows:

```html
{% load cache %}
<!-- ... -->

<!-- Fragment caching example -->
{% for item in list %}
  {% cache None 'item-fragment' item.id %}
  <div>
    <!-- fragment that does something with the item -->
  </div>
  {% endcache %}
{% endfor %}
```
Here the timeout is `None`, but it can also be a variable that contains a time or
an integer denoting seconds.

The cached snippet from the above example can be invalidated (deleted) as follows:

```python
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
key = make_template_fragment_key("item-fragment", vary_on=[str(item.id)])
cache.delete(key)
```

### View caching

Django also provides a decorator to cache views:

```python
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
# ...

timeout = 600 # 10 min

@cache_page(timeout)
def index(request):
  # ...
  return render_template('index.html', ...)
```

If a cached view ever has to be invalidated explicitly, the key to the view
needs to be saved:

```python
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.utils.cache import learn_cache_key
# ...

timeout = None
view_keys = {}

@cache_page(timeout)
def index(request):
  # ...
  response = render_template('index.html', ...)
  view_keys['index'] = learn_cache_key(request, response)
  return response
```

Now the view can be invalidated with:

```python
from django.core.cache import cache
cache.delete(view_keys['index'])
```

### Session storage

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
