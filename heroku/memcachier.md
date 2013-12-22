---
title: MemCachier
id: 674


[MemCachier](http://www.memcachier.com) is an implementation of the
[Memcache](http://memcached.org) in-memory key/value store used for
caching data. It is a key technology in modern web applications for
scaling and reducing server loads. The MemCachier add-on manages and
scales clusters of memcache servers so you can focus on your app. Tell
us how much memory you need and get started for free instantly. Add
capacity later as you need it.

## Getting started

Start by installing the add-on:

    :::term
    $ heroku addons:add memcachier:dev

You can start with more memory if you know you’ll need it:

    :::term
    $ heroku addons:add memcachier:100
    $ heroku addons:add memcachier:500
     ... etc ...

Once the add-on has been added you’ll notice three new variables in
`heroku config`:

    :::term
    $ heroku config
    ...
    MEMCACHIER_SERVERS    => mcX.ec2.memcachier.com
    MEMCACHIER_USERNAME   => bobslob
    MEMCACHIER_PASSWORD   => l0nGr4ndoMstr1Ngo5strang3CHaR4cteRS
    ...

Next, setup your app to start using the cache. We have documentation
for the following languages and frameworks:

* [Ruby](#ruby)
* [Rails 3 & 4](#rails-3-and-4)
* [Rails 2](#rails2)
* [Django](#django)
* [PHP](#php)
* [Node.js](#node.js)
* [Java](#java)

<p class="note">
Your credentials may take up to three (3) minutes to
be synced to our servers. You may see authentication errors if you
start using the cache immediately.
</p>

## Ruby

<p class="callout" markdown="1">
We’ve built a small Ruby example using Sinatra here: [MemCachier
Sinatra sample app](http://github.com/memcachier/examples-sinatra).
</p>

Start by adding the
[memcachier](http://github.com/memcachier/memcachier-gem) and
[dalli](http://github.com/mperham/dalli) gems to your Gemfile.

    :::ruby
    gem 'memcachier'
    gem 'dalli'

Then bundle install:

    :::term
    $ bundle install

`Dalli` is a Ruby memcache client, and the `memcachier` gem modifies
the environment (`ENV`) such that the environment variables set by
MemCachier will work with Dalli. Once these gems are installed you can
start writing code. The following is a basic example showing get and
set.

    :::ruby
    require 'dalli'
    require 'memcachier'
    cache = Dalli::Client.new
    cache.set("foo", "bar")
    puts cache.get("foo")

Without the `memcachier` gem, you’ll need to pass the proper
credentials to `Dalli`:

    :::ruby
    cache = Dalli::Client.new(ENV["MEMCACHIER_SERVERS"].split(","),
                        {:username => ENV["MEMCACHIER_USERNAME"],
                         :password => ENV["MEMCACHIER_PASSWORD"],
                         :failover => true,
                         :socket_timeout => 1.5,
                         :socket_failure_delay => 0.2
                        })

### Testing (Ruby)

The easiest way to test that your setup is working is through the
heroku console:

    :::term
    $ heroku run console --app <app>
    >> require 'dalli'
    >> require 'memcachier'
    >> dc = Dalli::Client.new
    >> dc.set('memcachier', 'rocks')
    => true

And then fetch the value back:

    :::term
    >> dc.get('memcachier')
    => "rocks"

You can also get an insight into your cache usage (number of keys
stored and bytes) with the `stats` command:

    :::term
    >> dc.stats
    => {"memcachier.example.net:11211" => {"cur_items" => "49982", "bytes" => "89982234"} }

## Rails 3 and 4

<p class="callout" markdown="1">
We’ve built a small Rails example here: [MemCachier Rails sample
app](http://github.com/memcachier/examples-rails).
</p>

Start by adding the
[memcachier](http://github.com/memcachier/memcachier-gem) and
[dalli](http://github.com/mperham/dalli) gems to your Gemfile.

    :::ruby
    gem 'memcachier'
    gem 'dalli'

Then run bundle install:

    :::term
    $ bundle install

`Dalli` is a Ruby memcache client, and the `memcachier` gem modifies
the environment (`ENV`) such that the environment variables set by
MemCachier will work with Dalli. Once these gems are installed you’ll
want to configure the Rails cache_store appropriately. Modify
`config/environments/production.rb` with the following:

    :::ruby
    config.cache_store = :dalli_store

<p class="callout" markdown="1">
In your development environment, Rails.cache defaults to a simple
in-memory store and so it doesn’t require a running memcached.
</p>

From here you can use the following code examples to use the cache in
your Rails app:

    :::ruby
    Rails.cache.write("foo", "bar")
    puts Rails.cache.read("foo")

Without the `memcachier` gem, you’ll need to pass the proper
credentials to Dalli in `config/environments/production.rb`:

    :::ruby
    config.cache_store = :dalli_store,
                        (ENV["MEMCACHIER_SERVERS"] || "").split(","),
                        {:username => ENV["MEMCACHIER_USERNAME"],
                         :password => ENV["MEMCACHIER_PASSWORD"],
                         :failover => true,
                         :socket_timeout => 1.5,
                         :socket_failure_delay => 0.2
                        }

<p class="callout" markdown="1">
It is possible you will run into a configuration problem if you are
using Rails 3.1 and the Heroku Cedar platform. Information on how to
fix that issue can be found at [this Stackoverflow
answer](http://stackoverflow.com/questions/6458947/rails-3-1-heroku-cedar-static-image-assets-are-not-being-served)
</p>

### Testing (Rails)

To test locally you can simply use the rails console:

    :::term
    rails console
    >> Rails.cache.write('memcachier', 'rocks')
    => true
    >> Rails.cache.read('memcachier')
    => "rocks"

To test against MemCachier itself, please refer to the [Ruby testing
instructions](#testing-ruby).

## Rails 2

Start by adding the
[memcachier](http://github.com/memcachier/memcachier-gem) and
[dalli](http://github.com/mperham/dalli) gems to your Gemfile. You
will need to use dalli **v1.0.5** as later versions of Dalli don't
support Rails 2.

    :::ruby
    gem 'memcachier'
    gem 'dalli', '~>1.0.5'

Then run bundle install:

    :::term
    $ bundle install

`Dalli` is a Ruby memcache client, and the `memcachier` gem modifies
the environment (`ENV`) such that the environment variables set by
MemCachier will work with Dalli. Once these gems are installed you’ll
want to configure the Rails cache_store appropriately. Modify
`config/environments/production.rb` with the following:

    :::ruby
    require 'active_support/cache/dalli_store23'
    config.cache_store = :dalli_store

<p class="callout" markdown="1">
In your development environment, Rails.cache defaults to a simple
in-memory store and so it doesn’t require a running memcached.
</p>

In `config/environment.rb`:

    :::ruby
    config.gem 'dalli'

From here you can use the following code examples to use the cache in
your Rails app:

    :::ruby
    Rails.cache.write("foo", "bar")
    puts Rails.cache.read("foo")

Without the `memcachier` gem, you’ll need to pass the proper
credentials to Dalli in `config/environments/production.rb`:

    :::ruby
    config.cache_store = :dalli_store,
                        (ENV["MEMCACHIER_SERVERS"] || "").split(","),
                        {:username => ENV["MEMCACHIER_USERNAME"],
                         :password => ENV["MEMCACHIER_PASSWORD"],
                         :failover => true,
                         :socket_timeout => 1.5,
                         :socket_failure_delay => 0.2
                        }

### Testing (Rails)

To test locally you can simply use the rails console:

    :::term
    rails console
    >> Rails.cache.write('memcachier', 'rocks')
    => true
    >> Rails.cache.read('memcachier')
    => "rocks"

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

<p class="callout" markdown="1">
We’ve built a small Django example here: [MemCachier Django sample
app](http://github.com/memcachier/examples-django).
</p>

MemCachier has been tested with the `pylibmc` memcache client, but the
default client doesn’t support SASL authentication. Run the following
commands on your local machine to install the necessary pips:

    :::term
    $ sudo port install libmemcached
    $ LIBMEMCACHED=/opt/local pip install pylibmc
    $ pip install django-pylibmc-sasl

Be sure to update your `requirements.txt` file with these new
requirements (note that your versions may differ than what’s below):

    pylibmc==1.2.2
    django-pylibmc-sasl==0.2.4

Next, configure your settings.py file the following way:

    :::python
    os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
    os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

    CACHES = {
      'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': {
            'tcp_nodelay': True,
            'remove_failed': 4
        }
      }
    }

From here you can start writing cache code in your Django app:

    :::python
    from django.core.cache import cache
    cache.set("foo", "bar")
    print cache.get("foo")

You may be interested in the
[django-heroku-memcacheify](http://github.com/rdegges/django-heroku-memcacheify)
pip, which fully configures MemCachier with one line of code for any
Django app the pip supports.

<p class="note" markdown="1">
A confusing error message you may get from `pylibmc` is
**MemcachedError: error 37 from memcached_set: SYSTEM ERROR(Resource
temporarily unavailable)**. This indicates that you are trying to
store a value larger than 1MB. MemCachier has a hard limit of 1MB for
the size of key-value pairs. To work around this, either consider
sharding the data or using a different technology. The benefit of an
in-memory key-value store diminishes at 1MB and higher.
</p>

## PHP

<p class="callout" markdown="1">
We’ve built a small PHP example here: [MemCachier PHP sample
app](http://github.com/memcachier/examples-php).
</p>

We recommend users utilize the
[PHPMemcacheSASL](http://github.com/ronnywang/PHPMemcacheSASL) client
as we have more experience in using and supporting it. Start by
downloading the
[PHPMemcacheSASL](http://github.com/ronnywang/PHPMemcacheSASL)
library. From here you can start writing cache code in your PHP app:

    :::php
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

The more common PHP memcache clients have limited support for working
with MemCachier due to issues with SASL authentication. The
[Memcache](http://www.php.net/manual/en/book.memcache.php) simply
doesn't provide SASL authentication support and so is not an option.
The [Memcached](http://www.php.net/manual/en/book.memcached.php), does
provide SASL authentication and so is a fine option for using with
MemCachier. We simply have less experience in using it at this time
and so continue to recommend PHPMemcacheSASL.

## Node.js

<p class="callout" markdown="1">
We’ve built a small Node.js example here: [MemCachier Node.js sample
app](http://github.com/memcachier/examples-node).
</p>

For Node.js we recommend the use of the
[memjs](http://github.com/alevy/memjs) client library. It is written
and supported by MemCachier itself! To install, use the [node package
manager (npm)](http://npmjs.org/):

    :::term
    npm install memjs

Using it is straight-forward as memjs understands the
`MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME` and `MEMCACHIER_PASSWORD`
environment variables that the MemCachier add-on setups. For example:

    :::javascript
    var memjs = require('memjs')
    var mc = memjs.Client.create()
    mc.get('hello', function(val) {
        alert(val)
    })

## Java

<p class="callout" markdown="1">
We’ve built a small Java example here, using Jetty: [MemCachier Java
sample app](http://github.com/memcachier/examples-java).
</p>

For Java we recommend using the
[SpyMemcached](http://code.google.com/p/spymemcached/) client. We also
recommend using the [Apache Maven](http://maven.apache.org/) build
manager for working with Java applications. If you aren't using
`maven` and are instead using [Apache Ant](http://ant.apache.org/) or
your own build system, then simply add the `spymemcached` jar file as
a dependency of your application.

<p class="warning" markdown="1">Please make sure to use version
__2.8.9__ or earlier! At the moment, version 2.8.10 and later have an
[issue](http://code.google.com/p/spymemcached/issues/detail?id=272)
with SASL authentication that makes them unusable with MemCachier.</p>

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

    :::java
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

<p class="callout" markdown="1">
It is possible that you will run into Java exceptions about the class
loader. (See Spymemcached [issue
155](http://code.google.com/p/spymemcached/issues/detail?id=155). The
reported issue also contains a suggested work around.
</p>

You may wish to look the `spymemcached`
[JavaDocs](http://dustin.github.com/java-memcached-client/apidocs/) or
some more [example
code](http://code.google.com/p/spymemcached/wiki/Examples) to help in
using MemCachier effectively.

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
  <a href="http://github.com/ronnywang/PHPMemcacheSASL">PHPMemcacheSASL</a> <b>or</b>
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

## Sample apps

We've built a number of working sample apps, too:

* [Sinatra Example](https://github.com/memcachier/examples-sinatra)
* [Rails Example](https://github.com/memcachier/examples-rails)
* [Django Example](https://github.com/memcachier/examples-django)
* [PHP Example](https://github.com/memcachier/examples-php)
* [Node.js Example](https://github.com/memcachier/examples-node)
* [Java Example](https://github.com/memcachier/examples-java)

## Local usage

To test your Heroku application locally, you will need to run a local
memcached server. MemCachier can only run in Heroku, but because
MemCachier and memcached speak the same protocol, you shouldn’t have
any issues testing locally. Installation depends on your platform.

<p class="callout" markdown="1">
This will install memcached without SASL authentication support. This
is generally what you want as client code can still try to use SASL
auth and memcached will simply ignore the requests which is the same
as allowing any credentials. So your client code can run without
modification locally and on Heroku.
</p>

On Ubuntu:

    :::term
    $ sudo apt-get install memcached

Or on OS X (with Homebrew):

    :::term
    $ brew install memcached

Or for Windows please refer to [these
instructions](http://www.codeforest.net/how-to-install-memcached-on-windows-machine).

For further information and resources (such as the memcached source
code) please refer to the [Memcache.org
homepage](http://memcached.org)

To run memcached simply execute the following command:

    :::term
    $ memcached -v

## Usage analytics

Our analytics dashboard is a simple tool that gives you more insight
into how you’re using memcache.  Here's a screenshot of the dashboard:

![Analytics Dashboard](https://www.memcachier.com/images/analytics.png)

To access your application's analytics dashboard run:

    :::term
    $ heroku addons:open memcachier

Or open MemCachier from your application's dashboard on heroku.com.

## Switching from the Memcache add-on

If you're switching from the [other Memcache add-on provided by
Couchbase](http://addons.heroku.com/memcache), the only change you'll
need to make is to your environment variables.

Most memcache client look for the environment variables,
`MEMCACHE_SERVERS`, `MEMCACHE_USERNAME` and `MEMCACHE_PASSWORD` for
their configuration.  If these environment variables aren't set,
clients generally default to connecting to `127.0.0.1:11211` (i.e.,
localhost).

The deprecated Couchbase Memcache add-on set the `MEMCACHE_*`
variables for your app. The MemCachier add-on however sets the
`MEMCACHIER_*` environment variables. So you'll need to translate them
across.

If you're using Ruby/Rails, then simply install the `memcachier` gem
which does this.  Add the following to your `Gemfile`:

    :::ruby
    gem 'memcachier'

Then run `$ bundle install`

<p class="warning">
Some older versions of Dalli require the Memcache add-on to be fully
removed before MemCachier can work correctly. Please either upgrade to
the latest version of Dalli, remove the Memcache add-on or use the
memcachier gem. Either of these will solve the issue.
</p>

If you're using `Python, Django, PHP, Java`, or any other language or
platform, simply jigger your environment variables.  All `MEMCACHE_*`
variables should be assigned to the values held in the `MEMCACHIER_*`
variables.  The below code is pseudo-code -- adapt it to your language
by referring to our documentation above for your given
language/framework:

    env[MEMCACHE_SERVERS] = env[MEMCACHIER_SERVERS]
    env[MEMCACHE_USERNAME] = env[MEMCACHIER_USERNAME]
    env[MEMCACHE_PASSWORD] = env[MEMCACHIER_PASSWORD]

With your environment variables jiggered such that `MEMCACHE_*` has
the values of `MEMCACHIER_*`, your existing client should work with
MemCachier and you shouldn't need to change any other code.

## Upgrading and downgrading

Changing your plan, either by upgrading or downgrading, can be done
easily at any time through Heroku.
* No code changes are required.
* Your cache won't be lost or reset<strong>*</strong>.
* You are charged by the hour for plans, so try experimenting with
  different cache sizes with low cost.

<p class="note" markdown="1">
<strong>\*</strong> When moving between the development plan to a
production plan, you __will__ loose your cache. This is unavoidable
due to the strong separation between the development and production
clusters.
</p>

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
of the [Heroku Support channels](support-channels). Any non-support
related issues or product feedback is welcome via email at:
[support@memcachier.com](mailto:support@memcachier.com)

Any issues related to MemCachier service are reported at [MemCachier
Status](http://status.memcachier.com/).

Please also follow us on twitter, <a
href="http://twitter.com/MemCachier">@memcachier</a>, for status and
product announcements.

