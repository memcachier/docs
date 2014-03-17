# Getting Started with MemCachier

MemCachier is an implementation of the
[Memcache](http://memcached.org) in-memory key/value store used for
caching data. Memcache a key technology in modern web applications for
scaling and reducing server loads. MemCachier manages and
scales clusters of memcache servers so you can focus on your app. Tell
us how much memory you need and get started for free instantly. Add
capacity later as you need it.

Below is our user guide for using MemCachier, you can also find answers
in our <a href="/faq">FAQ</a>.

<h2 id="toc">Table of Contents</h2>

1. [Ruby](#ruby)
2. [Rails 3 & 4](#rails3)
3. [Rails 2](#rails2)
4. [Django](#django)
5. [PHP](#php)
6. [Node.js](#node.js)
7. [Java](#java)
8. [Supported client libraries](#clients)
9. [Example applications](#sample-apps)
10. [Local usage](#local)
11. [MemCachier analytics](#analytics)
12. [Advanced analytics](#advanced-analytics)
13. [New Relic integration](#newrelic)
14. [Changing plans](#upgrading)
15. [Key-Value size limit](#1mb-limit)
16. [Errors connecting to localhost](#localhost-errors)
17. [Getting support](#support)


<h2 id="ruby">Ruby</h2>

Start by adding the [dalli](https://github.com/mperham/dalli) gem to your Gemfile.

~~~~ ruby
gem 'dalli'
~~~~

Then bundle install:

~~~~ text
$ bundle install
~~~~

`Dalli` is a Ruby memcache client.  Once it is installed you can start writing code. The following is a basic example showing get and set.

~~~~ ruby
cache = Dalli::Client.new(<MEMCACHIER_SERVERS>.split(","),
                    {:username => <MEMCACHIER_USERNAME>,
                     :password => <MEMCACHIER_PASSWORD>
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2
                    })
~~~~

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your [cache overview page](https://www.memcachier.com/caches).

From here you can use the following code examples to use the cache in your Ruby app:

~~~~ ruby
cache.write("foo", "bar")
puts cache.read("foo")
~~~~

You can also get an insight into your cache usage (number of keys stored and bytes) with the `stats` command:

~~~~ ruby
cache.stats
=> {"memcachier.example.net:11211" => {"cur_items" => "49982", "bytes" => "89982234"} }
~~~~

We’ve built a small Ruby example using Sinatra here: [MemCachier Sinatra Sample App](https://github.com/memcachier/examples-sinatra).


<h2 id="rails3">Rails 3 & 4</h2>

Start by adding the [dalli](https://github.com/mperham/dalli) gem to your Gemfile.

~~~~ ruby
gem 'dalli'
~~~~

Then bundle install:

~~~~ text
$ bundle install
~~~~

`Dalli` is a Ruby memcache client.  Once it is installed you’ll want to configure the Rails cache_store appropriately. Modify `config/environments/production.rb` with the following:

~~~~ ruby
config.cache_store = :dalli_store, <MEMCACHIER_SERVERS>.split(","),
                    {:username => <MEMCACHIER_USERNAME>,
                     :password => <MEMCACHIER_PASSWORD>
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2
                    }
~~~~

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your [cache overview page](https://www.memcachier.com/caches).

<p class="alert alert-info">In your development environment, Rails.cache defaults to a simple in-memory store and so it doesn’t require a running memcached.</p>

From here you can use the following code examples to use the cache in your Rails app:

~~~~ ruby
Rails.cache.write("foo", "bar")
puts Rails.cache.read("foo")
~~~~

We’ve built a small Rails example here: [MemCachier Rails sample app](https://github.com/memcachier/examples-rails).


<h2 id="rails2">Rails 2</h2>

Start by adding the [dalli](https://github.com/mperham/dalli) gem to your Gemfile. You will need to use dalli **v1.0.5** as later versions of Dalli don't
support Rails 2.

~~~~ ruby
gem 'memcachier'
gem 'dalli', '~>1.0.5'
~~~~

Then bundle install:

~~~~ text
$ bundle install
~~~~

`Dalli` is a Ruby memcache client.  Once it is installed you’ll want to configure the Rails cache_store appropriately. Modify `config/environments/production.rb` with the following:

~~~~ ruby
require 'active_support/cache/dalli_store23'
config.cache_store = :dalli_store, <MEMCACHIER_SERVERS>.split(","),
                    {:username => <MEMCACHIER_USERNAME>,
                     :password => <MEMCACHIER_PASSWORD>
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2
                    }
~~~~

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your [cache overview page](https://www.memcachier.com/caches).

<p class="alert alert-info">In your development environment, Rails.cache defaults to a simple in-memory store and so it doesn’t require a running memcached.</p>

Also modify`config/environment.rb` to contain:

~~~~ ruby
config.gem 'dalli'
~~~~

From here you can use the following code examples to use the cache in your Rails app:

~~~~ ruby
Rails.cache.write("foo", "bar")
puts Rails.cache.read("foo")
~~~~

We’ve built a small Rails (3 & 4) example here: [MemCachier Rails sample app](https://github.com/memcachier/examples-rails).


<h2 id="rack">Rails Rack::Cache</h2>

Rails can use a middle-ware component of the Rack web server architecture called Rack::Cache. This provides caching of static assets in Rails and is a simple alternative to use a full CDN.  

Please see [this
article](https://devcenter.heroku.com/articles/rack-cache-memcached-rails31#configure-rails-cache-store)
for information.


<h2 id="django">Django</h2>

MemCachier has been tested with the `pylibmc` memcache client, but the default client doesn’t support SASL authentication. Run the following commands on your machine to install the necessary pips:

~~~~ text
$ sudo port install libmemcached
$ LIBMEMCACHED=/opt/local pip install pylibmc
$ pip install django-pylibmc-sasl
~~~~

Be sure to update your `requirements.txt` file with these new
requirements (note that your versions may differ than what’s below):

~~~~ text
pylibmc==1.2.2
django-pylibmc-sasl==0.2.4
~~~~

Next, configure your settings.py file the following way:

~~~~ python
os.environ['MEMCACHE_SERVERS'] = <MEMCACHIER_SERVERS>.replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = <MEMCACHIER_USER_NAME>
os.environ['MEMCACHE_PASSWORD'] = <MEMCACHIER_PASSWORD>

CACHES = {
  'default': {
    'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
    'TIMEOUT': 500,
    'BINARY': True,
    'OPTIONS': { 'tcp_nodelay': True }
  }
}
~~~~

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your [cache overview page](https://www.memcachier.com/caches). Note that Django expects <MEMCACHIER_SERVERS> to be semicolon-delimited (while we provide it comma-eliminated).

From here you can start writing cache code in your Django app:

~~~~ python
from django.core.cache import cache
cache.set("foo", "bar")
print cache.get("foo")
~~~~

We’ve built a small Django example here: [MemCachier Django sample app](https://github.com/memcachier/examples-django).


<h2 id="php">PHP</h2>

We recommend users utilize the [PHPMemcacheSASL](https://github.com/ronnywang/PHPMemcacheSASL) client as we have more experience in using and supporting it. Start by downloading the [PHPMemcacheSASL](https://github.com/ronnywang/PHPMemcacheSASL) library. From here you can start writing cache code in your PHP app:

~~~~ php
include('MemcacheSASL.php');
$m = new MemcacheSASL;
$servers = explode(",", getenv("MEMCACHIER_SERVERS"));
foreach ($servers as $s) {
    $parts = explode(":", $s);
    $m->addServer($parts[0], $parts[1]);
}
$m->setSaslAuthData(<MEMCACHIER_USERNAME>, <MEMCACHIER_PASSWORD>);

$m->add("foo", "bar");
echo $m->get("foo");
~~~~

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your [cache overview page](https://www.memcachier.com/caches).

The more common PHP memcache clients have limited support for working with MemCachier due to issues with SASL authentication. The [Memcache](http://www.php.net/manual/en/book.memcache.php) simply doesn't provide SASL authentication support and so is not an option. The [Memcached](http://www.php.net/manual/en/book.memcached.php), does provide SASL authentication and so is a fine option for using with MemCachier. We simply have less experience in using it at this time and so continue to recommend PHPMemcacheSASL.

We’ve built a small PHP example here: [MemCachier PHP sample app](https://github.com/memcachier/examples-php).


<h2 id="node.js">Node.js</h2>

For Node.js we recommend the use of the
[memjs](https://github.com/alevy/memjs) client library. It is written
and supported by MemCachier itself! To install, use the [node package
manager (npm)](https://npmjs.org/):

~~~~ text
npm install memjs
~~~~

Using it is straight-forward as memjs understands the
`MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME` and `MEMCACHIER_PASSWORD`
environment variables that the MemCachier add-on setups. For example:

~~~~ javascript
var memjs = require('memjs')
var mc = memjs.Client.create()
client.get('hello', function(val) {
    alert(val)
})
~~~~

We’ve built a small Node.js example here: [MemCachier Node.js sample app](http://github.com/memcachier/examples-node).


<h2 id="java">Java</h2>

For Java we recommend using the [SpyMemcached](https://code.google.com/p/spymemcached/) client. We also recommend using the [Apache Maven](https://maven.apache.org/) build manager for working with Java applications. If you aren't using `maven` and are instead using [Apache Ant](https://ant.apache.org/) or your own build system, then simply add the `spymemcached` jar file as a dependency of your application.

<div class="alert">Please make sure to use version <strong>2.8.9</strong> or earlier! At the moment, version 2.8.10 and later have an <a href="https://code.google.com/p/spymemcached/issues/detail?id=272">issue</a> with SASL authentication that makes them unusable with MemCachier.</div>

For `maven` however, start by configuring it to have the proper `spymemcached` repository:

~~~~ xml
<repository>
  <id>spy</id>
  <name>Spy Repository</name>
  <layout>default</layout>
  <url>http://files.couchbase.com/maven2/</url>
  <snapshots>
    <enabled>false</enabled>
  </snapshots>
</repository>
~~~~

Then add the `spymemcached` library to your dependencies:

~~~~ xml
<dependency>
  <groupId>spy</groupId>
  <artifactId>spymemcached</artifactId>
  <version>2.8.1</version>
  <scope>provided</scope>
</dependency>
~~~~

Once your build system is configured, you can start adding caching to your Java app:

~~~~ java
import java.io.IOException;
import net.spy.memcached.AddrUtil;
import net.spy.memcached.MemcachedClient;
import net.spy.memcached.ConnectionFactoryBuilder;
import net.spy.memcached.auth.PlainCallbackHandler;
import net.spy.memcached.auth.AuthDescriptor;

public class Foo {
  public static void main(String[] args) {
    AuthDescriptor ad = new AuthDescriptor(new String[] { "PLAIN" },
        new PlainCallbackHandler(<MEMCACHIER_USERNAME>,
            <MEMCACHIER_PASSWORD>));

    try {
      MemcachedClient mc = new MemcachedClient(new ConnectionFactoryBuilder()
          .setProtocol(ConnectionFactoryBuilder.Protocol.BINARY)
          .setAuthDescriptor(ad).build(), AddrUtil.getAddresses(<MEMCACHIER_SERVERS>));
      mc.set("foo", "bar");
      System.out.println(mc.get("foo"));
    } catch (IOException ioe) {
      System.err.println("Couldn't create a connection to MemCachier: \nIOException "
              + ioe.getMessage());
    }
  }
}
~~~~

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your [cache overview page](https://www.memcachier.com/caches).

You may wish to look the `spymemcached` [JavaDocs](https://dustin.github.com/java-memcached-client/apidocs/) or some more [example code](https://code.google.com/p/spymemcached/wiki/Examples) to help in using MemCachier effectively.

We’ve built a small Java example here, using Jetty: [MemCachier Java Jetty sample app](https://github.com/memcachier/examples-java).


<h2 id="clients">Client library support</h2>

MemCachier will work with any memcached binding that supports [SASL authentication](https://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer) and the [binary protocol](https://code.google.com/p/memcached/wiki/MemcacheBinaryProtocol). We have tested MemCachier with the following language bindings, although the chances are good that other SASL binary protocol packages will also work.

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
</td>
</tr>
<tr>
<td>Django</td>
<td>
  <a href="https://github.com/jbalogh/django-pylibmc">django-pylibmc</a>
</td>
</tr>
<tr>
<td>PHP</td>
<td>
  <a href="http://github.com/ronnywang/PHPMemcacheSASL">PHPMemcacheSASL</a> <b>or</b>
  <a href="http://www.php.net/manual/en/book.memcached.php">PHP Memcached</a>
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
  <a href="http://code.google.com/p/spymemcached/">spymemcached</a>
  (version <b>2.8.9</b> or earlier) <b>or</b>
  <a href="https://code.google.com/p/xmemcached/">xmemcached</a>
</td>
</tr>
<tr>
<td>Go</td>
<td><a href="https://github.com/bmizerany/mc">mc</a></td>
</tr>
<tr>
<td>Haskell</td>
<td><a href="http://hackage.haskell.org/package/memcache">memcache</a></td>
</tr>
</tbody>
</table>


<h2 id="sample-apps">Sample applications</h2>

We've built a number of working sample apps, too. Though keep in mind that these apps are built for Heroku, so they expect `MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME`, and `MEMCACHIER_PASSWORD` to be in the environment.

* [Sinatra Example](https://github.com/memcachier/examples-sinatra)
* [Rails Example](https://github.com/memcachier/examples-rails)
* [Django Example](https://github.com/memcachier/examples-django)
* [PHP Example](https://github.com/memcachier/examples-php)
* [Node.js Example](https://github.com/memcachier/examples-node)
* [Java Example](https://github.com/memcachier/examples-java)


<h2 id="local">Local usage</h2>

To test against your application locally, you will need to run a local memcached process. MemCachier is only available from the datacenter you signed up for. But because MemCachier and memcached speak the same protocol, you shouldn’t have any issues testing locally. Installation depends on your platform.

<div class="alert alert-info">The below examples will install memcached without SASL authentication support. This is generally what you want as client code can still try to use SASL auth and memcached will simply ignore the requests which is the same as allowing any credentials. So your client code can run without modification locally.</div>

On Ubuntu:

~~~~ text
$ sudo apt-get install memcached
~~~~

Or on OS X (with Homebrew):

~~~~ text
$ brew install memcached
~~~~

Or for Windows please refer to [these instructions](http://www.codeforest.net/how-to-install-memcached-on-windows-machine).

For further information and resources (such as the memcached source code) please refer to the [Memcache.org homepage](http://memcached.org)

To run memcached simply execute the following command:

~~~~ text
$ memcached -v
~~~~


<h2 id="analytics">MemCachier analytics</h2>

Our analytics dashboard is a simple tool that gives you more insight into how you’re using memcache. Here's a screenshot of the dashboard:

<p style="text-align:center;">
<img style="width:80%;" src="/images/analytics.png" alt="Analytics dashboard">
</p>

To access your application's analytics dashboard login to your [account](https://www.memcachier.com/caches) and view one of your caches.

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

<h2 id="advanced-analytics">Advanced analytics</h2>

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

<h2 id="newrelic">New Relic integration</h2>

MemCachier supports integration with your New Relic dashboard if you happen to be a customer of both MemCachier and New Relic. Currently this feature is only available to caches of <strong>500MB</strong> or larger. A blog post showing the integration can be found [here](http://blog.memcachier.com/2014/03/05/memcachier-and-new-relic-together/).

To setup the integration you will need to find your New Relic license key. This can be done by going to your "Account Settings" page when logged in to New Relic by click on your New Relic username in the top right corner. Then you will find your license key in the right side information column. It should be exactly 40 characters long. Please refer to the [blog post](http://blog.memcachier.com/2014/03/05/memcachier-and-new-relic-together/) for a visual walkthrough.

Once you have your New Relic licence key, it can be entered for your cache on the analytics dashboard page. In the bottom right corner there is a button to do this.

<h2 id="upgrading">Upgrading and downgrading</h2>

Changing your plan, either by upgrading or downgrading, requires no code changes. Your cache won't be lost, either.  Upgrading and downgrading Just Works™. Also, you are only ever charged by the hour for the time that you are on a certain plan. So try experimenting with different cache sizes knowing that you will only be charged for the hours you are on a plan, not for a whole month.

Changing your plan, either by upgrading or downgrading, can be done
easily at any time through your
[account](https://www.memcachier.com/caches).

* No code changes are required.
* Your cache won't be lost or reset<strong>*</strong>.
* You are charged by the hour for plans, so try experimenting with
  different cache sizes with low cost.

<p class="alert alert-info">
<strong>*</strong> When moving between the development plan to a
production plan, you <strong>will</strong> loose your cache. This is
unavoidable due to the strong separation between the development and
production clusters.
</p>

<h2 id="1mb-limit">Key-Value size limit (1MB)</h2>

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

<h2 id="localhost-errors">Errors about app trying to connect to localhost</h2>

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


<h2 id="support">Support</h2>

All MemCachier support and runtime issues should be submitted via email to <a href="mailto:support@memcachier.com"><i class="icon-envelope"></i> support@memcachier.com</a> or through our [support site](http://support.memcchier.com).

Any issues related to MemCachier service are reported at [MemCachier Status](http://status.memcachier.com/).

Please also follow us on twitter, <a href="https://twitter.com/MemCachier">@memcachier</a>, for status and product announcements.

