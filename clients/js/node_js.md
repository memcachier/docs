

<h2 id="node.js">Node.js</h2>

For Node.js we recommend the use of the
[memjs](https://github.com/alevy/memjs) client library. It is written
and supported by MemCachier itself! To install, use the [node package
manager (npm)](https://npmjs.org/):

```text
npm install memjs
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

We’ve built a small Node.js example here: [MemCachier Node.js sample
app](http://github.com/memcachier/examples-node).
