---
title: "Documentation: Python"
description: "Documentation for using MemCachier with Python"
---

## Python

Here we explain how you setup and install MemCachier with Python.

**IF(direct)**
<p class="alert alert-info">
We recommend the <a
href="https://github.com/jaysonsantos/python-binary-memcached">python-binary-memcached</a>
memcache client as it is a pure Python library. However, if you prefer, you can
try <a href="https://github.com/lericson/pylibmc">pylibmc</a> which has a larger ecosystem.
</p>
**ENDIF**

**IF(heroku)**
>callout
>We recommend the [python-binary-memcached](https://github.com/jaysonsantos/python-binary-memcached)
>memcache client as it is a pure Python library. However, if you prefer, you can
>use [pylibmc](https://github.com/lericson/pylibmc) which has a larger ecosystem.
**ENDIF**

### Recommended client: python-binary-memcached

This is a pure python client that supports the binary protocol and SASL
authentication.

To install `python-binary-memcached`:

```term
$ pip install python-binary-memcached
```

Be sure to update your `requirements.txt` file with these new requirements
(note that your versions may differ than what’s below):

```text
python-binary-memcached==0.28.0
```

Next, configure your memcached client in the following way:

```python
import bmemcached
import os

servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
user = os.environ.get('MEMCACHIER_USERNAME', '')
passw = os.environ.get('MEMCACHIER_PASSWORD', '')

mc = bmemcached.Client(servers, username=user, password=passw)

mc.enable_retry_delay(True)  # Enabled by default. Sets retry delay to 5s.
```

After this, you can start writing cache code in your Python app:

```python
mc.set("foo", "bar")
print(mc.get("foo"))
```

### Alternative client: pylibmc

This client relies on the C libmemcached library. This should be fairly
straight-forward to install with your package manager on Linux or
Windows. We also have a
[blog post](https://blog.memcachier.com/2014/11/05/ubuntu-libmemcached-and-sasl-support/)
for Ubuntu users on how to do this.
**IF(heroku)**
You only need to be concerned about this for local development, the Heroku
platform includes `libmemcached`.
**ENDIF**

Once it's installed, then install `pylibmc`:

```term
$ pip install pylibmc
```

Be sure to update your `requirements.txt` file with these new requirements
(note that your versions may differ than what’s below):

```text
pylibmc==1.5.2
```

**IF(direct)**
<p class="alert alert-info">
<b>Heroku Users:</b> The above <code>pylibmc</code> requirements must be added
directly to your <code>requirements.txt</code> file. They shouldn't be placed
in an included pip requirement file. The Heroku Python buildpack checks the
<code>requirements.txt</code> file and only that file for the presence of
<code>pylibmc</code> to trigger bootstrapping <code>libmemcached</code>, which
is prerequisite for installing <code>pylibmc</code>.
</p>
**ENDIF**

**IF(heroku)**
>callout
>The above `pylibmc` requirements must be added directly to your
>`requirements.txt` file. They shouldn't be placed in an included pip
>requirement file. The Heroku Python buildpack checks the `requirements.txt`
>file and only that file for the presence of `pylibmc` to trigger bootstrapping
>`libmemcached`, which is prerequisite for installing `pylibmc`.
**ENDIF**

Next, configure your memcached client in the following way:

```python
import pylibmc
import os

servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
user = os.environ.get('MEMCACHIER_USERNAME', '')
passw = os.environ.get('MEMCACHIER_PASSWORD', '')

mc = pylibmc.Client(servers, binary=True,
                    username=user, password=passw,
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
```

**IF(direct)**
<p class="alert alert-info">
The values for <code>MEMCACHIER_SERVERS</code>, <code>MEMCACHIER_USERNAME</code>, and
<code>MEMCACHIER_PASSWORD</code> are listed on your
<a href="https://www.memcachier.com/caches">cache overview page</a>. Make sure to add them
to your environment.
</p>
**ENDIF**

After this, you can start writing cache code in your Python app:

```python
mc.set("foo", "bar")
print(mc.get("foo"))
```

**IF(direct)**
<p class="alert alert-info">
A confusing error message you may get from <code>pylibmc</code> is
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
>A confusing error message you may get from `pylibmc` is
>**MemcachedError: error 37 from memcached_set: SYSTEM ERROR (Resource
>temporarily unavailable)**. This indicates that you are trying to
>store a value larger than 1MB. MemCachier has a hard limit of 1MB for
>the size of key-value pairs. To work around this, either consider
>sharding the data or using a different technology. The benefit of an
>in-memory key-value store diminishes at 1MB and higher.
**ENDIF**
