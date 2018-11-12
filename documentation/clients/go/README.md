# Examples

| Name | Library | Framework | Deploy |
| ---  | ---     | ---       | ---    |
| [Prime numbers](https://github.com/memcachier/examples-gin) | `mc-2.0.0` | `gin-1.2` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-gin) |

# Go clients

| Library | Supported / Documented | ASCII / Binary / SASL | Version | Activity | Stars |
| ---     | ---                    | ---           | ---     | ---      | ---   |
| [mc](https://github.com/memcachier/mc) | yes / yes\* | no / yes / yes |  ![release](https://img.shields.io/github/release/memcachier/mc.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/memcachier/mc/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/memcachier/mc.svg?style=social&maxAge=3600) |
| [gomemcache](https://github.com/bradfitz/gomemcache) | limited<sup>1</sup> / yes | yes / no / limited<sup>1</sup> |  ![release](https://img.shields.io/github/release/bradfitz/gomemcache.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/bradfitz/gomemcache/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/bradfitz/gomemcache.svg?style=social&maxAge=3600) |
| [gomemcached](https://github.com/dustin/gomemcached) | ? / no | no / yes / yes |  ![release](https://img.shields.io/github/release/dustin/gomemcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/dustin/gomemcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/dustin/gomemcached.svg?style=social&maxAge=3600) |
| [memcache](https://github.com/rainycape/memcache)<sup>2</sup> | no / no | yes / no / no |  ![release](https://img.shields.io/github/release/rainycape/memcache.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/rainycape/memcache/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/rainycape/memcache.svg?style=social&maxAge=3600) |
| [gomemcache (zeayes)](https://github.com/zeayes/gomemcache) | no / no | yes / yes / no |  ![release](https://img.shields.io/github/release/zeayes/gomemcache.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/zeayes/gomemcache/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/zeayes/gomemcache.svg?style=social&maxAge=3600) |

\* Recommended.  
<sup>1</sup> We have a [fork](https://github.com/memcachier/gomemcache) that does
ASCII auth and an outstanding PR in the main repository.  
<sup>2</sup> A high performance fork of gomemcache.  

# Web frameworks

We don't document any, but we should definitely document Gin, probably also
Beego and myabe even Revel. See popularity
[here](http://www.timqian.com/star-history/#gin-gonic/gin&astaxie/beego&revel/revel).
