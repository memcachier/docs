# Examples

| Name | Library | Framework | Deploy |
| ---  | ---     | ---       | ---    |
| [Task list](https://github.com/memcachier/examples-spring-boot) | `xmemcached-2.4.3` | `spring-boot-2.0.1` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-spring-boot) |
| [Fibonacci](https://github.com/memcachier/examples-java) | `spymemcached-2.12.0` | `jetty-9.3.8` | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-java) |

# Java clients

| Library | Supported / Documented | Binary / SASL | Version | Activity | Stars |
| ---     | ---                    | ---           | ---     | ---      | ---   |
| [spymemcached](https://github.com/dustin/java-memcached-client) ([mirror](https://github.com/couchbase/spymemcached)) | yes / yes\* | yes / yes |  ![release](https://img.shields.io/maven-central/v/net.spy/spymemcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/dustin/java-memcached-client/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/dustin/java-memcached-client.svg?style=social&maxAge=3600) |
| [Xmemcached](https://github.com/killme2008/xmemcached) | yes / no | yes / yes |  ![release](https://img.shields.io/maven-central/v/com.googlecode.xmemcached/xmemcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/killme2008/xmemcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/killme2008/xmemcached.svg?style=social&maxAge=3600) |
| [Memcached-Java-Client](https://github.com/gwhalin/Memcached-Java-Client) | no / no | yes / no |  ![release](https://img.shields.io/maven-central/v/com.whalin/Memcached-Java-Client.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/gwhalin/Memcached-Java-Client/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/gwhalin/Memcached-Java-Client.svg?style=social&maxAge=3600) |
| [Folsom](https://github.com/spotify/folsom) | ? / no | yes / no |  ![release](https://img.shields.io/maven-central/v/com.spotify/folsom.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/spotify/folsom.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/spotify/folsom.svg?style=social&maxAge=3600) |

\* Recommended.  

# Web frameworks

We document Spring Boot. There is also stuff like Tomcat and Jetty. See popularity
[here](http://www.timqian.com/star-history/#spring-projects/spring-boot&perwendel/spark&eclipse/jetty.project&apache/tomcat&spring-projects/spring-framework).

## Spring

| Integration | Client | Supported / Documented | Version | Activity | Stars |
| ---                | ---    | ---                    | ---     | ---      | ---   |
| [simple-spring-memcached](https://github.com/ragnor/simple-spring-memcached) | XMemcached | yes / yes* | ![release](https://img.shields.io/maven-central/v/com.google.code.simple-spring-memcached/xmemcached-provider.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/ragnor/simple-spring-memcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/ragnor/simple-spring-memcached.svg?style=social&maxAge=3600) |
| [simple-spring-memcached](https://github.com/ragnor/simple-spring-memcached) | SpyMemcached | yes / no | ![release](https://img.shields.io/maven-central/v/com.google.code.simple-spring-memcached/spymemcached-provider.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/ragnor/simple-spring-memcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/ragnor/simple-spring-memcached.svg?style=social&maxAge=3600) |
