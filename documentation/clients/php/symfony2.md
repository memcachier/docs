
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
The values for `MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME`, and
`MEMCACHIER_PASSWORD` are listed on your
[cache overview page](https://www.memcachier.com/caches). Make sure to add them
to your environment.
</p>
**ENDIF**
