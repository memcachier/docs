<style>
h2 {
  font-size:26px;
  color: #555;
}
code {
  color: #444;
  background: #f0f6fc;
  border: 1px solid #d2dce6;
}
pre {
  background: #434e56;
  border: #1px solid #3f464c;
  border-radius: 3px;
  line-height: 18px;
  color: #EAEAEA;
}
</style>

MemCachier is an implementation of the
[Memcache](http://memcached.org) in-memory key/value store used for
caching data. It is a key technology in modern web applications for
scaling and reducing server loads. The MemCachier add-on manages and
scales clusters of memcache servers so you can focus on your app. Tell
us how much memory you need and get started for free instantly. Add
capacity later as you need it.

The information below will quickly get you up and running with the
MemCachier add-on. For information on the benefits of MemCachier and
how it works, please refer to the more extensive
[User Guide](http://www.memcachier.com/documentation/memcache-user-guide/).

## Signup

[Signup with MemCachier](https://my.memcachier.com) if you haven't
already. You will need to verify your email address after you've
signed up. We don't require a credit card if you choose a free plan.

## Create a MemCachier App

After you've verified your email address, you can start creating an
application.  Creating an application requires you to choose a plan
and name the application.

Once you've created an application, follow the below getting started
instructions to begin using the cache.

<p class="alert alert-info">Your credentials may take up to three (3) minutes to be synced to our servers. You may see authentication errors if you start using the cache immediately.</p>

## Getting started

We have documentation for the following languages and frameworks:

* [Ruby](#ruby)
* [Rails](#rails)
* [Django](#django)
* [PHP](#php)
* [Node.js](#node.js)
* [Java](#java)

We also have documentation on MemCachier usasge in general:

* [Supported client libraries](#clients)
* [Example applications](#sample-apps)
* [Local usage](#local)
* [MemCachier analytics](#analytics)
* [Changing plans](#upgrading)
* [Getting support](#support)


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
                     :password => <MEMCACHIER_PASSWORD>})
~~~~

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your application's page on [my.memcachier.com](https://my.memcachier.com).

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


<h2 id="rails">Rails</h2>

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
                     :password => <MEMCACHIER_PASSWORD>}
~~~~

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your application's page on [my.memcachier.com](https://my.memcachier.com).

<p class="alert alert-info">In your development environment, Rails.cache defaults to a simple in-memory store and so it doesn’t require a running memcached.</p>

From here you can use the following code examples to use the cache in your Rails app:

~~~~ ruby
Rails.cache.write("foo", "bar")
puts Rails.cache.read("foo")
~~~~

We’ve built a small Rails example here: [MemCachier Rails sample app](https://github.com/memcachier/examples-rails).


<h2 id="django">Django</h2>

MemCachier has been tested with the `pylibmc` memcache client, but the default client doesn’t support SASL authentication. Run the following commands on your machine to install the necessary pips:

~~~~ text
$ sudo port install libmemcached
$ LIBMEMCACHED=/opt/local pip install pylibmc
$ pip install django-pylibmc-sasl
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

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your application's page on my.memcachier.com.  Note that Django expects <MEMCACHIER_SERVERS> to be semicolon-delimited.

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
$m->setSaslAuthData(getenv("MEMCACHIER_USERNAME"), getenv("MEMCACHIER_PASSWORD"));

$m->add("foo", "bar");
echo $m->get("foo");
~~~~

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your application's page on [my.memcachier.com](https://my.memcachier.com).

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

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and `<MEMCACHIER_PASSWORD>` are listed on your application's page on [my.memcachier.com](https://my.memcachier.com).

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
<img style="width:85%;" src="https://www.evernote.com/shard/s17/sh/345fff03-736e-488c-a96a-c999f97757ae/6d7472dac4d27e74046d1290403732b3/deep/0/Screenshot%204/26/13%205:14%20PM.png" alt="Analytics dashboard">
</p>

To access your application's analytics dashboard login to your account at [my.memcachier.com](https://my.memcachier.com).


<h2 id="upgrading">Upgrading and downgrading</h2>

Changing your plan, either by upgrading or downgrading, requires no code changes.  Your cache won't be lost, either.  Upgrading and downgrading Just Works™. Also, you are only ever charged by the hour for the time that you are on a certain plan. So try experimenting with different cache sizes knowing that you will only be charged for the hours you are on a plan, not for a whole month.


<h2 id="support">Support</h2>

All MemCachier support and runtime issues should be submitted via email to <a href="mailto:support@memcachier.com"><i class="icon-envelope"></i> support@memcachier.com</a>.

Any issues related to MemCachier service are reported at [MemCachier Status](http://status.memcachier.com/).

Please also follow us on twitter, <a href="https://twitter.com/MemCachier">@memcachier</a>, for status and product announcements.

