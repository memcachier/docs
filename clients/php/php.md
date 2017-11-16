

<h2 id="php">PHP</h2>

We recommended you use the [PHP Memcached
client](http://www.php.net/manual/en/book.memcached.php) to connect with
MemCachier. It supports the full protocol and has great performance. We also
recommend that you use the [composer dependency
manager](https://getcomposer.org/) for PHP, although that is up to you.

It can be difficult to get the memcached client to work as it requires that you
build it against a version of libmemcached (a C library that the PHP client
relies upon) that support SASL authentication, which often isn't enabled by
default. If you have trouble, please open a [support
ticket](http://support.memcachier.com/) with us. Alternatively, you could use a
[pure PHP client](#php-memcachesasl) that MemCachier supports, instructions on
how are [here](#php-memcachesasl).

First, if using composer, you'll need to modify your `composer.json` file to
include the module:

```js
{
    "require": {
        "php": ">=5.3.2",
        "ext-memcached": "*"
    }
}
```

Then, you can connect to MemCachier using the client:

```php
require 'vendor/autoload.php';

// create a new persistent client
$m = new Memcached("memcached_pool");
$m->setOption(Memcached::OPT_BINARY_PROTOCOL, TRUE);

// some nicer default options
// - nicer TCP options
$m->setOption(Memcached::OPT_TCP_NODELAY, TRUE);
$m->setOption(Memcached::OPT_NO_BLOCK, FALSE);
// - timeouts
$m->setOption(Memcached::OPT_CONNECT_TIMEOUT, 2000);    // ms
$m->setOption(Memcached::OPT_POLL_TIMEOUT, 2000);       // ms
$m->setOption(Memcached::OPT_RECV_TIMEOUT, 750 * 1000); // us
$m->setOption(Memcached::OPT_SEND_TIMEOUT, 750 * 1000); // us
// - better failover
$m->setOption(Memcached::OPT_DISTRIBUTION, Memcached::DISTRIBUTION_CONSISTENT);
$m->setOption(Memcached::OPT_LIBKETAMA_COMPATIBLE, TRUE);
$m->setOption(Memcached::OPT_RETRY_TIMEOUT, 2);
$m->setOption(Memcached::OPT_SERVER_FAILURE_LIMIT, 1);
$m->setOption(Memcached::OPT_AUTO_EJECT_HOSTS, TRUE);

// setup authentication
$m->setSaslAuthData( <MEMCACHIER_USERNAME>
                   , <MEMCACHIER_PASSWORD> );

// We use a consistent connection to memcached, so only add in the
// servers first time through otherwise we end up duplicating our
// connections to the server.
if (!$m->getServerList()) {
    // parse server config
    $servers = explode(",", <MEMCACHIER_SERVERS>);
    foreach ($servers as $s) {
        $parts = explode(":", $s);
        $m->addServers($parts[0], $parts[1]);
    }
}
```

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and
`<MEMCACHIER_PASSWORD>` are listed on your [cache overview
page](https://www.memcachier.com/caches).

You should look at the PHP [Memcached client
documentation](http://www.php.net/manual/en/book.memcached.php) for a list of
API calls you can make against MemCachier.

We’ve built a small PHP example here: [MemCachier PHP sample
app](https://github.com/memcachier/examples-php).

<h3 id="php-session">PHP Session Support</h3>

You can configure PHP to store sessions in MemCachier as follows.

First, start by configuring an appropriate `.user.ini` in your document root.
It should contain the following:

```php
session.save_handler=memcached
memcached.sess_binary=1
session.save_path="PERSISTENT=myapp_session <MEMCACHIER_SERVERS>"
memcached.sess_sasl_username=<MEMCACHIER_USERNAME>
memcached.sess_sasl_password=<MEMCACHIER_PASSWORD>
```

In your code you should then be able to run:

```php
// Enable MemCachier session support
session_start();
$_SESSION['test'] = 42;
```

<h3 id="php-memcachesasl">Alternative PHP Client -- MemcacheSASL</h3>

This is not our recommended client for using MemCachier from PHP. We recommend
the [php memcached](#php) client. However, it is an easier client to use as
it's a pure PHP implementation while the [recommended php client](#php)
requires a C extension to be installed with
[SASL](http://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer)
support. It doesn't support multiple proxy servers like the memcached client
but is otherwise quite good.

You should first install the
[PHPMemcacheSASL](https://github.com/memcachier/PHPMemcacheSASL) client. You
can either grab the code directly or use [composer](https://getcomposer.org/)
for package management. We suggest composer.

First, if using composer, you'll need to modify your `composer.json` file to
include the module:

```js
{
    "require": {
        "php": ">=5.3.2",
        "memcachier/php-memcache-sasl": ">=1.0.1"
    }
}
```

Then, you can connect to MemCachier using the client:

```php
require 'vendor/autoload.php';
use MemCachier\MemcacheSASL;

// Create client
$m = new MemcacheSASL();
$servers = explode(",", <MEMCACHIER_SERVERS>);
foreach ($servers as $s) {
    $parts = explode(":", $s);
    $m->addServer($parts[0], $parts[1]);
}

// Setup authentication
$m->setSaslAuthData( getenv("MEMCACHIER_USERNAME")
                   , getenv("MEMCACHIER_PASSWORD") );

$m->add("foo", "bar");
echo $m->get("foo");
```

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and
`<MEMCACHIER_PASSWORD>` are listed on your [cache overview
page](https://www.memcachier.com/caches).

We’ve built a small PHP example here: [MemCachier PHP sample
app](https://github.com/memcachier/examples-php).
