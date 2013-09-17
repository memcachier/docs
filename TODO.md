# Documentation Work Items

* Own as many articles on Heroku as possible (See list).

## List of Heroku articles mentioning memcached

### Not Us (Couchbase)

* https://devcenter.heroku.com/articles/memcache
* https://devcenter.heroku.com/articles/java-webapp-runner

* https://devcenter.heroku.com/articles/releases
* https://devcenter.heroku.com/articles/facebook

### Us

* https://addons.heroku.com/memcachier
* https://devcenter.heroku.com/articles/django-memcache
* https://devcenter.heroku.com/articles/advanced-memcache

* https://devcenter.heroku.com/articles/rack-cache-memcached-rails31
* https://devcenter.heroku.com/articles/building-a-rails-3-application-with-the-memcache-addon

### No one (i.e., more general articles about caching)

* https://devcenter.heroku.com/articles/caching-strategies
* https://devcenter.heroku.com/articles/http-caching-ruby-rails

# PHP

PHPMemcacheSASL isn't very good, lets change to recommending PHP
Memcached. We can't though as PHP Memcached isn't installed by default
and is hard to build, we'd need to provide an easy [install
method](##PHPMemcachedbuildpack).

Client Issues:
* PHP Memcached seem to return a 'RESULT NOT FOUND' when its actually
  an authentication error.
* PHPMemCacheSASL and PHP Memcached both don't support the
  '<server>:<port>' style config! Need to add support or change our
  example code. Or add support to them for this string.
* Example code needs to recommend the use of caching sockets so not
  always reconnecting.
* Example code should show how to enable session caching.
* PHPMemcacheSASL returns FALSE on every addServer and setOption
  command!
  * PHP Memcached seems to always return true on addServer...

## PHP Memcached buildpack

Not sure how to install PHP Memcached. Perhaps these links help:

* https://devcenter.heroku.com/articles/buildpack-binaries
* https://devcenter.heroku.com/articles/buildpacks
* https://github.com/wuputah/heroku-libraries/tree/master/php
* https://gist.github.com/pedro/1288447
* https://github.com/heroku/heroku-buildpack-php
* http://www.amido.co.uk/chris-gray/compiling-php-extensions-like-mongo-and-memcache-on-heroku/

