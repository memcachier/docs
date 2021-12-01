---
title: "Documentation: Java"
description: "Documentation for using MemCachier with Java"
---

## Java

For Java we recommend using the
[XMemcached](https://github.com/killme2008/xmemcached) client. There is also
the [SpyMemcached](https://github.com/couchbase/spymemcached) client which we
have recommended in the past. Many MemCachier customers reported problems with
SpyMemcached in the presence of network issues. SpyMemcached seems to have
trouble coping with connection timeouts or resets. For this reason we now
recommend XMemcached.

We also recommend using [Apache Maven](https://maven.apache.org/) or
[Gradle](https://gradle.org/) as a build tool. Here we show the dependancy
configuration for Maven but they are similar for Gradle.
If you aren't using Maven or Gradle and are instead using
[Apache Ant](https://ant.apache.org/) or your own build system, then
simply add the `xmemcached` or `spymemcached` jar file as a dependency of your application.

### XMemcached

To use XMemcached with Maven you need to add the `xmemcached` library to
your dependencies in your `pom.xml` file:

```xml
<dependency>
  <groupId>com.googlecode.xmemcached</groupId>
  <artifactId>xmemcached</artifactId>
  <version>2.4.3</version>
</dependency>
```

**IF(direct)**
<p class="alert alert-info">
If you are using a version older than 2.4.3, please update to the latest version
as it contains important bug fixes.
</p>
**ENDIF**

**IF(heroku)**
>callout
>If you are using a version older than 2.4.3, please update to the latest version
>as it contains important bug fixes.
**ENDIF**

Once your build system is configured, you can start adding caching to your Java
app:

```java
import net.rubyeye.xmemcached.MemcachedClient;
import net.rubyeye.xmemcached.MemcachedClientBuilder;
import net.rubyeye.xmemcached.XMemcachedClientBuilder;
import net.rubyeye.xmemcached.auth.AuthInfo;
import net.rubyeye.xmemcached.command.BinaryCommandFactory;
import net.rubyeye.xmemcached.exception.MemcachedException;
import net.rubyeye.xmemcached.utils.AddrUtil;

import java.lang.InterruptedException;
import java.net.InetSocketAddress;
import java.io.IOException;
import java.util.List;
import java.util.concurrent.TimeoutException;

public class App {
  public static void main( String[] args ) {
    List<InetSocketAddress> servers =
      AddrUtil.getAddresses(System.getenv("MEMCACHIER_SERVERS").replace(",", " "));
    AuthInfo authInfo =
      AuthInfo.plain(System.getenv("MEMCACHIER_USERNAME"),
                     System.getenv("MEMCACHIER_PASSWORD"));

    MemcachedClientBuilder builder = new XMemcachedClientBuilder(servers);

    // Configure SASL auth for each server
    for(InetSocketAddress server : servers) {
      builder.addAuthInfo(server, authInfo);
    }

    // Use binary protocol
    builder.setCommandFactory(new BinaryCommandFactory());
    // Connection timeout in milliseconds (default: )
    builder.setConnectTimeout(1000);
    // Reconnect to servers (default: true)
    builder.setEnableHealSession(true);
    // Delay until reconnect attempt in milliseconds (default: 2000)
    builder.setHealSessionInterval(2000);

    try {
      MemcachedClient mc = builder.build();
      try {
        mc.set("foo", 0, "bar");
        String val = mc.get("foo");
        System.out.println(val);
      } catch (TimeoutException te) {
        System.err.println("Timeout during set or get: " +
                           te.getMessage());
      } catch (InterruptedException ie) {
        System.err.println("Interrupt during set or get: " +
                           ie.getMessage());
      } catch (MemcachedException me) {
        System.err.println("Memcached error during get or set: " +
                           me.getMessage());
      }
    } catch (IOException ioe) {
      System.err.println("Couldn't create a connection to MemCachier: " +
                         ioe.getMessage());
    }
  }
}
```

**IF(direct)**
<p class="alert alert-info">
The values for <code>MEMCACHIER_SERVERS</code>, <code>MEMCACHIER_USERNAME</code>, and
<code>MEMCACHIER_PASSWORD</code> are listed on your
<a href="https://www.memcachier.com/caches">cache overview page</a>. Make sure to add them
to your environment.
</p>
**ENDIF**

You may wish to look the `xmemcached`
[Wiki](https://github.com/killme2008/xmemcached/wiki) or
[JavaDocs](http://fnil.net/docs/xmemcached/).

### SpyMemcached

**IF(direct)**
<p class="alert alert-info">
We’ve built a small Java example, using SpyMemcached with Jetty:
<a href="https://github.com/memcachier/examples-java">MemCachier Java Jetty sample app</a>.
</p>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Java example, using SpyMemcached with Jetty.
><a class="github-source-code" href="https://github.com/memcachier/examples-java">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-java).
**ENDIF**

To use SpyMemcached with Maven you need to add the `spymemcached` library to
your dependencies in your `pom.xml` file:

```xml
<dependency>
  <groupId>spy</groupId>
  <artifactId>spymemcached</artifactId>
  <version>2.12.3</version>
  <scope>provided</scope>
</dependency>
```

Once your build system is configured, you can start adding caching to your Java
app:

```java
import java.io.IOException;
import net.spy.memcached.AddrUtil;
import net.spy.memcached.MemcachedClient;
import net.spy.memcached.ConnectionFactoryBuilder;
import net.spy.memcached.auth.PlainCallbackHandler;
import net.spy.memcached.auth.AuthDescriptor;

public class Foo {
  public static void main(String[] args) {
    AuthDescriptor ad = new AuthDescriptor(
        new String[] { "PLAIN" },
        new PlainCallbackHandler(System.getenv("MEMCACHIER_USERNAME"),
                                 System.getenv("MEMCACHIER_PASSWORD")));
    try {
      MemcachedClient mc = new MemcachedClient(
          new ConnectionFactoryBuilder()
              .setProtocol(ConnectionFactoryBuilder.Protocol.BINARY)
              .setAuthDescriptor(ad).build(),
          AddrUtil.getAddresses(System.getenv("MEMCACHIER_SERVERS")));

      mc.set("foo", 0, "bar");
      System.out.println(mc.get("foo"));
    } catch (IOException ioe) {
      System.err.println("Couldn't create a connection to MemCachier: \nIOException "
              + ioe.getMessage());
    }
  }
}
```

**IF(direct)**
<p class="alert alert-info">
The values for <code>MEMCACHIER_SERVERS</code>, <code>MEMCACHIER_USERNAME</code>, and
<code>MEMCACHIER_PASSWORD</code> are listed on your
<a href="https://www.memcachier.com/caches">cache overview page</a>. Make sure to add them
to your environment.
</p>
**ENDIF**

For convenience, you may want to set the above code up as a new `MemCachierClient`
class:

```java
package com.memcachier.examples.java;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.ArrayList;
import java.util.List;

import javax.security.auth.callback.CallbackHandler;

import net.spy.memcached.ConnectionFactory;
import net.spy.memcached.ConnectionFactoryBuilder;
import net.spy.memcached.MemcachedClient;
import net.spy.memcached.auth.AuthDescriptor;
import net.spy.memcached.auth.PlainCallbackHandler;

public class MemCachierClient extends MemcachedClient {

   public MemCachierClient(String username, String password, String servers) throws IOException {
       this(new SASLConnectionFactoryBuilder().build(username, password), getAddresses(servers));
   }

   public MemCachierClient(ConnectionFactory cf, List<InetSocketAddress> addrs) throws IOException {
       super(cf, addrs);
   }

   private static List<InetSocketAddress> getAddresses(String servers) {
       List<InetSocketAddress> addrList = new ArrayList<InetSocketAddress>();
       for (String server : servers.split(",")) {
           String addr = server.split(":")[0];
           int port = Integer.parseInt(server.split(":")[1]);
           addrList.add(new InetSocketAddress(addr, port));
       }
       return addrList;
   }
}

class SASLConnectionFactoryBuilder extends ConnectionFactoryBuilder {
   public ConnectionFactory build(String username, String password){
       CallbackHandler ch = new PlainCallbackHandler(username, password);
       AuthDescriptor ad = new AuthDescriptor(new String[]{"PLAIN"}, ch);
       this.setProtocol(Protocol.BINARY);
       this.setAuthDescriptor(ad);
       return this.build();
   }
}
```
**IF(direct)**
<p class="alert alert-info">
It is possible that you will run into Java exceptions about the class
loader. (See Spymemcached
<a href="http://code.google.com/p/spymemcached/issues/detail?id=155">issue 155</a>.
The reported issue also contains a suggested work around.
</p>
**ENDIF**
**IF(heroku)**
>callout
>It is possible that you will run into Java exceptions about the class
>loader. (See Spymemcached [issue
>155](http://code.google.com/p/spymemcached/issues/detail?id=155). The
>reported issue also contains a suggested work around.
**ENDIF**

You may wish to look the `spymemcached`
[JavaDocs](https://dustin.github.io/java-memcached-client/apidocs/) or some
more [example code](https://code.google.com/p/spymemcached/wiki/Examples) to
help in using MemCachier effectively.
**IF(heroku)**
There is also a guide on using
[WebRunner](https://devcenter.heroku.com/articles/java-webapp-runner),
Heroku's framework to handle sessions with MemCachier.
**ENDIF**
