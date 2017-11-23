
## Local usage

**IF(direct)**
To test against your application locally, you will need to run a local
memcached process. MemCachier is only available from the datacenter you signed
up for. But
**ENDIF**
**IF(heroku)**
To test your Heroku application locally, you will need to run a local
memcached server. MemCachier can only run in Heroku, but
**ENDIF**
because MemCachier and memcached speak the same protocol, you
shouldn’t have any issues testing locally. Installation depends on your
platform.

**IF(direct)**
<p class="alert alert-info">
The below examples will install memcached without
SASL authentication support. This is generally what you want as client code can
still try to use SASL auth and memcached will simply ignore the requests which
is the same as allowing any credentials. So your client code can run without
modification locally.
</p>
**ENDIF**

**IF(heroku)**
>callout
>This will install memcached without SASL authentication support. This is
>generally what you want as client code can still try to use SASL auth and
>memcached will simply ignore the requests which is the same as allowing any
>credentials. So your client code can run without modification locally and on
>Heroku.
**ENDIF**

On Ubuntu:

```shell
$ sudo apt-get install memcached
```

Or on OS X (with Homebrew):

```shell
$ brew install memcached
```

Or for Windows please refer to [these
instructions](http://www.heckler.com.br/blog/2013/05/10/memcached-on-windows/)

For further information and resources (such as the memcached source code)
please refer to the [Memcache.org homepage](http://memcached.org)

To run memcached simply execute the following command:

```shell
$ memcached -v
```
