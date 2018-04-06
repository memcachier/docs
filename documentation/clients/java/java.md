
## Java

**IF(direct)**
<p class="alert alert-info">
We’ve built a small Java example here, using Jetty:
<a href="https://github.com/memcachier/examples-java">MemCachier Java Jetty sample app</a>.
</p>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Java example with Jetty.
><a class="github-source-code" href="https://github.com/memcachier/examples-java">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-java).
**ENDIF**

For Java we recommend using the
[SpyMemcached](https://code.google.com/p/spymemcached/) client. We also
recommend using the [Apache Maven](https://maven.apache.org/) build manager for
working with Java applications. If you aren't using `maven` and are instead
using [Apache Ant](https://ant.apache.org/) or your own build system, then
simply add the `spymemcached` jar file as a dependency of your application.

For `maven` however, start by configuring it to have the proper `spymemcached`
repository:

```xml
<repository>
  <id>spy</id>
  <name>Spy Repository</name>
  <layout>default</layout>
  <url>http://files.couchbase.com/maven2/</url>
  <snapshots>
    <enabled>false</enabled>
  </snapshots>
</repository>
```

Then add the `spymemcached` library to your dependencies:

```xml
<dependency>
  <groupId>spy</groupId>
  <artifactId>spymemcached</artifactId>
  <version>2.12.1</version>
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
    AuthDescriptor ad = new AuthDescriptor(new String[] { "PLAIN" },
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
The values for `MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME`, and
`MEMCACHIER_PASSWORD` are listed on your
[cache overview page](https://www.memcachier.com/caches). Make sure to add them
to your environment.
</p>
**ENDIF**

**IF(heroku)**
You may want to set the above code up as a new `MemCachierClient`
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

>callout
>It is possible that you will run into Java exceptions about the class
>loader. (See Spymemcached [issue
>155](http://code.google.com/p/spymemcached/issues/detail?id=155). The
>reported issue also contains a suggested work around.
**ENDIF**

You may wish to look the `spymemcached`
[JavaDocs](https://dustin.github.com/java-memcached-client/apidocs/) or some
more [example code](https://code.google.com/p/spymemcached/wiki/Examples) to
help in using MemCachier effectively.
**IF(heroku)**
There is also a guide on using
[WebRunner](https://devcenter.heroku.com/articles/java-webapp-runner),
Heroku's framework to handle sessions with MemCachier.
**ENDIF**
