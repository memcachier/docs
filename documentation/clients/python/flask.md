
## Flask

**IF(direct)**
<div class="alert alert-info">
We’ve built a small Flask example here:
<a href="https://github.com/memcachier/examples-flask">MemCachier Flask sample app</a>.
<br>
Related tutorials:
<ul>
  <li><a href="https://devcenter.heroku.com/articles/flask-memcache">Scaling a Flask Application with Memcache on Heroku</a></li>
</ul>
</div>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Flask example.
><a class="github-source-code" href="http://github.com/memcachier/examples-flask">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-flask).
><br>
>We also have a tutorial on using Flask and MemCachier together
>[here](https://devcenter.heroku.com/articles/flask-memcache).
**ENDIF**

Here we explain how you setup and install MemCachier with Flask. While Flask
has a built-in caching backend its features are limited to manual caching. For
this reason we recommend you use the
[`Flask-Caching`](https://github.com/sh4nks/flask-caching) package.
Flask-Caching supports memoization, fragment caching (Jinja2 snippets), and
whole view caching. For more details about how to use Flask-Caching please
refer to its [documentation](https://flask-caching.readthedocs.io/en/latest/)

`Flask-Caching` requires the `pylibmc` client which relies on the C
`libmemcached` library. This should be
fairly straight-forward to install with your package manager on Linux or
Windows. For Mac OSX users, homebrew provides and easy solution. We also have a
[blog post](http://blog.memcachier.com/2014/11/05/ubuntu-libmemcached-and-sasl-support/)
for Ubuntu users on how to do this.
**IF(heroku)**
You only need to be concerned about this for local development, the Heroku
platform includes `libmemcached`.
**ENDIF**

Once `libmemcached` is installed, then install `Flask-Caching` and `pylibmc`:

```term
$ pip install Flask-Caching pylibmc
```

Be sure to update your `requirements.txt` file with these new requirements
(note that your versions may differ than what’s below):

```text
Flask-Caching==1.4.0
pylibmc==1.5.2
```

**IF(heroku)**
>callout
>Note: The above `pylibmc` requirements must be added directly to your
>`requirements.txt` file. They shouldn't be placed in an included pip
>requirement file. The Heroku Python buildpack checks the `requirements.txt`
>file and only that file for the presence of `pylibmc` to trigger bootstrapping
>`libmemcached`, which is prerequisite for installing `pylibmc`.
**ENDIF**

Next, configure your Flask app the following way:

```python
import os
from flask import Flask
from flask_caching import Cache

cache = Cache()
app = Flask(__name__)

cache_servers = os.environ.get('MEMCACHIER_SERVERS')
if cache_servers == None:
    # Fall back to simple in memory cache (development)
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
else:
    cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
    cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
    cache.init_app(app,
        config={'CACHE_TYPE': 'saslmemcached',
                'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
                'CACHE_MEMCACHED_USERNAME': cache_user,
                'CACHE_MEMCACHED_PASSWORD': cache_pass,
                'CACHE_OPTIONS': { 'behaviors': {
                    # Faster IO
                    'tcp_nodelay': True,
                    # Keep connection alive
                    'tcp_keepalive': True,
                    # Timeout for set/get requests
                    'connect_timeout': 2000, # ms
                    'send_timeout': 750 * 1000, # us
                    'receive_timeout': 750 * 1000, # us
                    '_poll_timeout': 2000, # ms
                    # Better failover
                    'ketama': True,
                    'remove_failed': 1,
                    'retry_timeout': 2,
                    'dead_timeout': 30}}})
```

**IF(direct)**
<p class="alert alert-info">
The values for <code>MEMCACHIER_SERVERS</code>, <code>MEMCACHIER_USERNAME</code>, and
<code>MEMCACHIER_PASSWORD</code> are listed on your
<a href="https://www.memcachier.com/caches">cache overview page</a>. Make sure to add them
to your environment.
</p>
**ENDIF**

After this, you can start writing cache code in your Flask app:

```python
cache.set("foo", "bar")
print cache.get("foo")
```

### Function memoization

`Flask-Caching` provides a decorator to memoize functions. This basically means
when the function is called, Flask-Cache will check if the result is in the
cache and if it is not it will run the function and save the result to the
cache. The memoize decorator works as follows:

```python
@cache.memoize()
def run_expensive_computation(parameter):
    # ...
    return result
```

If you need to invalidate stale data you can either delete all memoized results
for a function with `cache.delete_memoized(run_expensive_computation)` or a
result for a specific `parameter` with
`cache.delete_memoized(run_expensive_computation, parameter)`.

### View caching

`Flask-Caching` also provides a decorator to cache views:

```python
@bp.route('/', methods=('GET',))
@cache.cached()
def index():
  # ...
  return render_template('index.html', ...)
```

**IF(direct)**
<p class="alert alert-info">
It is important to note that the <code>@cache.cached()</code> decorator is
directly above the definition of the <code>index()</code> function, i.e., below
the <code>@bp.route()</code> decorator.
</p>
**ENDIF**
**IF(heroku)**
>note
>It is important to note that the ` @cache.cached()` decorator is directly above
>the definiton of the `index()` function, i.e., below the ` @bp.route()`
>decorator.
**ENDIF**

The views are cached with a key of the form `'view/' + request.path`. This is
important to know if you ever need to invalidate a cached view. You can do that
with `cache.delete('view/'+path_of_stale_view)`

### Jinja2 snippet caching

`Flask-Caching` provides a Jinja2 control flow statement to cache snippets.
The statement has the form `{% cache timeout, key, ... %}` where all additional
parameters after the key are just appended to the key. In practice this may look
as follows:

```html
<!-- Snippet caching example -->
{% for item in list %}
  {% cache None, 'item', item['id']|string %}
  <div>
    <!-- Jinja2 snippet that does something with the item -->
  </div>
  {% endcache %}
{% endfor %}
```

Here the timeout is `None` but it can also be a variable that contains a time or
an integer denoting seconds.

The cached snippet from the above example can be invalidated (deleted) as follows:

```python
from flask_caching import make_template_fragment_key
key = make_template_fragment_key('item', vary_on=[str(item.id)])
cache.delete(key)
```

### Session caching

Memcache works well for storing information for short-lived sessions that time
out. However, because Memcache is a cache and therefore not persistent,
long-lived sessions are better suited to permanent storage options, such as
your database.

To store sessions in Memcache, you need
[Flask-Session](https://pythonhosted.org/Flask-Session/).

```term
$ pip install Flask-Session pylibmc
```

Be sure to update your `requirements.txt` file with these new requirements
(note that your versions may differ than what’s below):

```text
Flask-Session==0.3.1
pylibmc==1.5.2
```

Now, configure `Flask-Session`:

```python
import os
import pylibmc
from flask import Flask
from flask_session import Session

app = Flask(__name__)

servers = os.environ.get('MEMCACHIER_SERVERS').split(',')
username = os.environ.get('MEMCACHIER_USERNAME')
passwd = os.environ.get('MEMCACHIER_PASSWORD')

app.config.from_mapping(
    SESSION_TYPE = 'memcached',
    SESSION_MEMCACHED =
        pylibmc.Client(cache_servers.split(','), binary=True,
                       username=cache_user, password=cache_pass,
                       behaviors={
                            # Faster IO
                            'tcp_nodelay': True,
                            # Keep connection alive
                            'tcp_keepalive': True,
                            # Timeout for set/get requests
                            'connect_timeout': 2000, # ms
                            'send_timeout': 750 * 1000, # us
                            'receive_timeout': 750 * 1000, # us
                            '_poll_timeout': 2000, # ms
                            # Better failover
                            'ketama': True,
                            'remove_failed': 1,
                            'retry_timeout': 2,
                            'dead_timeout': 30,
                       })
)
Session(app)
```

You can now use sessions in your app like so:

```python
from flask import session
session['key'] = 'value'
session.get('key', 'not set')
```
