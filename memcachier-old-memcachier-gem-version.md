---
title: MemCachier
id: 674
markdown_flavour: github


[MemCachier](http://www.memcachier.com) is an implementation of the
[Memcache](http://memcached.org) in-memory key/value store used for
caching data. It is a key technology in modern web applications for
scaling and reducing server loads. The MemCachier add-on manages and
scales clusters of memcache servers so you can focus on your app. Tell
us how much memory you need and get started for free instantly. Add
capacity later as you need it.

Follow our [blog](http://blog.memcachier.com) or twitter
([@memcachier](http://twitter.com/MemCachier)), for status and product
announcements.

## Getting started

Start by installing the add-on:

```term
$ heroku addons:add memcachier:dev
```

You can start with more memory if you know you’ll need it:

```term
$ heroku addons:add memcachier:100
$ heroku addons:add memcachier:500
 ... etc ...
```

Once the add-on has been added you’ll notice three new variables in
`heroku config`:

```term
$ heroku config
...
MEMCACHIER_SERVERS    => mcX.ec2.memcachier.com
MEMCACHIER_USERNAME   => bobslob
MEMCACHIER_PASSWORD   => l0nGr4ndoMstr1Ngo5strang3CHaR4cteRS
...
```

Next, setup your app to start using the cache. We have documentation
for the following languages and frameworks:

* [Ruby](#ruby)
* [Rails 3 & 4](#rails-3-and-4)
* [Rails 2](#rails2)
* [Rack::Cache](#rails-rack-cache)
* [PHP](#php)
* [CakePHP](#cakephp)
* [Symfony2](#symfony2)
* [Django](#django)
* [Node.js](#node.js)
* [Java](#java)

>note
>Your credentials may take up to three (3) minutes to
>be synced to our servers. You may see authentication errors if you
>start using the cache immediately.

## Ruby

>callout
>We’ve built a small Ruby Sinatra example. <br>
><a class="github-source-code" href="http://github.com/memcachier/examples-sinatra">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-sinatra)

Start by adding the
[memcachier](http://github.com/memcachier/memcachier-gem) and
[dalli](http://github.com/mperham/dalli) gems to your Gemfile.

```ruby
gem 'memcachier'
gem 'dalli'
```

Then bundle install:

```term
$ bundle install
```

`Dalli` is a Ruby memcache client, and the `memcachier` gem modifies
the environment (`ENV`) such that the environment variables set by
MemCachier will work with Dalli. Once these gems are installed you can
start writing code. The following is a basic example showing get and
set.

```ruby
require 'dalli'
require 'memcachier'
cache = Dalli::Client.new
cache.set("foo", "bar")
puts cache.get("foo")
```

Without the `memcachier` gem, you’ll need to pass the proper
credentials to `Dalli`:

```ruby
cache = Dalli::Client.new(ENV["MEMCACHIER_SERVERS"].split(","),
                    {:username => ENV["MEMCACHIER_USERNAME"],
                     :password => ENV["MEMCACHIER_PASSWORD"],
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2
                    })
```

### Testing (Ruby)

The easiest way to test that your setup is working is through the
heroku console:

```term
$ heroku run console --app <app>
>> require 'dalli'
>> require 'memcachier'
>> dc = Dalli::Client.new
>> dc.set('memcachier', 'rocks')
=> true
```

And then fetch the value back:

```term
>> dc.get('memcachier')
=> "rocks"
```

You can also get an insight into your cache usage (number of keys
stored and bytes) with the `stats` command:

```term
>> dc.stats
=> {"memcachier.example.net:11211" => {"cur_items" => "49982", "bytes" => "89982234"} }
```

## Rails 3 and 4

>callout
>We’ve built a small Rails example. <br>
><a class="github-source-code" href="https://github.com/memcachier/examples-rails">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-rails)

We also have a tutorial on using MemCachier with Rails [here](building-a-rails-3-application-with-memcache).

Here we explain how you setup and install MemCachier with Rails. Refer
to the [Rails caching
guide](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-site-cache)
for information on how you use MemCachier with Rails. Rails supports
automatic whole site caching, per-view caching and fragment caching.

Start by adding the
[memcachier](http://github.com/memcachier/memcachier-gem) and
[dalli](http://github.com/mperham/dalli) gems to your Gemfile.

```ruby
gem 'memcachier'
gem 'dalli'
```

Then run bundle install:

```term
$ bundle install
```

`Dalli` is a Ruby memcache client, and the `memcachier` gem modifies
the environment (`ENV`) such that the environment variables set by
MemCachier will work with Dalli. Once these gems are installed you’ll
want to configure the Rails cache_store appropriately. Modify your
`config/environments/production.rb` with the following:

```ruby
config.cache_store = :dalli_store
```

>callout
>In your development environment, Rails.cache defaults to a simple
>in-memory store and so it doesn’t require a running memcached.


From here you can use the following code examples to use the cache in
your Rails app:

```ruby
Rails.cache.write("foo", "bar")
puts Rails.cache.read("foo")
```

Without the `memcachier` gem, you’ll need to pass the proper
credentials to Dalli in `config/environments/production.rb`:

```ruby
config.cache_store = :dalli_store,
                    (ENV["MEMCACHIER_SERVERS"] || "").split(","),
                    {:username => ENV["MEMCACHIER_USERNAME"],
                     :password => ENV["MEMCACHIER_PASSWORD"],
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2
                    }
```

>callout
>It is possible you will run into a configuration problem if you are
>using Rails 3.1 and the Heroku Cedar platform. Information on how to
>fix that issue can be found at [this Stackoverflow
>answer](http://stackoverflow.com/questions/6458947/rails-3-1-heroku-cedar-static-image-assets-are-not-being-served)

### Testing (Rails)

To test locally you can simply use the rails console:

```term
rails console
>> Rails.cache.write('memcachier', 'rocks')
=> true
>> Rails.cache.read('memcachier')
=> "rocks"
```

To test against MemCachier itself, refer to the [Ruby testing
instructions](#testing-ruby).

## Rails 2

Start by adding the
[memcachier](http://github.com/memcachier/memcachier-gem) and
[dalli](http://github.com/mperham/dalli) gems to your Gemfile. You
will need to use dalli **v1.0.5** as later versions of Dalli don't
support Rails 2.

```ruby
gem 'memcachier'
gem 'dalli', '~>1.0.5'
```

Then run bundle install:

```term
$ bundle install
```

`Dalli` is a Ruby memcache client, and the `memcachier` gem modifies
the environment (`ENV`) such that the environment variables set by
MemCachier will work with Dalli. Once these gems are installed you’ll
want to configure the Rails cache_store appropriately. Modify
`config/environments/production.rb` with the following:

```ruby
require 'active_support/cache/dalli_store23'
config.cache_store = :dalli_store
```

>callout
>In your development environment, Rails.cache defaults to a simple
>in-memory store and so it doesn’t require a running memcached.

In `config/environment.rb`:

```ruby
config.gem 'dalli'
```

From here you can use the following code examples to use the cache in
your Rails app:

```ruby
Rails.cache.write("foo", "bar")
puts Rails.cache.read("foo")
```

Without the `memcachier` gem, you’ll need to pass the proper
credentials to Dalli in `config/environments/production.rb`:

```ruby
config.cache_store = :dalli_store,
                    (ENV["MEMCACHIER_SERVERS"] || "").split(","),
                    {:username => ENV["MEMCACHIER_USERNAME"],
                     :password => ENV["MEMCACHIER_PASSWORD"],
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2
                    }
```

### Testing (Rails)

To test locally you can simply use the rails console:

```term
rails console
>> Rails.cache.write('memcachier', 'rocks')
=> true
>> Rails.cache.read('memcachier')
=> "rocks"
```

To test against MemCachier itself, please refer to the [Ruby testing
instructions](#testing-ruby).

## Rails Rack::Cache

Rails can use a middle-ware component of the Rack web server
architecture called Rack::Cache. This provides caching of static
assets in Rails and is a simple alternative to use a full CDN.

Please see [this
article](https://devcenter.heroku.com/articles/rack-cache-memcached-rails31#configure-rails-cache-store)
for information.

## Django

>callout
>We’ve built a small Django example. <br>
><a class="github-source-code" href="http://github.com/memcachier/examples-django">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-django)

We also have a tutorial on using Django and MemCachier together [here](https://devcenter.heroku.com/articles/django-memcache).

Here we explain how you setup and install MemCachier with Django. Please
see the [Django caching
guide](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-site-cache)
for how you effectively use MemCachier. Django supports
whole site caching, per-view caching and fragement caching.

MemCachier has been tested with the `pylibmc` memcache client, but the
default client doesn’t support SASL authentication. Run the following
commands on your local machine to install the necessary pips:

```term
$ sudo port install libmemcached
$ LIBMEMCACHED=/opt/local pip install pylibmc
$ pip install django-pylibmc
```

Be sure to update your `requirements.txt` file with these new
requirements (note that your versions may differ than what’s below):

    pylibmc==1.3.0
    django-pylibmc==0.5.0

>note
>The above `pylibmc` requirements must be added directly to your
>`requirements.txt` file. They shouldn't be placed in an included pip
>requirement file. The Heroku Python buildpack checks the
>`requirements.txt` file and only that file for the presence of
>`pylibmc` to trigger bootstrapping `libmemcached`, which is
>prerequisite for installing `pylibmc`.

Next, configure your settings.py file the following way:

```python
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'BINARY': True,
        'OPTIONS': {
            'no_block': True,
            'tcp_nodelay': True,
            'tcp_keepalive': True,
            'remove_failed': 4,
            'retry_timeout': 2,
            'dead_timeout': 10,
            '_poll_timeout': 2000
        }
    }
}
```

From here you can start writing cache code in your Django app:

```python
from django.core.cache import cache
cache.set("foo", "bar")
print cache.get("foo")
```

You may be interested in the
[django-heroku-memcacheify](http://github.com/rdegges/django-heroku-memcacheify)
pip, which fully configures MemCachier with one line of code for any
Django app the pip supports.

>note
>A confusing error message you may get from `pylibmc` is
>**MemcachedError: error 37 from memcached_set: SYSTEM ERROR(Resource
>temporarily unavailable)**. This indicates that you are trying to
>store a value larger than 1MB. MemCachier has a hard limit of 1MB for
>the size of key-value pairs. To work around this, either consider
>sharding the data or using a different technology. The benefit of an
>in-memory key-value store diminishes at 1MB and higher.

## PHP

>callout
>We’ve built a small PHP example. <br>
><a class="github-source-code" href="https://github.com/memcachier/examples-php">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-php)

>callout
>Heroku recently improved their PHP support, please see their 
>[documentation](https://devcenter.heroku.com/articles/php-support)
>if you aren't familiar with the new model.

We recommended you use the
[PHP Memcached client](http://www.php.net/manual/en/book.memcached.php)
to connect with MemCachier. It supports the full protocol and has
great performance.

First, you'll need to modify your `composer.json` file to include the
module:

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
// create a new persistent client
$m = new Memcached("memcached_pool");
$m->setOption(Memcached::OPT_BINARY_PROTOCOL, TRUE);

// some nicer default options
$m->setOption(Memcached::OPT_NO_BLOCK, TRUE);
$m->setOption(Memcached::OPT_AUTO_EJECT_HOSTS, TRUE);
$m->setOption(Memcached::OPT_CONNECT_TIMEOUT, 2000);
$m->setOption(Memcached::OPT_POLL_TIMEOUT, 2000);
$m->setOption(Memcached::OPT_RETRY_TIMEOUT, 2);

// setup authentication
$m->setSaslAuthData( getenv("MEMCACHIER_USERNAME")
                   , getenv("MEMCACHIER_PASSWORD") );

// We use a consistent connection to memcached, so only add in the
// servers first time through otherwise we end up duplicating our
// connections to the server.
if (!$m->getServerList()) {
    // parse server config
    $servers = explode(",", getenv("MEMCACHIER_SERVERS"));
    foreach ($servers as $s) {
        $parts = explode(":", $s);
        $m->addServer($parts[0], $parts[1]);
    }
}
```

You should look at the PHP
[Memcached client documentation](http://www.php.net/manual/en/book.memcached.php)
for a list of API calls you can make against MemCachier.

### Session Support

You can configure PHP to store sessions in MemCachier as follows.

First, start by configuring an appropriate `.user.ini` in your
document root (see [heroku ini
guide](https://devcenter.heroku.com/articles/custom-php-settings#user-ini-files-recommended)).
It should contain the following:

```php
session.save_handler=memcached
memcached.sess_binary=1
session.save_path="PERSISTENT=myapp_session ${MEMCACHIER_SERVERS}"
memcached.sess_sasl_username=${MEMCACHIER_USERNAME}
memcached.sess_sasl_password=${MEMCACHIER_PASSWORD}
```

In your code you should then be able to run:

```php
// Enable MemCachier session support
session_start();
$_SESSION['test'] = 42;
```

### Alternative PHP Client

>note
>This is not our recommended client for using MemCachier from PHP. We
>recommend the [php memcached](#php) client. However, it may work
>better for you if you are running into any problems with the php
>memcached client.

You should first install the
[PHPMemcacheSASL](https://github.com/memcachier/PHPMemcacheSASL)
client. You can either grab the code directly or use
[composer](https://getcomposer.org/) for package management. We
suggest composer.

First, if using composer, you'll need to modify your `composer.json`
file to include the module:

~~~~ js
{
    "require": {
        "php": ">=5.3.2",
        "memcachier/php-memcache-sasl": ">=1.0.1"
    }
}
~~~~

Then, you can connect to MemCachier using the client:

~~~~ php
require 'vendor/autoload.php';
use MemCachier\MemcacheSASL;

// Create client
$m = new MemcacheSASL();
$servers = explode(",", getenv("MEMCACHIER_SERVERS"));
foreach ($servers as $s) {
    $parts = explode(":", $s);
    $m->addServer($parts[0], $parts[1]);
}

// Setup authentication
$m->setSaslAuthData( getenv("MEMCACHIER_USERNAME")
                   , getenv("MEMCACHIER_PASSWORD") );

// Test client
$m->add("foo", "bar");
echo $m->get("foo");
~~~~

## CakePHP

The CakePHP framework has excellent support for caching and can be
easily used with MemCachier as the provider. To setup CakePHP with
MemCachier, you'll need to edit the file `app/Config/bootstrap.php`
and add the following lines:

```php
Cache::config('default', array(
    'engine' => 'Memcached',
    'prefix' => 'mc_',
    'duration' => '+7 days',
    'servers' => explode(',', getenv('MEMCACHIER_SERVERS')),
    'compress' => false,
    'persistent' => 'memcachier',
    'login' => getenv('MEMCACHIER_USERNAME'),
    'password' => getenv('MEMCACHIER_PASSWORD'),
    'serialize' => 'php'
));
```

After that, you should be able to use caching throughout your application like
so:

```php
class Post extends AppModel {

    public function newest() {
        $model = $this;
        return Cache::remember('newest_posts', function() use ($model){
            return $model->find('all', array(
                'order' => 'Post.updated DESC',
                'limit' => 10
            ));
        }, 'longterm');
    }
}
```

The above will fetch the value associated with the key `newest_posts` from the
cache if it exists. Otherwise, it will execute the function and SQL query,
storing the result in the cache using the `newest_posts` key.

You can find much more information on how to use caching with CakePHP
[here](http://book.cakephp.org/2.0/en/core-libraries/caching.html).

## Symfony2

The [Symfony2](http://symfony.com/) framework is a great choice with
Heroku and MemCachier.  It supports caching and storing sessions in
MemCachier.

First, start by configuring an appropriate `.user.ini` in your
document root (see [heroku ini
guide](https://devcenter.heroku.com/articles/custom-php-settings#user-ini-files-recommended)).
It should contain the following:

```php
session.save_handler=memcached
memcached.sess_binary=1
session.save_path="PERSISTENT=myapp_session ${MEMCACHIER_SERVERS}"
memcached.sess_sasl_username=${MEMCACHIER_USERNAME}
memcached.sess_sasl_password=${MEMCACHIER_PASSWORD}
```

## Node.js

>callout
>We’ve built a small Node.js example. <br>
><a class="github-source-code" href="https://github.com/memcachier/examples-node">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-node)

For Node.js we recommend the use of the
[memjs](http://github.com/alevy/memjs) client library. It is written
and supported by MemCachier itself! To install, use the [node package
manager (npm)](http://npmjs.org/):

```term
$ npm install memjs
```

Using it is straight-forward as memjs understands the
`MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME` and `MEMCACHIER_PASSWORD`
environment variables that the MemCachier add-on setups. For example:

```javascript
var memjs = require('memjs')
var mc = memjs.Client.create()
mc.get('hello', function(val) {
    alert(val)
})
```

## Java

>callout
>We’ve built a small Java example with Jetty. <br>
><a class="github-source-code" href="https://github.com/memcachier/examples-java">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-java)

For Java we recommend using the
[SpyMemcached](http://code.google.com/p/spymemcached/) client. We also
recommend using the [Apache Maven](http://maven.apache.org/) build
manager for working with Java applications. If you aren't using
`maven` and are instead using [Apache Ant](http://ant.apache.org/) or
your own build system, then simply add the `spymemcached` jar file as
a dependency of your application.

>warning
>Please make sure to use version
>__2.8.9__ or earlier! At the moment, version 2.8.10 and later have an
>[issue](http://code.google.com/p/spymemcached/issues/detail?id=272)
>with SASL authentication that makes them unusable with MemCachier.

For `maven` however, start by configuring it to have the proper
`spymemcached` repository:

    <repository>
      <id>spy</id>
      <name>Spy Repository</name>
      <layout>default</layout>
      <url>http://files.couchbase.com/maven2/</url>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </repository>

Then add the `spymemcached` library to your dependencies:

    <dependency>
      <groupId>spy</groupId>
      <artifactId>spymemcached</artifactId>
      <version>2.8.9</version>
      <scope>provided</scope>
    </dependency>

Once your build system is configured, you can start adding caching to
your Java app:

```java
import java.io.IOException;
import net.spy.memcached.AddrUtil;
import net.spy.memcached.MemcachedClient;
import net.spy.memcached.ConnectionFactoryBuilder;
import net.spy.memcached.auth.PlainCallbackHandler;
import net.spy.memcached.auth.AuthDescriptor;

public class Foo {
  public static void main(String[] args) {
    AuthDescriptor ad = new AuthDescriptor(new String[] { "PLAIN" },
        new PlainCallbackHandler(System.getenv("MEMCACHIER_USERNAME"),
            System.getenv("MEMCACHIER_PASSWORD")));

    try {
      MemcachedClient mc = new MemcachedClient(
          new ConnectionFactoryBuilder()
              .setProtocol(ConnectionFactoryBuilder.Protocol.BINARY)
              .setAuthDescriptor(ad).build(),
          AddrUtil.getAddresses(System.getenv("MEMCACHIER_SERVERS")));
      mc.set("foo", "bar");
      System.out.println(mc.get("foo"));
    } catch (IOException ioe) {
      System.err.println("Couldn't create a connection to MemCachier: \nIOException "
              + ioe.getMessage());
    }
  }
}
```

>callout
>It is possible that you will run into Java exceptions about the class
>loader. (See Spymemcached [issue
>155](http://code.google.com/p/spymemcached/issues/detail?id=155). The
>reported issue also contains a suggested work around.


You may wish to look the `spymemcached`
[JavaDocs](http://dustin.github.com/java-memcached-client/apidocs/) or
some more [example
code](http://code.google.com/p/spymemcached/wiki/Examples) to help in
using MemCachier effectively. There is also a guide on using
[WebRunner](https://devcenter.heroku.com/articles/java-webapp-runner),
Heroku's framework to handle sessions with MemCachier.

## Library support

MemCachier will work with any memcached binding that supports [SASL
authentication](http://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer)
and the [binary
protocol](http://code.google.com/p/memcached/wiki/MemcacheBinaryProtocol).
We have tested MemCachier with the following language bindings,
although the chances are good that other SASL binary protocol packages
will also work.

<table>
<tbody>
<tr>
<th>Language</th>
<th>Bindings</th>
</tr>
<tr>
<td>Ruby</td>
<td><a href="http://github.com/mperham/dalli">dalli</a></td>
</tr>
<tr>
<td>Python</td>
<td>
  <a href="http://sendapatch.se/projects/pylibmc/">pylibmc</a>
</td>
</tr>
<tr>
<td>Django</td>
<td>
  <a href="http://github.com/jbalogh/django-pylibmc">django-pylibmc</a>
</td>
</tr>
<tr>
<td>PHP</td>
<td>
  <a href="http://www.php.net/manual/en/book.memcached.php">PHP Memcached</a>
</td>
</tr>
<tr>
<td>Node.js</td>
<td>
  <a href="http://github.com/alevy/memjs">memjs</a>
</td>
</tr>
<tr>
<td>Java</td>
<td>
  <a href="http://code.google.com/p/spymemcached/">spymemcached</a>
  (version <b>2.8.9</b> or earlier) <b>or</b>
  <a href="http://code.google.com/p/xmemcached/">xmemcached</a>
</td>
</tr>
<tr>
<td>Go</td>
<td><a href="http://github.com/bmizerany/mc">mc</a></td>
</tr>
<tr>
<td>Haskell</td>
<td><a href="http://hackage.haskell.org/package/memcache">memcache</a></td>
</tr>
</tbody>
</table>

## Local usage

To test your Heroku application locally, you will need to run a local
memcached server. MemCachier can only run in Heroku, but because
MemCachier and memcached speak the same protocol, you shouldn’t have
any issues testing locally. Installation depends on your platform.

>callout
>This will install memcached without SASL authentication support. This is generally what you want as client code can still try to use SASL auth and memcached will simply ignore the requests which is the same as allowing any credentials. So your client code can run without modification locally and on Heroku.

On Ubuntu:

```term
$ sudo apt-get install memcached
```

Or on OS X (with Homebrew):

```term
$ brew install memcached
```

Or for Windows please refer to [these
instructions](http://www.codeforest.net/how-to-install-memcached-on-windows-machine).

For further information and resources (such as the memcached source
code) please refer to the [Memcache.org
homepage](http://memcached.org)

To run memcached simply execute the following command:

```term
$ memcached -v
```

## Usage analytics

Our analytics dashboard is a simple tool that gives you more insight
into how you’re using memcache.  Here's a screenshot of the dashboard:

![Analytics Dashboard](https://www.memcachier.com/images/analytics.png)

To access your application's analytics dashboard run:

```term
$ heroku addons:open memcachier
```

Or open MemCachier from your application's dashboard on heroku.com.

The analytics displayed are:

* _Limit_ -- Your current cache size and memory limit. Once usage comes
  close to this amount you will start seeing evictions.
* _Live Connections_ -- Number of connections currently open to your
  cache.
* _Total connections_ -- Number of connections ever made to your cache.
  (So always larger than live connections).
* _Items_ -- Number of items currently stored in your cache.
* _Evictions_ -- Number of items ever evicted from your cache due to
  memory pressure. Items are evicted in an LRU order.
* _New Evictions_ -- Number of evictions that have occured since the
  last time we sampled your cache.
* _Hit Rate_ -- The ratio of `get` commands that return an item (hit)
  vs. the number that return nothing (miss). This ratio is for the
  period between now and when we last sampled your cache.
* _Set Cmds_ -- Number of times you have ever performed a set command.
* _Flush Cmds_ -- Number of times you have ever performned a flush
  command.

With the basic analytics dashboard we sample your cache once per hour.
With the advance dashboard we sample it once every 30 minutes.

### Advanced analytics

We offer higher paying customers an advance version of our analytics
dashboard. Currently, this offers two primary advantages:

* _Higher Sample Rate_ -- We sample the cache for collecting analytics
  once every thirty minutes, twice the rate of the basic analytics
  dashboard. We don't sample more often than that as a higher
  granularity hasn't proven to be useful, it leads to more noise and
  less signal.
* _More Graphs_ -- We offer two additional graphs for the advanced
  analytics dashboard.
  * _Eviction Graph_ -- Your new evictions tracked over time.
  * _Connection Graph_ -- Your new connecions tracked over time.

## New Relic integration

MemCachier supports integration with your New Relic dashboard if you
happen to be a customer of both MemCachier and New Relic. Currently
this feature is only available to caches of <strong>500MB</strong> or
larger. A blog post showing the integration can be found
[here](http://blog.memcachier.com/2014/03/05/memcachier-and-new-relic-together/).

To setup the integration you will need to find your New Relic license
key. This can be done by going to your "Account Settings" page when
logged in to New Relic by click on your New Relic username in the top
right corner. Then you will find your license key in the right side
information column. It should be exactly 40 characters long. Please
refer to the [blog
post](http://blog.memcachier.com/2014/03/05/memcachier-and-new-relic-together/)
for a visual walkthrough.

Once you have your New Relic licence key, it can be entered for your
cache on the analytics dashboard page. In the bottom right corner
there is a button to do this.

## Upgrading and downgrading

Changing your plan, either by upgrading or downgrading, can be done
easily at any time through Heroku.

* No code changes are required.
* Your cache won't be lost or reset<strong>*</strong>.
* You are charged by the hour for plans, so try experimenting with
  different cache sizes with low cost.

>note
>When moving between the development plan to a
>production plan, you __will__ loose your cache. This is unavoidable
>due to the strong separation between the development and production
>clusters.


## Using MemCachier

Please refer to your client or framework documentation for how to use
MemCachier effectively.

MemCachier Guides:

* [Advanced Memcache Usage](https://devcenter.heroku.com/articles/advanced-memcache)
* [Building a Rails 3 App with MemCachier](https://devcenter.heroku.com/articles/building-a-rails-3-application-with-memcache)
* [Rails + Rack::Cache + MemCachier](https://devcenter.heroku.com/articles/rack-cache-memcached-rails31)
* [Django and MemCachier](https://devcenter.heroku.com/articles/django-memcache)
* [Java Webapp Runner Guide](https://devcenter.heroku.com/articles/java-webapp-runner)
* [Heroku's Guide to Caching](https://devcenter.heroku.com/articles/caching-strategies)

Framework and Client Documentation:

* [Dalli (Ruby Client) API](http://www.rubydoc.info/github/mperham/dalli/Dalli/Client)
* [Rails Caching Guide](http://guides.rubyonrails.org/caching_with_rails.html)
* [PHP Memcached client](http://www.php.net/manual/en/book.memcached.php)
* [CakePHP Caching Guide](http://book.cakephp.org/2.0/en/core-libraries/caching.html)
* [Pylibmc (Pytnon Client) API](http://sendapatch.se/projects/pylibmc/)
* [Django Caching Guide](https://docs.djangoproject.com/en/dev/topics/cache/)
* [MemJS (node.js client) API](http://amitlevy.com/projects/memjs/)
* [Spymemcached JavaDocs](http://dustin.github.com/java-memcached-client/apidocs/)


## Key-Value size limit (1MB)

MemCachier has a maximum size that a key-value object can be of
__1MB__. This applies to both key-value pairs created through a `set`
command, or existing key-value pairs grown through the use of an
`append` or `prepend` command. In the later case, the size of the
key-value pair with the new data added to it, must still be less than
1MB.

The 1MB limit applies to the size of the key and the value together. A
key of size 512KB with a value of 712KB would be in violation of the
1MB limit.

The reason for this has partially to do with how memory is managed in
MemCachier. A limitation of the high performance design is a
restriction on how large key-value pairs can become. Another reason is
that storing values larger than 1MB doesn't normally make sense in a
high-performance key-value store. The network transfer time in these
situations becomes the limiting factor for performance. A disk cache
or even a database makes sense for this size value.

## Errors about app trying to connect to localhost

By default, most memcache client look for the environment variables,
`MEMCACHE_SERVERS`, `MEMCACHE_USERNAME` and `MEMCACHE_PASSWORD` for
their configuration. These variables are used when the initialization
code for the memcache client doesn't specifically specify these values.

If these environment variables aren't set, clients generally default
to connecting to `127.0.0.1:11211` (i.e., localhost), with no username
and password.

The MemCachier add-on sets the `MEMCACHIER_SERVERS`,
`MEMCACHIER_USERNAME` and `MEMCACHIER_PASSWORD` environment variables.
So you need to either set the equivalent `MEMCACHE_*` variables from
these, or pass these values to your client when you create a new one
in your code.

For example, pseudo-code for the first approach is:

    env[MEMCACHE_SERVERS] = env[MEMCACHIER_SERVERS]
    env[MEMCACHE_USERNAME] = env[MEMCACHIER_USERNAME]
    env[MEMCACHE_PASSWORD] = env[MEMCACHIER_PASSWORD]

While pseudo-code for the second approach is:

    memClient = new MemcacheClient(ENV['MEMCACHIER_SERVERS'],
                                   ENV['MEMCACHIER_USERNAME'],
                                   ENV['MEMCACHIER_PASSWORD'])

Please be careful that you have setup the your client in all
locations. Many frameworks, such as Rails, use memcache in multiple
ways and may require you to setup initialization properly in a few
locations. Generally the first approach is preferred as it is global
while the second approach is local to each initialization.

For example, with Ruby on Rails, you'll need to setup `cache_store`,
`Rack::Cache` and the `session_store`.

## Support

All MemCachier support and runtime issues should be submitted via on
of the [Heroku Support channels](support-channels). You can also reach
us directly at
[support@memcachier.com](mailto:support@memcachier.com). We encourage
you to CC us on any urgent support tickets sent to Heroku. Please
include your `MEMCACHIER_USERNAME` with support tickets.

Any non-support related issues or product feedback is welcome via
email at: [support@memcachier.com](mailto:support@memcachier.com).

Any issues related to MemCachier service are reported at [MemCachier
Status](http://status.memcachier.com/).

Please also follow us on twitter,
[@memcachier](http://twitter.com/MemCachier), for status and product
announcements.
