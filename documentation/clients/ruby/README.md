# Examples

| Name | Library | Framework | Deploy |
| ---  | ---     | ---       | ---    |
| [Contact list](https://github.com/memcachier/examples-rails-heroku) | `dalli-2.7.6` | `rails-5.1.4` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/memcachier/examples-rails-heroku) |
| [Contact list (old)](https://github.com/memcachier/examples-rails3-heroku) | `dalli-2.7.6` | `rails-3.2.22.2` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/memcachier/examples-rails3-heroku) |
| [GIS lookup](https://github.com/memcachier/examples-rails) | `dalli-2.7.6` | `rails-3.2.22.2` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/memcachier/examples-rails) |
| [Facebook Graph API](https://github.com/memcachier/examples-sinatra) | `dalli-2.7.6` | `sinatra-1.4.7` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/memcachier/examples-sinatra) |
<!-- | [TODO](https://github.com/memcachier/examples-rails-memcached_store) | `memcached-1.8.0` | `Rails-5.1.4` & `memcached_store-1.1.0` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-rails-memcached_store) | -->



# Ruby clients

| Library | Supported / Documented | ASCII / Binary / SASL | Version | Activity | Stars |
| ---     | ---                    | ---           | ---     | ---      | ---   |
| [dalli](https://github.com/petergoldstein/dalli) | yes / yes\* | no / yes / yes | ![release](https://img.shields.io/gem/v/dalli.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/petergoldstein/dalli/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/petergoldstein/dalli.svg?style=social&maxAge=3600) |
| [memcached](https://github.com/arthurnn/memcached)<sup>1</sup> | ? / no<sup>2</sup> | ? / ? / ? |  ![release](https://img.shields.io/gem/v/memcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/arthurnn/memcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/arthurnn/memcached.svg?style=social&maxAge=3600) |

\* Recommended.  
<sup>1</sup> Requires `libmemcached`.  
<sup>2</sup> We should check if we can support and document this client because
it is supposedly [faster](https://github.com/basecamp/memcached_bench).

# Web frameworks

We document Rails and Sinatra. See popularity
[here](http://www.timqian.com/star-history/#rails/rails&sinatra/sinatra).

## Rails

| Integration | Client | Supported / Documented | Version | Activity | Stars |
| ---               | ---    | ---                    | ---     | ---      | ---   |
| native | dalli | yes / yes* | ![release](https://img.shields.io/gem/v/rails.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/rails/rails/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/rails/rails.svg?style=social&maxAge=3600) |
| [memcached_store](https://github.com/Shopify/memcached_store) | memcached | ? / no | ![release](https://img.shields.io/gem/v/memcached_store.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/Shopify/memcached_store/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/Shopify/memcached_store.svg?style=social&maxAge=3600) |

\* Recommended.

## Sinatra

| Integration | Client | Supported / Documented | Version | Activity | Stars |
| ---                 | ---    | ---                    | ---     | ---      | ---   |
| native<sup>3</sup> | dalli | yes / no<sup>4</sup> | ![release](https://img.shields.io/gem/v/sinatra.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/sinatra/sinatra/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/sinatra/sinatra.svg?style=social&maxAge=3600) |
| native<sup>3</sup> | memcached | ? / no | ![release](https://img.shields.io/gem/v/sinatra.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/sinatra/sinatra/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/sinatra/sinatra.svg?style=social&maxAge=3600) |

<sup>3</sup> Since sinatra is a minimal framework caching is not really integrated.  
<sup>4</sup> There is a sample app.
