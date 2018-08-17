
## Spring Boot

**IF(direct)**
<p class="alert alert-info">
We’ve built a small Spring Boot example here:
<a href="https://github.com/memcachier/examples-spring-boot-heroku">MemCachier Spring Boot sample app</a>.
<br>
Related tutorials:
<ul>
  <li><a href="https://devcenter.heroku.com/articles/spring-boot-memcache">Scaling a Spring Boot Application with Memcache on Heroku</a></li>
  <li><a href="https://blog.memcachier.com/2018/07/16/spring-boot-on-pivotal-tutorial//">Build a Spring Boot Application on Pivotal Web Services and scale it with Memcache</a></li>
</ul>
</p>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Spring Boot example.
><a class="github-source-code" href="http://github.com/memcachier/examples-spring-boot-heroku">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-spring-boot-heroku).
><br>
>We also have a tutorial on using Spring Boot with MemCachier
>[here](https://devcenter.heroku.com/articles/spring-boot-memcache).
**ENDIF**

In order to use memcache in Spring you can use
[`simple-spring-memcached`](https://github.com/ragnor/simple-spring-memcached).
It works with both, the `XMemcached` (recommended) or the `SpyMemcached` client.

### Simple Spring XMemcached

We recommend you use Simple Spring Memcached with the XMemcached client. In
order to do so you need to add the respective dependencies to your `pom.xml`:

```xml
<dependency>
  <groupId>com.google.code.simple-spring-memcached</groupId>
  <artifactId>xmemcached-provider</artifactId>
  <version>4.0.0</version>
</dependency>
<dependency>
  <groupId>com.googlecode.xmemcached</groupId>
  <artifactId>xmemcached</artifactId>
  <version>2.4.3</version>
</dependency>
```

For version 4.0.0 of `simple-spring-memcached` it is important that you
explicitly import XMemcached version 2.4.3 as it contains important bug fixes.

To configure Simple Spring Memcached with XMemcached, add the following
configuration class to your application:

```java
import java.net.InetSocketAddress;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import com.google.code.ssm.CacheFactory;
import com.google.code.ssm.config.AbstractSSMConfiguration;
import com.google.code.ssm.config.DefaultAddressProvider;
import com.google.code.ssm.providers.xmemcached.XMemcachedConfiguration;
import com.google.code.ssm.providers.xmemcached.MemcacheClientFactoryImpl;
import net.rubyeye.xmemcached.auth.AuthInfo;
import net.rubyeye.xmemcached.utils.AddrUtil;

@Configuration
public class MemCachierConfig extends AbstractSSMConfiguration {

  @Bean
  @Override
  public CacheFactory defaultMemcachedClient() {
    String serverString = System.getenv("MEMCACHIER_SERVERS").replace(",", " ");
    List<InetSocketAddress> servers = AddrUtil.getAddresses(serverString);
    AuthInfo authInfo = AuthInfo.plain(System.getenv("MEMCACHIER_USERNAME"),
                                       System.getenv("MEMCACHIER_PASSWORD"));
    Map<InetSocketAddress, AuthInfo> authInfoMap =
      new HashMap<InetSocketAddress, AuthInfo>();
    for(InetSocketAddress server : servers) {
      authInfoMap.put(server, authInfo);
    }

    final XMemcachedConfiguration conf = new XMemcachedConfiguration();
    conf.setUseBinaryProtocol(true);
    conf.setAuthInfoMap(authInfoMap);

    final CacheFactory cf = new CacheFactory();
    cf.setCacheClientFactory(new MemcacheClientFactoryImpl());
    cf.setAddressProvider(new DefaultAddressProvider(serverString));
    cf.setConfiguration(conf);
    return cf;
  }
}
```

Now you can use the Simple Spring Memcached annotations in your Spring
application.

### Simple Spring SpyMemcached

If you want to use Simple Spring Memcached with SpyMemcached you need to add the respective dependencies to your `pom.xml`:

```xml
<dependency>
  <groupId>com.google.code.simple-spring-memcached</groupId>
  <artifactId>spymemcached-provider</artifactId>
  <version>4.0.0</version>
</dependency>
```

To configure Simple Spring Memcached with SpyMemcached, add the following
configuration class to your application:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import com.google.code.ssm.CacheFactory;
import com.google.code.ssm.config.AbstractSSMConfiguration;
import com.google.code.ssm.config.DefaultAddressProvider;
import com.google.code.ssm.providers.spymemcached.SpymemcachedConfiguration;
import com.google.code.ssm.providers.spymemcached.MemcacheClientFactoryImpl;
import net.spy.memcached.auth.AuthDescriptor;
import net.spy.memcached.auth.PlainCallbackHandler;

@Configuration
public class MemCachierConfig extends AbstractSSMConfiguration {

  @Bean
  @Override
  public CacheFactory defaultMemcachedClient() {
    String serverString = System.getenv("MEMCACHIER_SERVERS");
    AuthDescriptor ad = new AuthDescriptor(new String[] { "PLAIN" },
                new PlainCallbackHandler(System.getenv("MEMCACHIER_USERNAME"),
                                         System.getenv("MEMCACHIER_PASSWORD")));

    final SpymemcachedConfiguration conf = new SpymemcachedConfiguration();
    conf.setUseBinaryProtocol(true);
    conf.setAuthDescriptor(ad);

    final CacheFactory cf = new CacheFactory();
    cf.setCacheClientFactory(new MemcacheClientFactoryImpl());
    cf.setAddressProvider(new DefaultAddressProvider(serverString));
    cf.setConfiguration(conf);
    return cf;
  }
}
```

Now you can use the Simple Spring Memcached annotations in your Spring
application.

### Use Simple Spring Memcached annotations

To apply caching to functions Simple Spring Memcached provides three main types
of annotations:

1. **@ReadThrough\*Cache** tries to get a value from the cache. If it does not
  exist it will execute the function and store the return value in the cache to
  make sure it is available the next time the function is called.
2. **@Invalidate\*Cache** deletes key value pairs from the cache.
3. **@Update\*Cache** updates the values for stored keys.


Each type of annotation comes in 3 flavors (to replace the \* above):

1. **Single** applies the caching method to a single key that is specified by
  a parameter of the annotated function marked with the
  `@ParameterValueKeyProvider` annotation.
2. **Multi** applies the caching method to a collection of keys and works the
  same as `Single` but the annotated parameter needs to be a `Collection`.
3. **Assign** applies the caching method to an assigned key defined within the
  annotation.

These 9 annotations are the meat of Simple Spring Memacached but it offers more
annotations to aid your caching needs. For more information consult the Simple
Spring Memcached
[documentation](https://github.com/ragnor/simple-spring-memcached/wiki/Getting-Started#usage).

#### Some examples

* Probably the most used annotation is `@ReadThroughSingleCache`. It caches the
  result of complex computation with a key depending on the namespace and the
  input value. The cached value never expires.

  ```java
  @ReadThroughSingleCache(namespace = "ComplexComuptation", expiration = 0)
  public ComplexSerializableResult compute(@ParameterValueKeyProvider Long input) {
    // ...
    return result;
  }
  ```

* It is important to delete stale data and `@InvalidateAssignCache` does
  exactely that for a given key:

  ```java
  @InvalidateAssignCache(namespace = "TableA", assignedKey = "SumOfColumnX")
  public void saveValueToTableA(TableAObject value) {
    //...
  }
  ```

More examples can be found in the Simple Spring Memcached
[documentation](https://github.com/ragnor/simple-spring-memcached/wiki/Getting-Started#usage).

### Use Spring Caching integration

Spring also has native caching annotations and `simple-spring-memcached` can
be configured so Spring's integrated caching is backed by memcache. While it is
a good idea to use Spring's caching integration if you want the flexibility to
change the underlying store at any time, we generally recommend using the
annotations provided by Simple Spring Memcached as they are specifically
designed to be used with Memcache.

Enabling memcache for Spring's cache integration requires an additional
dependency in your `pom.xml` file:

```xml
<dependency>
  <groupId>com.google.code.simple-spring-memcached</groupId>
  <artifactId>spring-cache</artifactId>
  <version>4.0.0</version>
</dependency>
```

To use these annotations you need create a `CacheManager` bean and set the
`@EnableCaching` annotation. Concretely, extend the `MemCachierConfig` shown
above as follows:

```java
// ...
import java.util.Arrays;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.CacheManager;
import com.google.code.ssm.Cache;
import com.google.code.ssm.spring.ExtendedSSMCacheManager;
import com.google.code.ssm.spring.SSMCache;

@EnableCaching
@Configuration
public class MemCachierConfig extends AbstractSSMConfiguration {

  @Bean
  @Override
  public CacheFactory defaultMemcachedClient() {
    // ...
  }

  @Bean
  public CacheManager cacheManager() throws Exception {
    // Use SSMCacheManager instead of ExtendedSSMCacheManager if you do not
    // need to set per key expiration
    ExtendedSSMCacheManager cacheManager = new ExtendedSSMCacheManager();
    Cache cache = this.defaultMemcachedClient().getObject();
    // SSMCache(cache, 0, false) creates a cache with default key expiration
    // of 0 (no expiration) and flushing disabled (allowClear = false)
    cacheManager.setCaches(Arrays.asList(new SSMCache(cache, 0, false)));
    return cacheManager;
  }
}
```

Now you can use Spring's caching annotations, most importantly `@Cacheble`,
`@CacheEvict`, and `@CachePut`.

**IF(direct)**
<p class="alert alert-info">
Note: Spring's annotations require a cache name. The default cache name
configured by Simple Spring Memcached is `"default"`.
</p>
**ENDIF**

**IF(heroku)**
>callout
>Note: Spring's annotations require a cache name. The default cache name
>configured by Simple Spring Memcached is `"default"`.
**ENDIF**

* `@Cacheable` performs similarly to the `@ReadThrough*Cache` annotations
  explained above: it tries to get a value from the cache but if unavailable,
  it will execute the function and store the result for future calls to this
  function with the given parameters.

  ```java
  @Cacheable("default#3600")
  public ComplexSerializableResult compute(Long input) {
    // ...
    return result;
  }
  ```

  `@Cacheable` does not have native support setting expiration times. However,
  if you use the `ExtendedSSMCacheManager` you can set an expriation time by
  appending `#<seconds>` to the cache name. The example above sets the
  expiration to one hour. Omitting this appendix falls back to the configured
  default expiration time.

* `@CacheEvict` deletes a value from the cache. This is important to get rid of
  stale data.

  ```java
  @CacheEvict("default")
  public void updateValue(ValueId id) {
    //...
  }
  ```

* `@CachePut` allows you to add values to the cache and is a great way to
  optimize your cache. It supports the same options as the `@Cacheable`
  annotation.

  ```java
  @CachePut("default")
  public Value updateValue(ValueId id) {
    //...
    return value;
  }
  ```

For more information on these caching annotations and their options consult Spring's
[caching documentation](https://docs.spring.io/spring/docs/5.0.5.RELEASE/spring-framework-reference/integration.html#cache)
and the *Spring Caching Integration* secion of the Simple Spring Memcached
[documentation](https://github.com/ragnor/simple-spring-memcached/wiki/Getting-Started#spring-31-cache-integration).
