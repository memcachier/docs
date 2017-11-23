
## PHP

**IF(direct)**
<p class="alert alert-info">
We’ve built a small PHP example here:
<a href="https://github.com/memcachier/examples-php">MemCachier PHP sample app</a>.
</p>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small PHP example.
><a class="github-source-code" href="https://github.com/memcachier/examples-php">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-php).

>callout
>Heroku recently improved their PHP support, please see their
>[documentation](https://devcenter.heroku.com/articles/php-support)
>if you aren't familiar with the new model.
**ENDIF**

We recommended you use the [PHP Memcached
client](http://www.php.net/manual/en/book.memcached.php) to connect with
MemCachier. It supports the full protocol and has great performance.
**IF(direct)**
We also recommend that you use the [composer dependency
manager](https://getcomposer.org/) for PHP, although that is up to you.

It can be difficult to get the memcached client to work as it requires that you
build it against a version of libmemcached (a C library that the PHP client
relies upon) that support SASL authentication, which often isn't enabled by
default. If you have trouble, please open a [support
ticket](http://support.memcachier.com/) with us. Alternatively, you could use a
[pure PHP client](#alternative-php-client----memcachesasl) that MemCachier
supports, instructions on how are [here](#alternative-php-client----memcachesasl).

First, if using composer, you'll need to modify your `composer.json` file to
include the module:
**ENDIF**

**IF(heroku)**
First, you'll need to modify your `composer.json` file to include the
module:
**ENDIF**

```js
{
    "require": {
        "php": ">=5.3.2",
        "ext-memcached": "*"
    }
}
```

Next, ensure that your new requirements are "frozen" to `composer.lock` by running:

```term
$ composer update
```

**IF(heroku)**
For more information on enabling the extension and potential troubleshooting (e.g. when you don't have the `memcached` extension available on your local computer), refer to the [using optional extensions extensions](/articles/php-support#using-optional-extensions) section of Heroku's PHP reference documentation.
**ENDIF**

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
**IF(direct)**
$m->setSaslAuthData( <MEMCACHIER_USERNAME>
                   , <MEMCACHIER_PASSWORD> );
**ENDIF**
**IF(heroku)**
$m->setSaslAuthData( getenv("MEMCACHIER_USERNAME")
                   , getenv("MEMCACHIER_PASSWORD") );
**ENDIF**

// We use a consistent connection to memcached, so only add in the
// servers first time through otherwise we end up duplicating our
// connections to the server.
if (!$m->getServerList()) {
    // parse server config
**IF(direct)**
    $servers = explode(",", <MEMCACHIER_SERVERS>);
**ENDIF**
**IF(heroku)**
    $servers = explode(",", getenv("MEMCACHIER_SERVERS"));
**ENDIF**
    foreach ($servers as $s) {
        $parts = explode(":", $s);
        $m->addServer($parts[0], $parts[1]);
    }
}
```

**IF(direct)**
The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and
`<MEMCACHIER_PASSWORD>` are listed on your [cache overview
page](https://www.memcachier.com/caches).
**ENDIF**

You should look at the PHP [Memcached client
documentation](http://www.php.net/manual/en/book.memcached.php) for a list of
API calls you can make against MemCachier.

### PHP Session Support

You can configure PHP to store sessions in MemCachier as follows.

First, start by configuring an appropriate `.user.ini` in your document
**IF(direct)**
root.
**ENDIF**
**IF(heroku)**
root (see [heroku ini
guide](https://devcenter.heroku.com/articles/custom-php-settings#user-ini-files-recommended)).
**ENDIF**
It should contain the following:

```php
session.save_handler=memcached
memcached.sess_binary=1
**IF(direct)**
session.save_path="PERSISTENT=myapp_session <MEMCACHIER_SERVERS>"
memcached.sess_sasl_username=<MEMCACHIER_USERNAME>
memcached.sess_sasl_password=<MEMCACHIER_PASSWORD>
**ENDIF**
**IF(heroku)**
session.save_path="PERSISTENT=myapp_session ${MEMCACHIER_SERVERS}"
memcached.sess_sasl_username=${MEMCACHIER_USERNAME}
memcached.sess_sasl_password=${MEMCACHIER_PASSWORD}
**ENDIF**
```

In your code you should then be able to run:

```php
// Enable MemCachier session support
session_start();
$_SESSION['test'] = 42;
```

### Alternative PHP Client -- MemcacheSASL

**IF(direct)**
This is not our recommended client for using MemCachier from PHP. We recommend
the [php memcached](#php) client. However, it is an easier client to use as
it's a pure PHP implementation while the [recommended php client](#php)
requires a C extension to be installed with
[SASL](http://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer)
support. It doesn't support multiple proxy servers like the memcached client
but is otherwise quite good.
**ENDIF**

**IF(heroku)**
>note
>This is not our recommended client for using MemCachier from PHP. We
>recommend the [php memcached](#php) client. However, it may work
>better for you if you are running into any problems with the php
>memcached client.
**ENDIF**

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
**IF(direct)**
$servers = explode(",", <MEMCACHIER_SERVERS>);
**ENDIF**
**IF(heroku)**
$servers = explode(",", getenv("MEMCACHIER_SERVERS"));
**ENDIF**
foreach ($servers as $s) {
    $parts = explode(":", $s);
    $m->addServer($parts[0], $parts[1]);
}

// Setup authentication
**IF(direct)**
$m->setSaslAuthData( <MEMCACHIER_USERNAME>
                   , <MEMCACHIER_PASSWORD> );
**ENDIF**
**IF(heroku)**
$m->setSaslAuthData( getenv("MEMCACHIER_USERNAME")
                   , getenv("MEMCACHIER_PASSWORD") );
**ENDIF**

// Test client
$m->add("foo", "bar");
echo $m->get("foo");
```

**IF(direct)**
The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and
`<MEMCACHIER_PASSWORD>` are listed on your [cache overview
page](https://www.memcachier.com/caches).
**ENDIF**
