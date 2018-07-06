
Memcache is a technology that improves the performance and scalability of web
apps and mobile app backends. You should consider
using Memcache when your pages are loading too slowly or your app is
having scalability issues. Even for small sites, Memcache can make page loads
snappy and help future-proof your app.

This guide shows how to create a simple [Gin Gonic](https://gin-gonic.github.io/gin/)
application, deploy it to Heroku, then add Memcache to alleviate a
performance bottleneck.

>note
>The sample app in this guide can be seen running
>[here](https://memcachier-examples-gin.herokuapp.com/). You can
>[view the source code](http://github.com/memcachier/examples-gin) or
>deploy it with this Heroku Button:
>
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-gin)

## Prerequisites
Before you complete the steps in this guide, make sure you have all of the following:

* Familiarity with Go (and ideally Gin)
* A Heroku user account ([signup is free and instant](https://signup.heroku.com/signup/dc))
* Familiarity with the steps in [Getting Started on Heroku with Go](getting-started-with-go)
* Go, [govendor](https://github.com/kardianos/govendor), and the [Heroku CLI](heroku-cli) installed on your computer
* Make sure the `GOPATH` environment variable is set.

## Deploying a Gin application to Heroku

Gin is a minimalist framework that doesn't require an application skeleton.
Simply create a Go app and add `github.com/gin-gonic/gin` as a depenency
like so:

```term
$ cd $GOPATH/src
$ mkdir gin_memcache
$ cd gin_memcache
$ govendor init
$ govendor fetch github.com/gin-gonic/gin@v1.2
```

Now that we've installed the Gin framework, we can add our app code. We'll
create a page that calculates the largest prime number that's smaller than a
number a visitor submits.

Create `main.go` and paste the following code into it:

```go
package main

import (
  "net/http"
  "os"
  "strconv"

  "github.com/gin-gonic/gin"
)

func main() {
  port := os.Getenv("PORT")

  if port == "" {
    port = "3000"
  }

  router := gin.New()
  router.Use(gin.Logger())
  router.LoadHTMLGlob("templates/*.tmpl.html")
  router.Static("/static", "static")

  router.GET("/", func(c *gin.Context) {
    n := c.Query("n")
    if n == "" {
      // Render view
      c.HTML(http.StatusOK, "index.tmpl.html", nil)
    } else {
      i, err := strconv.Atoi(n)
      if err != nil || i < 1 || i > 10000 {
        // Render view with error
        c.HTML(http.StatusOK, "index.tmpl.html", gin.H{
          "error": "Please submit a valid number between 1 and 10000.",
        })
      } else {
        p := calculatePrime(i)
        // Render view with prime
        c.HTML(http.StatusOK, "index.tmpl.html", gin.H{"n": i, "prime": p})
      }
    }
  })

  router.Run(":" + port)
}

// Super simple algorithm to find largest prime <= n
func calculatePrime(n int) int {
  prime := 1
  for i := n; i > 1; i-- {
    isPrime := true
    for j := 2; j < i; j++ {
      if i%j == 0 {
        isPrime = false
        break
      }
    }
    if isPrime {
      prime = i
      break
    }
  }
  return prime
}
```

Now let's add a corresponding view. Create the file `templates/index.tmpl.html`
and paste the following code into it:

```html
{{ define "index.tmpl.html" }}
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">

    <title>Gin caching example</title>
  </head>

  <body>
    <div class="container">
      <h1>
        Gin caching example
      </h1>

      <p class="lead">For any number N (max 10000), we'll find the largest prime number
        less than or equal to N.
      </p>
      <!-- Form to submit a number -->
      <form class="form-inline" action="/">
        <input type="text" class="form-control" name="n" />
        <input type="submit" class="btn btn-primary" value="Find Prime" />
      </form>

      <hr>
      <!-- Show the result -->
      {{ if .prime }}
        <div class="alert alert-primary">
          <p class="lead">Largest prime less or equal than {{ .n }} is {{ .prime }}</p>
        </div>
      {{ end }}

      <!-- Error handling -->
      {{ if .error }}
      <div class="alert alert-danger">
        <p class="lead">{{ .error }}</p>
      </div>
      {{ end }}

    </div>
  </body>
</html>
{{ end }}
```

You now have a working app that you can start by running `go run main.go`.

For the app to work on Heroku, we need to create a [`Procfile`](procfile) that
indicates how to run it:

```term
$ echo web: gin_memcache > Procfile
```

To deploy the app to Heroku, it needs to live in a Git repository. First, create a `.gitignore` file:

```term
$ echo 'vendor/*' > .gitignore
$ echo '!vendor/vendor.json' >> .gitignore
```

Then, create the repository and commit the initial state of the app:

```term
$ git init
$ git add .
$ git commit -m 'Initial gin app'
```

Finally, create the Heroku app, push your code to it, and explore the running app:

```term
$ heroku create
$ git push heroku master
$ heroku open
```

## Adding caching to Gin

Memcache is an in-memory, distributed cache. Its primary API consists of two
operations: `SET(key, value)` and `GET(key)`.
Memcache is like a hashmap (or dictionary) that is spread across
multiple servers, where operations are still performed in constant
time.

The most common use for Memcache is to cache expensive database
queries and HTML renders so that these expensive operations don’t
need to happen over and over again.

### Set up Memcache

To use Memcache in Gin, you first need to provision an actual Memcache
cache. You can easily get one for free with the
[MemCachier add-on](https://elements.heroku.com/addons/memcachier):

```term
$ heroku addons:create memcachier:dev
```

This adds three config vars to your Heroku application,
`MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME`, and `MEMCACHIER_PASSWORD`, so you
can connect to your cache.

To use the cache in Gin, we need to install `mc` with `govendor`:

```term
$ govendor fetch github.com/memcachier/mc
```

and configure it in `main.go`:

```go
package main

import (
  // ...
  "github.com/memcachier/mc"
)

func main() {
  username := os.Getenv("MEMCACHIER_USERNAME")
  password := os.Getenv("MEMCACHIER_PASSWORD")
  servers := os.Getenv("MEMCACHIER_SERVERS")

  mcClient := mc.NewMC(servers, username, password)
  defer mcClient.Quit()
  // ...
}
// ...
```

### Caching expensive computations

There are two reasons why caching the results of expensive computations is a good idea:

1. Pulling the results from the cache is much faster, resulting in a better
user experience.
2. Expensive computations use significant CPU resources, which can slow down the
rest of your app.

Our prime number calculator doesn't really have any expensive computations,
because we limit the input value to 10000. For the sake of the tutorial,
however, let's assume that calculating the prime is an expensive computation
we would like to cache.

To achieve this, let's modify the `GET` route in `main.go` and replace

```go
// ...
p = calculatePrime(i)
// ...
```

with

```go
// ...
key := "prime." + strconv.Itoa(i)
p := 0
// Look in cache
val, _, _, err := mcClient.Get(key)
if err != nil {
  // Prime not in cache (calculate and store)
  p = calculatePrime(i)
  val = strconv.Itoa(p)
  mcClient.Set(key, val, 0, 0, 0)
} else {
  // Found it!
  p, _ = strconv.Atoi(val)
}
// ...
```

Deploy these changes to Heroku and submit some numbers to find primes:

```term
$ git commit -am 'Add caching'
$ git push heroku master
```

The page should work just as before. However, under the hood, already calculated
primes are now cached. To see what's going on in your cache, open the MemCachier
dashboard:

```term
$ heroku addons:open memcachier
```

On the dashboard you can refresh the stats each time you request a prime. The
first time you enter a number, the `get misses` will increase. For any subsequent
request of the same number, you should get an additional `get hit`.

### Caching rendered views

Rendering HTML views is generally an expensive computation, and you should
cache rendered views whenever possible. In Gin, you can achieve this easily
with `gin-contrib/cache` library. Fetch the library with `govendor`:

```term
$ govendor fetch github.com/gin-contrib/cache
```

Now we can cache rendered views in `main.go` like so:

```go
package main

import (
  // ...
  "github.com/gin-contrib/cache"
  "github.com/gin-contrib/cache/persistence"
  // ...
)

func main() {
  // ...
  mcStore := persistence.NewMemcachedBinaryStore(servers, username, password, persistence.FOREVER)

  router.GET("/", cache.CachePage(mcStore, persistence.DEFAULT, func(c *gin.Context) {
    // ...
  }))
  // ...
}
// ...
```

This is easy enough and works well. However, if the view ever changes, we need to
be careful. To illustrate the case of a changing page, let's add a "Like" button
to each number and its calculated largest prime. Let's put the button just below
the calculated prime in the `index.tmpl.html` file:

```html
<!-- ... -->

<!-- Show the result -->
{{ if .prime }}
  <div class="alert alert-primary">
    <p class="lead">Largest prime less or equal than {{ .n }} is {{ .prime }}</p>
    <p>Likes: {{ .likes }}</p>
  </div>
  <form method='POST'>
    <input type="hidden" name="n" value="{{ .n }}" />
    <input type="submit" class="btn btn-primary" value="Like!" />
  </form>
{{ end }}

<!-- ... -->
```

We now need to create a controller for the `POST` route in `main.go` and store
the posted like in a variable.

> note
> Storing likes in a variable is a bad idea. Each time the app restarts, it wipes
> all likes. We do this here only for convenience. In a production application, you
> should store such information in a database.

```go
// ...
func main() {
  // ...

  likes := make(map[string]int)
  router.POST("/", func(c *gin.Context){
    n := c.PostForm("n")
    likes[n] += 1
    c.Redirect(http.StatusMovedPermanently, "/?n=" + n)
  })

  router.GET("/", cache.CachePage(mcStore, persistence.DEFAULT, func(c *gin.Context) {
    // ...
  }))
  //...
}
// ...
```

In addition, we also need to make sure the likes are passed to the `HTML`
function in the `GET` controller:

```go
// ...

// Render view with prime
c.HTML(http.StatusOK, "index.tmpl.html", gin.H{"n": i, "prime": p, "likes": likes[n] })

// ...
```

To illustrate the problem with changing pages, let's commit our current
implementation and test it:

```term
$ git commit -am 'Add view caching'
$ git push heroku master
```

If you submit a number, you will now get the largest prime below it, together with a Like button. However, when you click **Like!**, the like count doesn't
increase. This is because the view is cached.

To resolve this, we need to **invalidate** the cached view whenever it is updated:

```go
// ...

router.POST("/", func(c *gin.Context){
  n := c.PostForm("n")
  likes[n] += 1
  mcStore.Delete(cache.CreateKey("/?n=" + n))
  c.Redirect(http.StatusMovedPermanently, "/?n=" + n)
})

// ...
```

Deploy again to Heroku:

```term
$ git commit -am 'Fix view caching'
$ git push heroku master
```

Now you can see the number of likes increase.

### Session Caching

On Heroku, it's not advisable to store session information on disk, because
dynos have an ephemeral filesystem that doesn't persist across restarts.

Memcache works well for storing information for short-lived sessions that time
out. However, because Memcache is a cache and therefore not persistent,
long-lived sessions are better suited to permanent storage options, such as
your database.

To use sessions in Gin, you need `gin-contrib/session`:

```term
$ govendor fetch github.com/gin-contrib/sessions
$ govendor fetch github.com/gin-contrib/sessions/memcached
```

The configuration in `main.go` is easy enough:

```go
package main

import (
	// ...
  "github.com/gin-contrib/sessions"
  "github.com/gin-contrib/sessions/memcached"
  // ...
)

func main() {
  // ...
  // add below `router := gin.New()`
  sessionStore := memcached.NewMemcacheStore(mcClient, "", []byte("secret"))
  router.Use(sessions.Sessions("mysession", sessionStore))
  // ...
}
// ...
```

Now you can now use sessions as you please. For more information about session
usage in Gin, check out the
[gin-contrib/sessions README](https://github.com/gin-contrib/sessions#memcached-binary-protocol-with-optional-sasl-authentication).

## Further reading & resources

* [MemCachier Add-on Page](https://elements.heroku.com/addons/memcachier)
* [MemCachier Documentation](memcachier)
* [Advance Memcache Usage](advanced-memcache)
* [Getting Started on Heroku with Go](getting-started-with-go)
