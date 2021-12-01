---
title: "Documentation: Symfony2"
description: "Documentation for using MemCachier with Symfony2"
---

## Symfony2

The [Symfony2](http://symfony.com/) framework is a great choice with
**IF(heroku)**
Heroku and
**ENDIF**
MemCachier. It supports caching and storing sessions in Memcache.

First, start by configuring an appropriate `.user.ini` in your document
**IF(heroku)**
root (see [heroku ini
guide](https://devcenter.heroku.com/articles/custom-php-settings#user-ini-files-recommended)).
**ENDIF**
**IF(direct)**
root.
**ENDIF**
It should contain the following:

```php
session.save_handler=memcached
memcached.sess_binary=1
session.save_path="PERSISTENT=myapp_session ${MEMCACHIER_SERVERS}"
memcached.sess_sasl_username=${MEMCACHIER_USERNAME}
memcached.sess_sasl_password=${MEMCACHIER_PASSWORD}
```
**ENDIF**

**IF(direct)**
<p class="alert alert-info">
The values for <code>MEMCACHIER_SERVERS</code>, <code>MEMCACHIER_USERNAME</code>, and
<code>MEMCACHIER_PASSWORD</code> are listed on your
<a href="https://www.memcachier.com/caches">cache overview page</a>. Make sure to add them
to your environment.
</p>
**ENDIF**
