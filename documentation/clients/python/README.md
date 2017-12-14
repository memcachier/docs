
## Python clients

| Library | Supported | Binary | SASL | Version | Activity | Stars |
| ---     | ---       | ---    | ---  | ---     | ---      | ---   |
| [pylibmc](https://github.com/lericson/pylibmc)<sup>1</sup> | yes | yes | yes |  ![release](https://img.shields.io/github/tag/lericson/pylibmc.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/lericson/pylibmc/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/lericson/pylibmc.svg?style=social&maxAge=3600) |
| [python-binary-memcached](https://github.com/jaysonsantos/python-binary-memcached) | yes | yes | yes |   ![release](https://img.shields.io/github/tag/jaysonsantos/python-binary-memcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/jaysonsantos/python-binary-memcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/jaysonsantos/python-binary-memcached.svg?style=social&maxAge=3600) |
| [python-memcached](https://github.com/linsomniac/python-memcached) | no | no | no |   ![release](https://img.shields.io/github/tag/linsomniac/python-memcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/linsomniac/python-memcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/linsomniac/python-memcached.svg?style=social&maxAge=3600) |
| [pymemcache](https://github.com/pinterest/pymemcache) | limited<sup>2</sup> | no | no |   ![release](https://img.shields.io/github/tag/pinterest/pymemcache.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/pinterest/pymemcache/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/pinterest/pymemcache.svg?style=social&maxAge=3600) |

<sup>1</sup> Requires `libmemcached`.  
<sup>2</sup> Only one server.

## Django support

| Django integration | Client | Supported | Version | Activity | Stars |
| ---                | ---    | ---       | ---     | ---      | ---   |
| native | pylibmc | yes | ![release](https://img.shields.io/github/tag/django/django.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/django/django/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/django/django.svg?style=social&maxAge=3600) |
| native | python-memcached | no | ![release](https://img.shields.io/github/tag/django/django.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/django/django/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/django/django.svg?style=social&maxAge=3600) |
| [django-pylibmc](https://github.com/django-pylibmc/django-pylibmc)<sup>3</sup> | pylibmc | yes | ![release](https://img.shields.io/github/tag/django-pylibmc/django-pylibmc.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/django-pylibmc/django-pylibmc/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/django-pylibmc/django-pylibmc.svg?style=social&maxAge=3600) |
| [django-bmemcached](https://github.com/jaysonsantos/django-bmemcached) | python-binary-memcached | yes |  ![release](https://img.shields.io/github/tag/jaysonsantos/django-bmemcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/jaysonsantos/django-bmemcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/jaysonsantos/django-bmemcached.svg?style=social&maxAge=3600) |
| [memcachier-django-ascii](https://github.com/memcachier/django-ascii) | pymemcache | limited<sup>4</sup> |   ![release](https://img.shields.io/github/tag/memcachier/django-ascii.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/memcachier/django-ascii/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/memcachier/django-ascii.svg?style=social&maxAge=3600) |

<sup>3</sup> Obsolete as of Django 1.11.  
<sup>4</sup> Only one server.

### Helper libraries

#### memcachify:
![release](https://img.shields.io/github/tag/rdegges/django-heroku-memcacheify.svg?maxAge=3600) ![commit](https://img.shields.io/github/last-commit/rdegges/django-heroku-memcacheify/master.svg?maxAge=3600) ![stars](https://img.shields.io/github/stars/rdegges/django-heroku-memcacheify.svg?style=social&maxAge=3600)

Sets up `django-pylibmc` with `pylibmc` for MemCachier on Heroku.


<!-- ## TODO: Flask support (via Werkzeug)  -->
