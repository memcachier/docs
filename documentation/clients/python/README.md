# Examples

| Name | Library | Framework | Deploy |
| ---  | ---     | ---       | ---    |
| [Task list](https://github.com/memcachier/examples-flask) | `pylibmc-1.5.2` & `Flask-Caching-1.4.0` & `Flask-Session-0.3.1` | `Flask-1.0` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-flask) |
| [Task list](https://github.com/memcachier/examples-django-tasklist) | `pylibmc-1.5.2` | `Django-2.1` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-django-tasklist) |
| [FIFO queue](https://github.com/memcachier/examples-django2) | `pylibmc-1.5.2` | `Django-2.0` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-django2) |
| [Algebra (binary)](https://github.com/memcachier/examples-django) | `pylibmc-1.5.1` | `Django-1.8.16` & `django-pylibmc-0.6.1` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-django) |
| [Algebra (ASCII)](https://github.com/memcachier/examples-django3) | `pymemcache-1.4.0` | `Django-1.8.16` & `memcachier-django-ascii-1.0.0` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-django3) |


# Python clients

| Library | Supported / Documented | ASCII / Binary / SASL | Version | Activity | Stars |
| ---     | ---                    | ---           | ---     | ---      | ---   |
| [pylibmc](https://github.com/lericson/pylibmc)<sup>1</sup> | yes / yes\* | yes / yes / yes |  ![release](https://img.shields.io/pypi/v/pylibmc.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/lericson/pylibmc/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/lericson/pylibmc.svg?style=social&maxAge=3600) |
| [python-binary-memcached](https://github.com/jaysonsantos/python-binary-memcached) | yes / yes | no / yes / yes | ![release](https://img.shields.io/pypi/v/python-binary-memcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/jaysonsantos/python-binary-memcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/jaysonsantos/python-binary-memcached.svg?style=social&maxAge=3600) |
| [python-memcached](https://github.com/linsomniac/python-memcached) | no / no | ? / no / no |   ![release](https://img.shields.io/pypi/v/python-memcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/linsomniac/python-memcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/linsomniac/python-memcached.svg?style=social&maxAge=3600) |
| [pymemcache](https://github.com/pinterest/pymemcache) | limited<sup>2</sup> / no | yes / no / no |   ![release](https://img.shields.io/pypi/v/pymemcache.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/pinterest/pymemcache/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/pinterest/pymemcache.svg?style=social&maxAge=3600) |
| [ultramemcache](https://github.com/esnme/ultramemcache)<sup>3</sup> | no / no | yes / no / no |   ![release](https://img.shields.io/pypi/v/umemcache.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/esnme/ultramemcache/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/esnme/ultramemcache.svg?style=social&maxAge=3600) |

\* Recommended.  
<sup>1</sup> Requires `libmemcached`.  
<sup>2</sup> Only one server.  
<sup>3</sup> C++ bindings.

# Web frameworks

We document Django and Flask. See popularity
[here](http://www.timqian.com/star-history/#django/django&pallets/flask).

## Django

| Integration | Client | Supported / Documented | Version | Activity | Stars |
| ---                | ---    | ---                    | ---     | ---      | ---   |
| native | pylibmc | yes / yes* | ![release](https://img.shields.io/pypi/v/django.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/django/django/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/django/django.svg?style=social&maxAge=3600) |
| native | python-memcached | no / no | ![release](https://img.shields.io/pypi/v/django.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/django/django/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/django/django.svg?style=social&maxAge=3600) |
| [django-pylibmc](https://github.com/django-pylibmc/django-pylibmc)<sup>3</sup> | pylibmc | yes / limited<sup>4</sup> | ![release](https://img.shields.io/pypi/v/django-pylibmc.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/django-pylibmc/django-pylibmc/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/django-pylibmc/django-pylibmc.svg?style=social&maxAge=3600) |
| [django-bmemcached](https://github.com/jaysonsantos/django-bmemcached) | python-binary-memcached | yes / no | ![release](https://img.shields.io/pypi/v/django-bmemcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/jaysonsantos/django-bmemcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/jaysonsantos/django-bmemcached.svg?style=social&maxAge=3600) |
| [memcachier-django-ascii](https://github.com/memcachier/django-ascii) | pymemcache | limited<sup>5</sup> / limited<sup>4</sup> | ![release](https://img.shields.io/pypi/v/memcachier-django-ascii.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/memcachier/django-ascii/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/memcachier/django-ascii.svg?style=social&maxAge=3600) |

\* Recommended.  
<sup>3</sup> Obsolete as of Django 1.11.  
<sup>4</sup> Documented in example README.  
<sup>5</sup> Only one server.

### Helper libraries

**memcachify:**  
![release](https://img.shields.io/github/tag/rdegges/django-heroku-memcacheify.svg?maxAge=3600) ![commit](https://img.shields.io/github/last-commit/rdegges/django-heroku-memcacheify/master.svg?maxAge=3600) ![stars](https://img.shields.io/github/stars/rdegges/django-heroku-memcacheify.svg?style=social&maxAge=3600)

Sets up `django-pylibmc` with `pylibmc` for MemCachier on Heroku.

## Flask

| Integration | Client | Supported / Documented | Version | Activity | Stars |
| ---                | ---    | ---                    | ---     | ---      | ---   |
| native | pylibmc | yes / no | ![release](https://img.shields.io/pypi/v/flask.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/pallets/flask/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/pallets/flask.svg?style=social&maxAge=3600) |
| [Flask-Caching](https://github.com/sh4nks/flask-caching) | pylibmc | yes / yes | ![release](https://img.shields.io/pypi/v/flask-caching.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/sh4nks/flask-caching/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/sh4nks/flask-caching.svg?style=social&maxAge=3600) |
| [Flask-Session](https://github.com/fengsp/flask-session) | pylibmc | yes / yes | ![release](https://img.shields.io/pypi/v/flask-session.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/fengsp/flask-session/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/fengsp/flask-session.svg?style=social&maxAge=3600) |
