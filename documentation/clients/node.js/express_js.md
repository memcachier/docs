
## Espress.js

**IF(direct)**
<div class="alert alert-info">
We’ve built a small Express.js example here:
<a href="http://github.com/memcachier/examples-expressjs">MemCachier Express.js sample app</a>.
<br>
Related tutorials:
<ul>
  <li><a href="https://devcenter.heroku.com/articles/expressjs-memcache">Scaling an Express.js Application with Memcache on Heroku</a></li>
  <li><a href="https://blog.memcachier.com/2018/07/09/scaling-an-express-application-with-memcache-on-amazon-elastic-beanstalk/">Scaling an Express.js Application with Memcache on Amazon Elastic Beanstalk</a></li>
</ul>
</div>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Express.js example.
><a class="github-source-code" href="https://github.com/memcachier/examples-expressjs">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-expressjs).
><br>
>We also have a tutorial on using Express.js with MemCachier
>[here](https://devcenter.heroku.com/articles/expressjs-memcache).
**ENDIF**

In Express.js you can use the standard `memjs` interface to get and set values
as described in our Node.js documentation to cache expensive
computations or database queries:

```javascript
var memjs = require('memjs')

var mc = memjs.Client.create(process.env.MEMCACHIER_SERVERS, {
  failover: true,  // default: false
  timeout: 1,      // default: 0.5 (seconds)
  keepAlive: true  // default: false
})

mc.set('hello', 'memcachier', {expires:0}, function(err, val) {
  if(err != null) {
    console.log('Error setting value: ' + err)
  }
})

mc.get('hello', function(err, val) {
  if(err != null) {
    console.log('Error getting value: ' + err)
  }
  else {
    console.log(val.toString('utf8'))
  }
})
```

In addition there are two Express.js specific ways to use Memcache:

1. Cache rendered views
2. Store sessions

### Cache rendered views

To cache rendered views it is best to create an Express.js middleware function
as such:

```javascript
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
```

If you use the `cacheView` middleware you need to take care to invalidate the
cache whenever the view needs to be re-rendered, e.g., when the content changes.
This can be done by deleting the cached item:

```javascript
mc.delete('_view_cache_/?n=' + req.body.n, function(err, val){/* handle error */});
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

To use sessions in Express you need `express-session` and to store them in
Memcache you need `connect-memjs`:

```term
$ npm install express-session connect-memjs
```

Then you can configure sessions in your app:

```javascript
var session = require('express-session');
var MemcachedStore = require('connect-memjs')(session);
var express = require("express");
var app = express();

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
```
