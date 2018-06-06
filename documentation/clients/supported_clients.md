
## Client library support

MemCachier will work with any memcached binding that supports [SASL
authentication](https://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer)
and the [binary
protocol](https://github.com/memcached/memcached/wiki/BinaryProtocolRevamped).
In the following you can find a list of all clients known to us including a
description of their most important features. This list is by no means exhaustive
and if you know of a client not on this list, don't hesitate to contact us. All
clients marked as supported have been tested with our service.

### Clojure

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [Xmemcached](https://github.com/killme2008/clj-xmemcached) | yes | yes | yes | yes |

### Go

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [mc](https://github.com/memcachier/mc) | yes | yes | yes | yes |
| [gomemcache](https://github.com/bradfitz/gomemcache) | limited<sup>1</sup> | no | limited<sup>1</sup> | yes |
| [gomemcached](https://github.com/dustin/gomemcached) | ? | yes | yes | no |
| [memcache](https://github.com/rainycape/memcache)<sup>2</sup> | no | no | no | yes |
| [gomemcache (zeayes)](https://github.com/zeayes/gomemcache) | no | yes | no | yes |

<sup>1</sup> We have a [fork](https://github.com/memcachier/gomemcache) that does
ASCII auth and an outstanding PR in the main repository.  
<sup>2</sup> A high performance fork of gomemcache.  

### Haskell

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [memcache](https://github.com/dterei/memcache-hs) | yes | yes | yes | ? |
| [memcached](https://github.com/olegkat/haskell-memcached) | ? | ? | ? | ? |

### Java

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [Xmemcached](https://github.com/killme2008/xmemcached) | yes | yes | yes | yes |
| [spymemcached](https://github.com/dustin/java-memcached-client) ([mirror](https://github.com/couchbase/spymemcached)) | yes | yes | yes | yes |
| [Memcached-Java-Client](https://github.com/gwhalin/Memcached-Java-Client) | no | yes | no | ? |
| [Folsom](https://github.com/spotify/folsom) | ? | yes | no | ? |

### Node.js

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [memjs](https://github.com/alevy/memjs) | yes | yes | yes | yes |
| [memcached](https://github.com/3rd-Eden/memcached) | no | no | no | ? |
| [memcache](https://github.com/elbart/node-memcache) | no | no | no | ? |

### PHP

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [php-memcached](https://github.com/php-memcached-dev/php-memcached)<sup>1</sup> | yes | yes | yes | yes |
| [php-memcache-sasl](https://github.com/memcachier/PHPMemcacheSASL) | yes | yes | yes | yes |
| [memcached.php](https://github.com/clickalicious/memcached-php) | ? | no | no | ? |
| [php-memcache](https://github.com/tricky/php-memcache) | no | yes | yes | ? |

<sup>1</sup> Requires `libmemcached`.  

### Python

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [pylibmc](https://github.com/lericson/pylibmc)<sup>1</sup> | yes | yes | yes | yes |
| [python-binary-memcached](https://github.com/jaysonsantos/python-binary-memcached) | yes | yes | yes | yes |
| [python-memcached](https://github.com/linsomniac/python-memcached) | no | no | no | ? |
| [pymemcache](https://github.com/pinterest/pymemcache) | no | no | no | no |
| [ultramemcache](https://github.com/esnme/ultramemcache)<sup>2</sup> | no | no | no | ? |

<sup>1</sup> Requires `libmemcached`.  
<sup>2</sup> C++ bindings.

### Ruby

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [dalli](https://github.com/petergoldstein/dalli) | yes | yes | yes | yes |
| [memcached](https://github.com/arthurnn/memcached)<sup>1</sup> | ? | ? | ? | ? |

<sup>1</sup> Requires `libmemcached`.  

### Rust

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [memcache](https://github.com/aisk/rust-memcache) | no | yes | no | ? |
| [bmemcached](https://github.com/jaysonsantos/bmemcached-rs) | no | yes | no | ? |
| [memcached-rs](https://github.com/zonyitoo/memcached-rs) | no | yes | no | ? |

### Scala

| Library | Supported | Binary protocol | SASL authentication | Cluster support |
| ---     | ---       | ---             | ---                 | ---             |
| [Shade](https://github.com/monix/shade) | yes | yes | yes | ? |
| [memcontinuationed](https://github.com/Atry/memcontinuationed) | no | no | no | ? |
