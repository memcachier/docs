---
title: "Documentation: Gin"
description: "Documentation for using MemCachier with Gin"
---

## Gin

**IF(direct)**
<div class="alert alert-info">
We’ve built a small Gin example here:
<a href="https://github.com/memcachier/examples-gin">MemCachier Gin sample app</a>.
<br>
Related tutorials:
<ul>
  <li><a href="https://devcenter.heroku.com/articles/gin-memcache">Scaling a Gin Application with Memcache on Heroku</a></li>
</ul>
</div>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Gin example.
><a class="github-source-code" href="http://github.com/memcachier/examples-gin">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-gin).
><br>
>We also have a tutorial on using Gin and MemCachier together
>[here](https://devcenter.heroku.com/articles/gin-memcache).
**ENDIF**

In Gin you can use the standard `mc` interface to get and set values
as described in our Go documentation to cache results of expensive
computations or database queries:

```go
package main

import (
  "os"
  "fmt"
  "github.com/memcachier/mc"
)

func main() {
  username := os.Getenv("MEMCACHIER_USERNAME")
  password := os.Getenv("MEMCACHIER_PASSWORD")
  servers := os.Getenv("MEMCACHIER_SERVERS")

  mcClient := mc.NewMC(servers, username, password)
  defer mcClient.Quit()

  _, err := mcClient.set("foo", "bar", 0, 0, 0)
  if err != nil {
    fmt.Printf("Failed to set value: %s\n", err)
  }

  val, _, _, err := c.Get("foo")
  if err != nil {
    fmt.Printf("Failed to fetch value: %s\n", err)
  }
  fmt.Printf("Got value: %s\n", val)
}
```

In addition there are two Gin specific ways to use Memcache:

1. Cache rendered views
2. Store sessions

### Cache rendered views

To cache rendered views you need the `gin-contrib/cache` library. Now you can
use the `CachePage` middleware like so:

```go
package main

import (
  "os"
  "github.com/gin-gonic/gin"
  "github.com/gin-contrib/cache"
  "github.com/gin-contrib/cache/persistence"
)

func main() {
	username := os.Getenv("MEMCACHIER_USERNAME")
  password := os.Getenv("MEMCACHIER_PASSWORD")
  servers := os.Getenv("MEMCACHIER_SERVERS")

  mcStore := persistence.NewMemcachedBinaryStore(servers, username, password, persistence.FOREVER)

	router := gin.New()
  router.GET("/", cache.CachePage(mcStore, persistence.DEFAULT, func(c *gin.Context) {
    // ...
  }))
}
```

Whenever the view changes, e.g., when the content changes, you need to make
sure to invalidate the cached view so it will be re-rendered.
This can be done by deleting the cached item (for the `root` route in this
case):

```go
mcStore.Delete(cache.CreateKey("/"))
```

### Storing Sessions in Memcache

**IF(heroku)**
On Heroku it is a good idea to store sessions in Memcache instead of in a file
on disk for two reasons:

1. Dynos only have an ephemeral filesystem that is not persisted across restarts.
2. You might have multiple dynos which will not share the same ephemeral filesystem.
**ENDIF**

Memcache works well for sessions that time out, however,
since Memcache is a cache and thus not persistent, saving long-lived
sessions in Memcache might not be ideal. For long-lived sessions consider a
permanent storage option such as your database.

To use sessions in Gin you need `gin-contrib/session`. You can easily add it
to your Gin app like so:

```go
package main

import (
  "os"
  "github.com/memcachier/mc"
  "github.com/gin-contrib/sessions"
  "github.com/gin-contrib/sessions/memcached"
)

func main() {
	username := os.Getenv("MEMCACHIER_USERNAME")
  password := os.Getenv("MEMCACHIER_PASSWORD")
  servers := os.Getenv("MEMCACHIER_SERVERS")

  mcClient := mc.NewMC(servers, username, password)
  defer mcClient.Quit()

	router := gin.New()
  sessionStore := memcached.NewMemcacheStore(mcClient, "", []byte("secret"))
  router.Use(sessions.Sessions("mysession", sessionStore))
}
```
