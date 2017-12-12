
## Node.js

**IF(direct)**
<p class="alert alert-info">
We’ve built a small Node.js example here:
<a href="http://github.com/memcachier/examples-node">MemCachier Node.js sample app</a>.
</p>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Node.js example.
><a class="github-source-code" href="https://github.com/memcachier/examples-node">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-node).
**ENDIF**

For Node.js we recommend the use of the
[memjs](https://github.com/alevy/memjs) client library. It is written
and supported by MemCachier itself! To install, use the [node package
manager (npm)](https://npmjs.org/):

```term
$ npm install memjs
```

Using it is straight-forward as memjs understands the `MEMCACHIER_SERVERS`,
`MEMCACHIER_USERNAME` and `MEMCACHIER_PASSWORD`
environment variables that the MemCachier add-on setups. For example:

```javascript
var memjs = require('memjs')
var mc = memjs.Client.create()
mc.get('hello', function(val) {
    alert(val)
})
```
