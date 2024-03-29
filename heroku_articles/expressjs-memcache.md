
Memcache is a technology that improves the performance and scalability of web
apps and mobile app backends. You should consider
using Memcache when your pages are loading too slowly or your app is
having scalability issues. Even for small sites, Memcache can make page loads
snappy and help future-proof your app.

This guide shows how to create a simple [Express 4](https://expressjs.com/)
application, deploy it to Heroku, then add Memcache to alleviate a
performance bottleneck.

>note
>The sample app in this guide can be seen running
>[here](https://memcachier-examples-expressjs.herokuapp.com/). You can
>[view the source code](http://github.com/memcachier/examples-expressjs) or
>deploy it with this Heroku Button:
>
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-expressjs)

## Prerequisites
Before you complete the steps in this guide, make sure you have all of the following:

* Familiarity with Node.js (and ideally Express.js)
* A Heroku user account ([signup is free and instant](https://signup.heroku.com/signup/dc))
* Familiarity with the steps in [Getting Started on Heroku with Node.js](getting-started-with-nodejs)
* Node.js, `npm`, and the [Heroku CLI](heroku-cli) installed
on your computer.

## Deploying an Express.js application to Heroku

Express.js is a minimalist framework that doesn't require an
application skeleton. Simply create a Node.js
app and add `express` as a depenency like so:

```term
$ mkdir express_memcache
$ cd express_memcache
$ npm init
  # choose a package name and make sure the entry point is app.js
$ npm install express
```

To simplify development, we'll use a template engine. This tutorial uses `ejs`, but you can use whichever engine you prefer, including `mustache`, `pug`, or `nunjucks`.

```term
$ npm install ejs
```

Now that we've installed all the packages we need, we can add our app code. We'll create a page that calculates the largest prime number that's smaller than a number a visitor submits.

Create `app.js` and paste the following code into it:

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

Now let's add a corresponding view. Create the file `views/index.ejs` and paste the following `ejs`-enhanced HTML into it:

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

You now have a working app that you can start by running `node app.js`.

For the app to work on Heroku, we need to create a [`Procfile`](procfile) that indicates how to run it:

```term
$ echo web: node app.js > Procfile
```

To deploy the app to Heroku, it needs to live in a Git repository. First, create a `.gitignore` file:

```term
$ echo node_modules/ > .gitignore
```

Then, create the repository and commit the initial state of the app:

```term
$ git init
$ git add .
$ git commit -m 'Initial express app'
```

Finally, create the Heroku app, push your code to it, and explore the running app:

```term
$ heroku create
$ heroku config:add NODE_ENV=production
$ git push heroku master
$ heroku open
```

## Learn to write Express.js middleware

Our prime-calculating app works, but it has one major flaw: a user can submit
invalid input, such as a string of letters. To validate the input, we'll create **middleware** in Express.

> note
> There are several validation middleware packages available for Express, and
> you should use one of those in most cases. In this tutorial, we create our own validation for demonstration purposes.

Express middleware typically consists of a chain of functions that inspect and potentially modify the details of a request and its corresponding response. Each function takes three parameters:

* The `request` object
* The `response` object
* A `next` function that represents the next middleware function in the chain

Each middleware function can modify the `request` and `response`
objects as necessary. After doing so, it can either call the `next` middleware function or `return` to terminate the chain prematurely.

For our app, we create a validation middleware function that parses the submitted query and checks whether it's a number below 10000.

* If it is, the function calls `next`.
* If it isn't, the function `return`s an error response.

Add this function to `app.js` and call it when processing the `GET` route:

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

The validation middleware might return an error message, which we need to
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

Commit and deploy your changes:

```term
$ git commit -am 'Add input validation'
$ git push heroku master
```

Open the app and submit some invalid queries to see the error message in action.

## Adding caching to Express

Memcache is an in-memory, distributed cache. Its primary API consists of two operations: `SET(key, value)` and `GET(key)`.
Memcache is like a hashmap (or dictionary) that is spread across
multiple servers, where operations are still performed in constant
time.

The most common use for Memcache is to cache expensive database
queries and HTML renders so that these expensive operations don’t
need to happen over and over again.

### Set up Memcache

To use Memcache in Express, you first need to provision an actual Memcache
cache. You can easily get one for free with the
[MemCachier add-on](https://elements.heroku.com/addons/memcachier):

```term
$ heroku addons:create memcachier:dev
```

This adds three config vars to your Heroku application,
`MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME`, and `MEMCACHIER_PASSWORD`, so you can connect to your cache.

To use the cache in Express, we need to install `memjs` with `npm`:

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

### Caching expensive computations

There are two reasons why caching the results of expensive computations is a good idea:

1. Pulling the results from the cache is much faster, resulting in a better user experience.
2. Expensive computations use significant CPU resources, which can slow down the rest of your app.

Our prime number calculator doesn't really have any expensive computations, because we limit the input value to 10000. For the sake of the tutorial, however, let's assume
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
        mc.set(prime_key, '' + prime, {expires:0}, function(err, val){/* handle error */})
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

Rendering HTML views is generally an expensive compuation, and you should
cache rendered views whenever possible. In Express, you can achieve this easily with middleware. Let's add a `cacheView` middleware function to `app.js` that checks whether the view for a given URL (including query parameters) is in the cache.

* If it is, the view is sent immediately from the cache.
* If not, we wrap the `send` function in the response object to cache the rendered view and call the `next` function.

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
      mc.set(view_key, body, {expires:0}, function(err, val){/* handle error */})
      res.sendRes(body);
    }
    next();
  });
}

app.get('/', validate, cacheView, function (req, res) {
  // ...
```

This is easy enough and works well. However, if the view ever changes, we need to be careful. To illustrate the case of a changing page, let's add a "Like" button
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

The like is submitted via `POST` request, and to parse its input we need
the `body-parser` package:

```term
$ npm install body-parser
```

We can now create a controller for the `POST` route in `app.js` and store the
posted like in a variable.

> note
> Storing likes in a variable is a bad idea. Each time the app restarts, it wipes
> all likes. We do this here only for convenience. In a production application, you
> should store such information in a database.

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

In addition, we also need to make sure the likes are passed to the `render`
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

If you submit a number, you will now get the largest prime below it, together with a Like button. However, when you click **Like!**, the like count doesn't
increase. This is because the view is cached.

To resolve this, we need to **invalidate** the cached view whenever it is updated:

```js
// ...

app.post('/', function (req, res) {
  mc.delete('_view_cache_/?n=' + req.body.n, function(err, val){/* handle error */});
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

Now you can see the number of likes increase.

### Session Caching

On Heroku, it's not advisable to store session information on disk, because
dynos have an ephemeral filesystem that doesn't persist across restarts.

Memcache works well for storing information for short-lived sessions that time
out. However, because Memcache is a cache and therefore not persistent,
long-lived sessions are better suited to permanent storage options, such as
your database.

To use sessions in Express, you need `express-session`. To store the sessions
in Memcache, you need `connect-memjs`:

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
