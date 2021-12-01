---
title: "Documentation: Local usage"
description: "To test against your application locally, you will need to run a local memcached process."
---

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

```term
$ sudo apt-get install memcached
```

On macOS (with Homebrew):

```term
$ brew install memcached
```

For Windows you will need to build memcached from
[source](https://github.com/memcached/memcached).

For further information and resources (such as the memcached source code)
please refer to the [Memcached.org homepage](https://memcached.org)

To run memcached simply execute the following command:

```term
$ memcached -v
```
