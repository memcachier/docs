

<h2 id="symfony2">Symfony2</h2>

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
