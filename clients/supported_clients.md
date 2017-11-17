
## Client library support

MemCachier will work with any memcached binding that supports [SASL
authentication](https://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer)
and the [binary
protocol](https://github.com/memcached/memcached/wiki/BinaryProtocolRevamped). We
have tested MemCachier with the following language bindings, although the
chances are good that other SASL binary protocol packages will also work.

<table class="table table-striped table-bordered">
<tbody>
<tr>
<th>Language</th>
<th>Bindings</th>
</tr>
<tr>
<td>Ruby</td>
<td><a href="https://github.com/mperham/dalli">dalli</a></td>
</tr>
<tr>
<td>Python</td>
<td>
  <a href="http://sendapatch.se/projects/pylibmc/">pylibmc</a>
  <b>or</b>
  <a href="https://github.com/jaysonsantos/python-binary-memcached">python-binary-memcached</a>
</td>
</tr>
<tr>
<td>Django</td>
<td>
  (
    <a href="http://sendapatch.se/projects/pylibmc/">pylibmc</a>
    <b>and</b>
    <a href="https://github.com/jbalogh/django-pylibmc">django-pylibmc</a>
  )
  <b>or</b>
  (
    <a href="https://github.com/jaysonsantos/python-binary-memcached">python-binary-memcached</a>
    <b>and</b>
    <a href="https://github.com/jaysonsantos/django-bmemcached">django-bmemcached</a>
  )
  <b>or</b>
  (
    <a href=https://github.com/memcachier/django-ascii>django-ascii</a>
  )
</td>
</tr>
<tr>
<td>PHP</td>
<td>
  <a href="http://www.php.net/manual/en/book.memcached.php">php-memcached</a>
  <b>or</b>
  <a href="http://github.com/ronnywang/PHPMemcacheSASL">PHPMemcacheSASL</a>
</td>
</tr>
<tr>
<td>Node.js</td>
<td>
  <a href="https://github.com/alevy/memjs">memjs</a>
</td>
</tr>
<tr>
<td>Java</td>
<td>
  <a href="http://code.google.com/p/spymemcached/">SpyMemcached</a>
  <b>or</b>
  <a href="https://code.google.com/p/xmemcached/">XMemcached</a>
</td>
</tr>
<tr>
<td>Go</td>
<td><a href="https://github.com/memcachier/mc">mc</a></td>
</tr>
<tr>
<td>Haskell</td>
<td><a href="http://hackage.haskell.org/package/memcache">memcache</a></td>
</tr>
</tbody>
</table>
