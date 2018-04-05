
Memcached is a technology that helps web apps and mobile app backends
in two main ways: *performance* and *scalability*. You should consider
using memcache when your pages are loading too slowly or your app is
having scalability issues. Even for small sites it can be a great
technology, making page loads snappy and future proofing for scale.

This guide will show you how to create a simple [Express 4](https://expressjs.com/)
application, deploy it on Heroku, then add caching with Memcache to alleviate a
performance bottleneck.

>note
>The sample sample app built in this guide can be seen running
>[here](https://memcachier-examples-expressjs.herokuapp.com/).<br>
><a class="github-source-code" href="http://github.com/memcachier/examples-expressjs">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-expressjs)

## Prerequisites

* Node.js (and ideally some Express.js) knowledge.
* A Heroku user account. [Signup is free and instant.](https://signup.heroku.com/signup/dc)
* Familiarity with the [Getting Started on Heroku with Node.js](getting-started-with-nodejs)
guide, with `npm`, and the [Heroku CLI](https://cli.heroku.com) installed
on your computer.

## Creating a Express.js application on Heroku

Express.js is a very minimalist framework and as such there is no need for an
application template or bootstrapping of a skeleton app. Simply create a node.js
app and add `express` as a depenency:

```term
$ mkdir express_memcache
$ cd express_memcache
$ npm init
  # choose a package name and make sure the entry point is app.js
$ npm install express
```

To make our life a bit easier we will use a template engine. In this tutorial
we use `ejs` but you could also use `mustache`, `pug`, or `nunjucks` if you
prefer. So, let's add the template engine to our app:

```term
$ npm install ejs
```

Now that we have installed all the packages we need, we can create our app. We
will create a page that calculates the largest prime smaller than a number
a visitor submits. Create `app.js` and fill it with the following code:

```js
var express = require("express");
var app = express();

// Set template engine
app.set('view engine', 'ejs')

// Bind the app to a specified port
var port = process.env.PORT || 3000;
app.listen(port);
console.log("Listening on port " + port);

// Super simple algorithm to find largest prime <= n
var calculatePrime = function(n){
  var prime = 1;
  for (var i = n; i > 1; i--) {
    var is_prime = true;
    for (var j = 2; j < i; j++) {
      if (i % j == 0) {
        is_prime = false;
        break;
      }
    }
    if (is_prime) {
      prime = i;
      break;
    }
  }
  return prime;
}

// Set up the GET route
app.get('/', function (req, res) {
  if(req.query.n) {
    // Calculate prime and render view
    var prime = calculatePrime(req.query.n);
    res.render('index', { n: req.query.n, prime: prime});
  }
  else {
    // Render view without prime
    res.render('index', {});
  }
});
```

Let's add the correspondig view. Create the file `views/index.ejs` and fill it
with the following `ejs`-branded html code:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">

    <title>Express.js caching example</title>
  </head>

  <body>
    <div class="container">
      <h1>
        Express.js caching example
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
      <% if (locals.prime) { %>
        <div class="alert alert-primary">
          <p class="lead">Largest prime less or equal than <%= n %> is <%= prime %></p>
        </div>
      <% } %>

      <!-- TODO: Error handling -->

    </div>
  </body>
</html>
```

Now you already have a working app which you can start with `node app.js`. For
it to work on Heroku we will need to create a [`Procfile`](procfile) that
contains the instructions on how to start the app:

```term
$ echo web: node app.js > Procfile
```

It is time to create a Heroku app. For this we need to create a git repository
first. Let's start by createing a `.gitignore` file that contains:

```term
$ echo node_modules/ > .gitignore
```

Then, create the git repository and commit the initial state of the app:

```term
$ git init
$ git add .
$ git commit -m 'Initial express app'
```

Finally, create the Heroku app, push the changes, and explore the running app:

```term
$ heroku create
$ heroku config:add NODE_ENV=production
$ git push heroku master
$ heroku open
```

## Learn to write Express.js middleware

Our prime calculating app works but has one mayor flaw: A user is able to submit
invalid input, i.g., a string of letters. We need to validate the input and to
do so we will create an Express middleware.

> note
> Note that there are valication middleware packages available for Express and
> in general you should use those. Here we create our own validation because
> our case is super simple and it serves as a gentle introduction into creating
> Express middleware which we will need later.

Express middleware is basically a function that takes a request, a response,
and a next function. The function can then modify the request and response
object at will and either call the next function to execute the next middleware
or call return to terminate the chain of executing middleware prematurely and
return a response.

For our purposes we create a validation middleware function that parses the
submitted query, checks if it is a number below 10000, and if this is the case
it will call next. If not, it will return an error response. We will add this
function to `app.js` and call it when processing the `GET` route:

```js
// ...

var validate = function(req, res, next) {
  if(req.query.n) {
    number = parseInt(req.query.n, 10);
    if(isNaN(number) || number < 1 || number > 10000){
      res.render('index', {error: 'Please submit a valid number between 1 and 10000.'});
      return;
    }
    req.query.n = number;
  }
  next();
}

app.get('/', validate, function (req, res) {
  // ...
```

The validation middleware may return an error message which we now need to
display in the `index.ejs` view:

```html
<!-- Show the result -->
<!-- ... -->

<!-- Error handling -->
<% if (locals.error) { %>
  <div class="alert alert-danger">
    <p class="lead"><%= error %></p>
  </div>
<% } %>
```

Let's deploy the changes submit some invalid queries:

```term
$ git commit -am 'Add input validation'
$ git push heroku master
```

## Speed up the application with Memcache

Memcache is an in-memory, distributed cache. The primary API for
interacting with it are `SET(key, value)` and `GET(key)` operations.
Memcache is like a hashmap (or dictionary) that is spread across
multiple servers, where operations are still performed in constant
time.

The most common usage of memcache is to cache expensive computations and
database queries as well as rendered partials or views such that these
expensive operations don’t need to happen over and over again.

### Set up memcache

In order to use memcache in your Express app you first need to have an actual
memcached cache. You can easily get one for free with the
[MemCachier addon](https://elements.heroku.com/addons/memcachier):

```term
$ heroku addons:create memcachier:dev
```

This will add three environment variables to your Heroku application,
`MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME`, and `MEMCACHIER_PASSWORD`, so you
can connect to your cache.

To use the cache we need to install `memjs` with

```term
$ npm install memjs
```

and configure it in `app.js`:

```js
// ...

var memjs = require('memjs')
var mc = memjs.Client.create(process.env.MEMCACHIER_SERVERS, {
  failover: true,  // default: false
  timeout: 1,      // default: 0.5 (seconds)
  keepAlive: true  // default: false
})

// ...
```

### Cache expensive computations

There are two reasons why caching expensive computations is a good idea:

1. The computation takes a lot of time and getting it from the cache is faster.
2. The computation uses too many CPU cycles and slows down the rest of the app.

Our little prime number calculator does not really have an expensive computation
as we limit the input to 10000. For the sake of this example however, let's assume
that calulating the prime is an expensive computation we would like to cache.
To achieve this, let's modify the `GET` route in `app.js` as follows:

```js
// ...

app.get('/', validate, function (req, res) {
  if(req.query.n) {
    var prime;
    var prime_key = 'prime.' + req.query.n;
    // Look in cache
    mc.get(prime_key, function(err, val) {
      if(err == null && val != null) {
        // Found it!
        prime = parseInt(val)
      }
      else {
        // Prime not in cache (calculate and store)
        prime = calculatePrime(req.query.n)
        mc.set(prime_key, '' + prime, {expires:0}, function(err, val){})
      }
      // Render view with prime
      res.render('index', { n: req.query.n, prime: prime });
    })
  }
  else {
    // Render view without prime
    res.render('index', {});
  }
});

// ...
```

Deploy it to Heroku and submit some numbers to find primes:

```term
$ git commit -am 'Add caching'
$ git push heroku master
```

The page should work just as before. However, under the hood already calculated
primes are now cached. To see what is going on in your cache open the MemCachier
dashboard:

```term
$ heroku addons:open memcachier
```

On the dashboard you can refresh the stats each time you request a prime. The
first time you enter a number the get misses will increase, for any subsequent
request of the same number you should get an additional get hit.

### Cache rendered views

Rendering HTML views is generally an expensive compuation and as such we should
cache it whenever possible. In Express this can be easily achieved by writing a
middleware. Let's add a `cacheView` middleware function to `app.js` that checks
for a given URL (including query parameters) if the view is in the cache. If it
is, the view is sent immediately. If not, we wrap the send function in the
response object to cache the rendered view and call the `next` function.

```js
// ...

var cacheView = function(req, res, next) {
  var view_key = '_view_cache_' + req.originalUrl || req.url;
  mc.get(view_key, function(err, val) {
    if(err == null && val != null) {
      // Found the rendered view -> send it immediately
      res.send(val.toString('utf8'));
      return;
    }
    // Cache the rendered view for future requests
    res.sendRes = res.send
    res.send = function(body){
      mc.set(view_key, body, {expires:0}, function(err, val){})
      res.sendRes(body);
    }
    next();
  });
}

app.get('/', validate, cacheView, function (req, res) {
  // ...
```

This is easy enough and works well. However, if the view ever changes we need
to be careful. To illustrate the case of a changing page, let's add a Like button
to each number and its calculated largest prime. Let's put the button just below
the calculated prime in the `index.ejs` file:

```html
<!-- ... -->

<!-- Show the result -->
<% if (locals.prime) { %>
  <div class="alert alert-primary">
    <p class="lead">Largest prime less or equal than <%= n %> is <%= prime %></p>
    <p>Likes: <%= likes %></p>
    <form method='POST'>
      <input type="hidden" name="n" value="<%= n %>" />
      <input type="submit" class="btn btn-primary" value="Like!" />
    </form>
  </div>
<% } %>

<!-- ... -->
```

The like is submitted via `POST` request and to parse its input we will need
the `body-parser` package:

```term
$ npm install body-parser
```

We can now create a controller for the `POST` route in `app.js` and store the
posted like in a variable.

> note
> Storing likes in a variable is a bad idea. Each time the app restarts it wipes
> all likes. We just do this here for convenience. In a serious application you
> would store such information in a database.

```js
// ...

var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Like storage (in a serious app you should use a permanent storage like a database)
var likes = {}

app.post('/', function (req, res) {
  likes[req.query.n] = (likes[req.query.n] || 0) + 1
  res.redirect('/?n=' + req.query.n)
});

// ...
```

In addition, we also need to make sure the likes are passed to the render
function in the `GET` controller:

```js
// ...

// Render view with prime
res.render('index', { n: req.query.n, prime: prime, likes: likes[req.query.n] || 0 });

// ...
```

To illustrate the problem with changing pages, let's commit our current
implementation and test it:

```term
$ git commit -am 'Add view caching'
$ git push heroku master
```

If you submit a number you will now get the largest prime below it together with
a Like button. However, when you click on `Like!` the like count will not
increase. This is because the view is cached.

So we need to invalidate the cached view whenever it is updated:

```js
// ...

app.post('/', function (req, res) {
  mc.delete('_view_cache_/?n=' + req.body.n, function(err, val){});
  likes[req.query.n] = (likes[req.query.n] || 0) + 1
  res.redirect('/?n=' + req.query.n)
});

// ...
```

Deploy again to Heroku:

```term
$ git commit -am 'Fix view caching'
$ git push heroku master
```

Now you will see the likes increasing.

### Session Caching

On Heroku it is a good idea to store sessions in memcache instead of in a file
on disk for two reasons:

1. Dynos only have an ephemeral filesystem that is not persisted across restarts.
2. You might have multiple dynos which will not share the same ephemeral filesystem.

Memcache works well for sessions that time out, however,
since memcache is a cache and thus not persistent, saving long-lived
sessions in memcache might not be ideal. For long-lived sessions consider a
permanent storage option such as your database.

To use sessions in Express you need `express-session` and to back it by your
memcache you need `connect-memjs`:

```term
$ npm install express-session connect-memjs
```

The configuration in `app.js` is easy enough:

```js
//...

var session = require('express-session');
var MemcachedStore = require('connect-memjs')(session);

// Session config
app.use(session({
  secret: 'ClydeIsASquirrel',
  resave: 'false',
  saveUninitialized: 'false',
  store: new MemcachedStore({
    servers: [process.env.MEMCACHIER_SERVERS],
    prefix: '_session_'
  })
}));

//...
```

Now you can now use sessions as you please. For more information about session
usage in Express, check out the
[express-session documentation](https://www.npmjs.com/package/express-session).

## Further reading & resources

* [MemCachier Add-on Page](https://elements.heroku.com/addons/memcachier)
* [MemCachier Documentation](memcachier)
* [Advance Memcache Usage](advanced-memcache)
* [Getting Started on Heroku with Node.js](getting-started-with-nodejs)
