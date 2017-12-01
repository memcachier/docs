
## Symfony2

**IF(direct)**

The [Symfony2](http://symfony.com/) framework is a great choice with
MemCachier. It supports caching and storing sessions in MemCachier.

First, start by configuring an appropriate `.user.ini` in your document root.
It should contain the following:

```php
session.save_handler=memcached
memcached.sess_binary=1
session.save_path="PERSISTENT=myapp_session <MEMCACHIER_SERVERS>"
memcached.sess_sasl_username=<MEMCACHIER_USERNAME>
memcached.sess_sasl_password=<MEMCACHIER_PASSWORD>
```
**ENDIF**

**IF(heroku)**

The [Symfony2](http://symfony.com/) framework is a great choice with
Heroku and MemCachier. It supports caching and storing sessions in
MemCachier.

First, start by configuring an appropriate `.user.ini` in your
document root (see [heroku ini
guide](https://devcenter.heroku.com/articles/custom-php-settings#user-ini-files-recommended)).
It should contain the following:

```php
session.save_handler=memcached
memcached.sess_binary=1
session.save_path="PERSISTENT=myapp_session ${MEMCACHIER_SERVERS}"
memcached.sess_sasl_username=${MEMCACHIER_USERNAME}
memcached.sess_sasl_password=${MEMCACHIER_PASSWORD}
```
**ENDIF**