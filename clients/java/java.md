

<h2 id="java">Java</h2>

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
        new PlainCallbackHandler(<MEMCACHIER_USERNAME>,
            <MEMCACHIER_PASSWORD>));

    try {
      MemcachedClient mc = new MemcachedClient(new ConnectionFactoryBuilder()
          .setProtocol(ConnectionFactoryBuilder.Protocol.BINARY)
          .setAuthDescriptor(ad).build(), AddrUtil.getAddresses(<MEMCACHIER_SERVERS>));
      mc.set("foo", "bar");
      System.out.println(mc.get("foo"));
    } catch (IOException ioe) {
      System.err.println("Couldn't create a connection to MemCachier: \nIOException "
              + ioe.getMessage());
    }
  }
}
```

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and
`<MEMCACHIER_PASSWORD>` are listed on your [cache overview
page](https://www.memcachier.com/caches).

You may wish to look the `spymemcached`
[JavaDocs](https://dustin.github.com/java-memcached-client/apidocs/) or some
more [example code](https://code.google.com/p/spymemcached/wiki/Examples) to
help in using MemCachier effectively.

We’ve built a small Java example here, using Jetty: [MemCachier Java Jetty
sample app](https://github.com/memcachier/examples-java).
