---
title: "Documentation: Laravel"
description: "Documentation for using MemCachier with Laravel"
---

## Laravel

**IF(direct)**
<div class="alert alert-info">
We’ve built a small Laravel example here:
<a href="https://github.com/memcachier/examples-laravel-heroku">MemCachier Laravel sample app</a>.
<br>
Related tutorials:
<ul>
  <li><a href="https://devcenter.heroku.com/articles/laravel-memcache">Scaling a Laravel Application with Memcache on Heroku</a></li>
</ul>
</div>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Laravel example.
><a class="github-source-code" href="http://github.com/memcachier/examples-laravel-heroku">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-laravel-heroku).
><br>
>We also have a tutorial on using Laravel with MemCachier
>[here](https://devcenter.heroku.com/articles/laravel-memcache).
**ENDIF**

As of Laravel 5.3, memcached is supported out of the box with the `php-memcached`
PECL extension. Instructions on how to install `php-memcached` can be found
**IF(direct)**
[here](/documentation/php).
**ENDIF**
**IF(heroku)**
[here](#php).
**ENDIF**
Older versions of Laravel require
[`laravel-memcached-plus`](https://github.com/b3it/laravel-memcached-plus) for
memcached integration.

Before setting up `memcached` as your default cache we need to add the
dependency to `composer.json`:

```term
$ composer require ext-memcached
```

Then we need to config the cache in `config/cache.php`:

```php
'memcached' => [
    'driver' => 'memcached',
    'persistent_id' => 'memcached_pool_id',
    'sasl' => [
        env('MEMCACHIER_USERNAME'),
        env('MEMCACHIER_PASSWORD'),
    ],
    'options' => [
        // some nicer default options
        // - nicer TCP options
        Memcached::OPT_TCP_NODELAY => TRUE,
        Memcached::OPT_NO_BLOCK => FALSE,
        // - timeouts
        Memcached::OPT_CONNECT_TIMEOUT => 2000,    // ms
        Memcached::OPT_POLL_TIMEOUT => 2000,       // ms
        Memcached::OPT_RECV_TIMEOUT => 750 * 1000, // us
        Memcached::OPT_SEND_TIMEOUT => 750 * 1000, // us
        // - better failover
        Memcached::OPT_DISTRIBUTION => Memcached::DISTRIBUTION_CONSISTENT,
        Memcached::OPT_LIBKETAMA_COMPATIBLE => TRUE,
        Memcached::OPT_RETRY_TIMEOUT => 2,
        Memcached::OPT_SERVER_FAILURE_LIMIT => 1,
        Memcached::OPT_AUTO_EJECT_HOSTS => TRUE,

    ],
    'servers' => array_map(function($s) {
        $parts = explode(":", $s);
        return [
            'host' => $parts[0],
            'port' => $parts[1],
            'weight' => 100,
        ];
      }, explode(",", env('MEMCACHIER_SERVERS', 'localhost:11211')))
],
```
**IF(direct)**
<p class="alert alert-info">
The values for <code>MEMCACHIER_SERVERS</code>, <code>MEMCACHIER_USERNAME</code>, and
<code>MEMCACHIER_PASSWORD</code> are listed on your
<a href="https://www.memcachier.com/caches">cache overview page</a>. Make sure to add them
to your environment.
</p>
**ENDIF**

For Laravel to use memcached as its cache you will need to set the `CACHE_DRIVER`
**IF(direct)**
environment variable in the `.env` file:

```
CACHE_DRIVER=memcached
```
**ENDIF**
**IF(heroku)**
environment variable:

```term
$ heroku config:set CACHE_DRIVER=memcached
```
**ENDIF**

Note, if you prefer you may also configure `memcached` to be your default cache
driver in `config/cache.php`:

```php
'default' => env('CACHE_DRIVER', 'memcached'),
```

For more information on how to use the cache in Laravel, we recommend you consult
the [Laravel caching documentation](https://laravel.com/docs/5.6/cache) or our
[Laravel tutorial](https://devcenter.heroku.com/articles/laravel-memcache).

### Use memcached for session storage

Memcached works well for sessions that time out, however,
since memcached is a cache and thus not persistent, saving long-lived
sessions in memcached might not be ideal. For long-lived sessions consider a
permanent storage option such as you database.

Changing the session store from a file (default) to memcached can be done easily
**IF(direct)**
by just setting an environment variable in the `.env` file:

```
SESSION_DRIVER=memcached
```
**ENDIF**
**IF(heroku)**
by just setting an environment variable:

```term
$ heroku config:set SESSION_DRIVER=memcached
```
**ENDIF**

### Caching rendered partials

With the help of
[laravel-partialcache](https://github.com/spatie/laravel-partialcache) you can
also cache rendered partials in Laravel. This is essentially the same as
fragment caching in Ruby on Rails. If you have complex partials in your
application it is a good idea to cache them because rendering HTML can be a
CPU intensive task.

> warning
> Do not cache partials that include forms with CSRF tokens.

You can add this dependency to your Laravel project with

```term
$ composer require spatie/laravel-partialcache
```

and it will give you the `@cache` blade directive. It works just like the
`@include` directive with a few added parameters.

For example,

```php
@cache('my-complex.partial', ['data' => $data], null, $data->id)
```

will include `my-complex.partial`, pass it `$data` with the identifier `data`
and cache it forever (`null`) and add `$data->id` to the cache key.

You can invalidate this cached partial with from your code with
`PartialCache::forget('my-complex.partial', $data->id);`.

### Caching entire reponses

In Laravel it is also easy to cache the entire rendered HTML response by using
[laravel-responsecache](https://github.com/spatie/laravel-responsecache). This
is essentially the same as view caching in Ruby on Rails. This package is easy
to use and has good documentation in it's README. To use this package with
memcached you have to set the environment variable `RESPONSE_CACHE_DRIVER` to
`memcached`.
