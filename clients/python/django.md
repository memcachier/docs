
## Django

<p class="alert alert-info">
We support the <code>pylibmc</code> memcache client as it has great performance
and Python 3 support. However, it can sometimes be difficult to install locally
as it relies on the C <code>libmemcached</code> library. If you prefer, you can
try a pure python client, <a
href="https://github.com/jaysonsantos/python-binary-memcached">python-binary-memcached</a>.
You'll also need the <a
href="https://github.com/jaysonsantos/django-bmemcached">django-bmemcached</a>
package.
</p>

MemCachier has been tested with the `pylibmc` memcache client. This is a great
client, fully-featured, high-performance and Python 2 & 3 support. Sadly, the
Django integration of `pylibmc` and other memcache clients doesn't work
out-of-the-box with MemCachier as they don't expose the authentication
mechanism (SASL). This is easily solved by using the `django-pylibmc` package.

The `pylibmc` client relies on the C `libmemcached` library. This should be
fairly straight-forward to install with your package manager on Linux or
Windows. We also have a [blog
post](http://blog.memcachier.com/2014/11/05/ubuntu-libmemcached-and-sasl-support/)
for Ubuntu users on how to do this.

Once `libmemcached` is installed, then install `pylibmc` and `django-pylibmc`:

```shell
$ pip install pylibmc django-pylibmc
```

Be sure to update your `requirements.txt` file with these new requirements
(note that your versions may differ than what’s below):

```text
pylibmc==1.5.1
django-pylibmc==0.6.1
```

<p class="alert alert-info">
<b>Heroku Users:</b> The above <code>pylibmc</code> requirements must be added
directly to your <code>requirements.txt</code> file. They shouldn't be placed
in an included pip requirement file. The Heroku Python buildpack checks the
<code>requirements.txt</code> file and only that file for the presence of
<code>pylibmc</code> to trigger bootstrapping <code>libmemcached</code>, which
is prerequisite for installing <code>pylibmc</code>.
</p>

Next, configure your settings.py file the following way:

```python
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
    'default': {
        # Use pylibmc
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',

        # Use binary memcache protocol (needed for authentication)
        'BINARY': True,

        # TIMEOUT is not the connection timeout! It's the default expiration
        # timeout that should be applied to keys! Setting it to `None`
        # disables expiration.
        'TIMEOUT': None,

        'OPTIONS': {
            # Enable faster IO
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
```

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and
`<MEMCACHIER_PASSWORD>` are listed on your [cache overview
page](https://www.memcachier.com/caches). Note that Django expects
<MEMCACHIER_SERVERS> to be semicolon-delimited (while we provide it
comma-eliminated).

Finally, we also *strongly* recommend that you place the following
code in your `wsgi.py` file to correct a serious performance bug
([#11331](https://code.djangoproject.com/ticket/11331)) with Django
and memcached. The fix enables persistent connections under Django,
which by default uses a new connection for each request:

```python
# Fix django closing connection to MemCachier after every request (#11331)
from django.core.cache.backends.memcached import BaseMemcachedCache
BaseMemcachedCache.close = lambda self, **kwargs: None
```

After this, you can start writing cache code in your Django app:

```python
from django.core.cache import cache
cache.set("foo", "bar")
print cache.get("foo")
```

We’ve built a small Django example here: [MemCachier Django sample
app](https://github.com/memcachier/examples-django).

You may also be interested in the
[django-heroku-memcacheify](http://github.com/rdegges/django-heroku-memcacheify)
pip, which fully configures MemCachier with one line of code for any Django app
the pip supports.

<p class="alert alert-info">
A confusing error message you may get from <code>pylibmc</code> is
<b>MemcachedError: error 37 from memcached_set: SYSTEM ERROR (Resource
temporarily unavailable)</b>. This indicates that you are trying to store a
value larger than 1MB. MemCachier has a hard limit of 1MB for the size of
key-value pairs. To work around this, either consider sharding the data or
using a different technology. The benefit of an in-memory key-value store
diminishes at 1MB and higher.
</p>
