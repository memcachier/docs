
## Go

Here we explain how you setup and use MemCachier in Go.

We recommend the [`mc`](https://github.com/memcachier/mc) memcache client. It
supports the binary protocol and SASL authentication and was specifically
designed to work well with MemCachier.
However, if you prefer to use [`gomemcache`](https://github.com/bradfitz/gomemcache)
we have a [fork](https://github.com/memcachier/mc) of `gomemcache` that works
with MemCachier.

### Recommended client: `mc`

This client is supports the binary protocol and SASL authentication and is
maintained by MemCachier. To install it run:

```term
$ go get github.com/memcachier/mc
```

Next, configure your memcached client in the following way:

```go
username := os.Getenv("MEMCACHIER_USERNAME")
password := os.Getenv("MEMCACHIER_PASSWORD")
server := os.Getenv("MEMCACHIER_SERVERS")

c := mc.NewMC(server, username, password)
defer c.Quit()
```

This will create a memcache client with default parameters. If you prefer, you
can also configure the memcache client like so:

```go
username := os.Getenv("MEMCACHIER_USERNAME")
password := os.Getenv("MEMCACHIER_PASSWORD")
server := os.Getenv("MEMCACHIER_SERVERS")

config := mc.DefaultConfig()
config.Hasher = mc.NewModuloHasher()         // default
config.Retries = 2                           // default
config.RetryDelay = 200 * time.Millisecond   // default
config.Failover = true                       // default
config.ConnectionTimeout = 2 * time.Second   // default
config.DownRetryDelay = 60 * time.Second     // default
config.PoolSize = 1                          // default
config.TcpKeepAlive = true                   // default
config.TcpKeepAlivePeriod = 60 * time.Second // default
config.TcpNoDelay = true                     // default
c := mc.NewMCwithConfig(server, username, password, config)
defer c.Quit()
```

**IF(direct)**
<p class="alert alert-info">
The values for `MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME`, and
`MEMCACHIER_PASSWORD` are listed on your
[cache overview page](https://www.memcachier.com/caches). Make sure to add them
to your environment.
</p>
**ENDIF**

After this, you can start writing cache code in your app:

```go
exp := 0 // seconds if less than 30 days, unix timestamp if more
flags := 0
cas := 0
_, err := c.Set("foo", "bar", flags, exp, cas)
if err != nil {
	fmt.Printf("Failed to set value: %s\n", err)
}

val, _, _, err := c.Get("foo")
if err != nil {
	fmt.Printf("Failed to fetch value: %s\n", err)
}
fmt.Printf("Got value: %s\n", val)
```

### Alternative client: `gomemcache`

We highly recommed to use the `mc` client since it was designed to work well
with MemCachier but using `gomemcache` is also possilbe. While `gomemcache` is
a popular memcache client it only supports the ASCII protocol. We have a fork
that allows you to use this client with MemCachier anyway.

To install our version of `gomemcache`:

```term
$ go get github.com/memcachier/gomemcache
```

Next, configure your memcached client in the following way:

```go
username := os.Getenv("MEMCACHIER_USERNAME")
password := os.Getenv("MEMCACHIER_PASSWORD")
servers := os.Getenv("MEMCACHIER_SERVERS")

mc := memcache.New(strings.Split(servers, ",")...)
mc.SetAuth(username, []byte(password))
```

**IF(direct)**
<p class="alert alert-info">
The values for `MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME`, and
`MEMCACHIER_PASSWORD` are listed on your
[cache overview page](https://www.memcachier.com/caches). Make sure to add them
to your environment.
</p>
**ENDIF**

After this, you can start writing cache code in your app:

```go
err := mc.Set(&memcache.Item{Key: "foo", Value: []byte("my value")})
if err != nil {
	fmt.Printf("Failed to set value: %s\n", err)
}

val, err := mc.Get("foo")
if err != nil {
	fmt.Printf("Failed to fetch value: %s\n", err)
}
fmt.Printf("Got value: %s\n", val)
```
