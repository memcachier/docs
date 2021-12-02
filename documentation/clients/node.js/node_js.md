**IF(direct)**
---
title: "Documentation: Node.js"
description: "Documentation for using MemCachier with Node.js"
---
**ENDIF**

## Node.js

For Node.js we recommend the use of the
[memjs](https://github.com/memcachier/memjs) client library. It is written
and supported by MemCachier itself! To install, use [npm](https://npmjs.org/):

```term
$ npm install memjs
```

Using it is straight-forward as memjs understands the `MEMCACHIER_SERVERS`,
`MEMCACHIER_USERNAME` and `MEMCACHIER_PASSWORD`
**IF(heroku)**
environment variables that the MemCachier add-on setups.
**ENDIF**
**IF(direct)**
environment variables. The values for these variables are listed on your
[cache overview page](https://www.memcachier.com/caches).
**ENDIF**
For example:

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
