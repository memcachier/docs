
>callout
>Heroku recommends using a [CDN to speed up delivery of assets](https://devcenter.heroku.com/articles/using-amazon-cloudfront-cdn) over `Rack::Cache` for the best visitor experience. If you are already using a CDN, then adding `Rack::Cache` will not speed up delivery of assets.

Ruby on Rails applications should use
[Rack::Cache](http://rtomayko.github.com/rack-cache/) to efficiently
serve assets on the [Cedar stack](stack). Proper Rack::Cache usage
improves response time, decreases load and is important when serving
static assets through your application.

This article summarizes the concepts of caching assets using
Rack::Cache and walk you through the appropriate configuration of a
Rails 3.1+ application and the asset pipeline. This guide also works
perfectly with Rails 4 applications.


>callout
>We’ve built a small example app that can be seen running
>[here](http://memcachier-examples-rack.herokuapp.com/). <br>
><a class="github-source-code" href="https://github.com/memcachier/examples-rack-cache">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-rack-cache)

## Understanding Rack

[Rack](http://rack.github.io/) is a minimal interface between
webservers that support Ruby, and Ruby frameworks. Its purpose is to
act as a common interface, so that a webserver simply implements Rack
and can now support any ruby web framework that also supports Rack,
and vice-versa.

A nice feature that falls out of this design are so called
'middlewares'. A middleware is simply an application that implements
the Rack interface on both sides, that is, it consumes requests from a
webserver through the Rack interface and after some processing, passes
them onward to another application through the Rack interface. The
Rack interface in effect allows for any number of transparent
proxy-like services to be put between your webserver and application.
For an incoming HTTP request, each middleware performs some action,
then passes the request to the next middleware in the 'rack'.
Eventually the request is properly formatted and it will reach your
application.

Rack is written to be lightweight and flexible. If middleware can
respond to a request directly, then it doesn't have to hit your Rails
application. This means that the request is returned faster, and the
overall load on the Rails application is decreased.

Many Ruby web frameworks, including Rails 3+ and Sinatra, are built on
top of Rack.

## Rack::Cache

[Rack::Cache](http://rtomayko.github.io/rack-cache) is a Rack
middleware that enables HTTP caching on your application and allows an
application to serve assets from a storage backend without requiring
work from the main Rails application.

## Rack::Cache storage

Rack::Cache has two different storage areas: Meta and Entity stores.
The MetaStore keeps high level information about each cache entry
including HTTP request and response headers. When a request is
received, the core caching logic uses this meta information to
determine whether a fresh cache entry exists that can satisfy the
request. The EntityStore is where the actual response body content is
stored. When a response is entered into the cache, a SHA1 digest of
the response body content is calculated and used as a key.

Rack::Cache differentiates between MetaStore and EntityStore to allow
you as a user to customize what storage engine is used for each one
independently. MetaStore is accessed very frequently but requires
little memory, while EntityStore is accessed less often but requires
more memory.

Rack::Cache ships with three different storage engines: `file`,
`heap`, and `memcache`. Storing data in the `file` engine is slower
but memory efficient. Using `heap` means your process' memory will be
used which is quicker but can have an impact on performance if it
grows unbounded. Using `memcache` is the fastest option though it
isn't well suited to store large objects.

>callout
>For more information on the entity and meta stores read about [Rack Cache Storage](http://rtomayko.github.com/rack-cache/storage).

Using the MetaStore with the `memcache` storage engine, which allows
very quick access to shared meta-data, while using the `file` engine
for the EntityStore and its larger objects results in an efficient and
predictable application performance profile and is recommended on
Heroku.

## Install Memcached locally

>callout
>Local installation instructions for other OSs can be found in the [MemCachier add-on article](https://devcenter.heroku.com/articles/memcachier#local-usage).

To run your application locally and test the Rack::Cache setup you
will need to have memcached installed. You can install it on Mac OSX
using a tool such as homebrew.

```term
$ brew install memcached
```

At the end of installation homebrew will give you instructions on how
to start memcached manually and automatically on system start.

## Rails cache-store and Rack::Cache

Rails has it's own built-in caching system separate from Rack::Cache.
In general it serves a different purpose than Rack::Cache.

The rails caching system is for caching controller actions and page
fragments, it still invokes your rails code.  Rack::Cache on the other
hand manages caching of complete static assets such as stylesheets,
javascript and images. A cache hit never invokes your Rails code.
Rack::Cache is a replacement for a CDN or HTTP cache such as Varnish,
Nginx or Apache, while the rails caching system is orthogonal to
these.

You can find more on the rails caching system
[here](http://guides.rubyonrails.org/caching_with_rails.html#cache-stores).
Memcache is also a great choice and very well supported for use with
it.

## Configure Rails cache-store

This step configures the rails caching system to use memcached. This
isn't strictly necessary as the rails caching system is separate from
Rack::Cache. However, it's recommended to unify your caching systems.

You should install the Rack::Cache gem as well as the recommended
memcached client, [Dalli](https://github.com/mperham/dalli). In your
`Gemfile` add:

```ruby
gem 'rack-cache'
gem 'dalli'
```

While optional, it is also recommended to install the faster kgio IO
system:

```ruby
gem 'kgio'
```

After running `bundle install` to establish Dalli as an application
dependency tell Rails to use the Dalli client for its cache-store in
`config/application.rb`.

```ruby
config.cache_store = :dalli_store
```

Confirm your configuration by starting a local Rails console session
and getting/setting a simple key-value.

```term
$ rails c
> mc = Dalli::Client.new
> mc.set('foo', 'bar')
> mc.get('foo')
'bar'
```

Once you've configured your application to use memcached it's now time
to configure Rack::Cache.

## Configure Rack::Cache

Modify your `config/environments/production.rb` environment file to
specify the appropriate storage backends for Rails' built-in
Rack::Cache integration.

>callout
>If not specified, `Dalli::Client.new` automatically retrieves the memcache server location from the
>`MEMCACHE_SERVERS` environment variable. If it doesn't exist it will
> default to localhost and default port (11211).

```ruby
client = Dalli::Client.new((ENV["MEMCACHIER_SERVERS"] || "").split(","),
                           :username => ENV["MEMCACHIER_USERNAME"],
                           :password => ENV["MEMCACHIER_PASSWORD"],
                           :failover => true,
                           :socket_timeout => 1.5,
                           :socket_failure_delay => 0.2,
                           :value_max_bytes => 10485760)
config.action_dispatch.rack_cache = {
  :metastore    => client,
  :entitystore  => client
}
config.static_cache_control = "public, max-age=2592000"
```

You can find a full list of configuration options
[here](http://rtomayko.github.io/rack-cache/configuration), but the
above should be enough.

We set the `:value_max_bytes` option to 10MB as without this,
Rack::Cache will return a HTTP 5xx error response for any asset larger
than 1MB. This occurs as memcached by default only allows values of
1MB or smaller and so Dalli will throw an exception if you try to
`set` a key-value pair larger than 1MB. Increasing `:value_max_bytes`
to 10MB stops Dalli throwing this error and instead results in the
memcache server returning a miss for any assets larger than 1MB. So
while very large assets won't be served by Rack::Cache (not much
benefit for these kinds of assets anyway), they won't cause any
problems.

## Handling Multiple Dynos

While it is recommended to use the `file` storage engine for
EntityStorage, this is not possible on Heroku when using multiple
dynos. The problem is that when using `memcache` for the MetaStore,
then all metadata about what files aren't or are cached currently is
shared across all dynos. However, the `file` store is not, it is only
local to a dyno. So the first dyno to cache a file will store it on
its local disk but tell all other dynos that the cache contains the
file. The other dynos will now never find the actual file in their
cache since it doesn't exist.

The approach we take here is to use memcached for the EntityStore as
well. Another option would be to setup each dyno to use a dyno
specific prefix on keys for the MetaStore, keeping each dyno's
Rack::Cache independent.

Alternatively, memcached could be dropped altogether and a `heap`
store used for the MetaStore and a `file` store for the EntityStore.

## Serve static assets

>callout
>See the `production.rb` config of the [reference application](https://github.com/memcachier/examples-rack-cache/blob/master/config/environments/production.rb) on GitHub.

To allow your application to properly serve, invalidate and refresh
static assets, several configuration settings must be updated in
`config/environments/production.rb`. To have Rails to serve assets
(and so be managed by Rack::Cache), use the `serve_static_assets`
setting.

```ruby
config.serve_static_assets = true
```

Additionally, specify how long an item should stay cached by setting
the Cache-Control headers. Without a Cache-Control header static files
will not be stored by Rack::Cache.

```ruby
config.static_cache_control = "public, max-age=2592000"
```

These settings tell Rack::Cache to store static elements for a very
long time.

>note
>The `Cache-Control` header and, in general, [HTTP Caching](http-caching-ruby-rails), can be applied to dynamic content as well.

To properly invalidate modified files, Rails keeps a hash digest of
each file, storing it as part of the computed filename. This acts as a
fingerprint of a file so it can be detected when it has changed.
Enable this approach with the `config.assets.digest` setting.

```ruby
config.assets.digest = true
```

You also want to confirm that caching is turned on in production.

```ruby
config.action_controller.perform_caching = true
```

## Provision MemCachier add-on

Since you will use memcache as your Rack::Cache MetaStore, you will
need to add the [MemCachier
add-on](https://elements.heroku.com/addons/memcachier) to your application on
Heroku.

```term
$ heroku addons:create memcachier:dev
----> Adding memcachier on memcachier-direct... done, v24 (free)
```

MemCachier sets environment variables prefixed with `MEMCACHIER`
rather than `MEMCACHE`. The `memcachier` gem, however, fixes this for
you. Include it in your gemfile.

```ruby
gem "memcachier"
```

## Caching in production

Deploy the application to Heroku and use the `heroku logs` command to
view cache output.

```term
$ git push heroku master
$ heroku logs --ps web -t
```

>callout
>Using a hard refresh clears your browser cache and is useful for
>forcing asset requests. Most browsers will perform a hard refresh with the `Shift-R` shortcut.

You should see `cache` entries in your production log-stream. Seeing
`miss, store` tokens indicate that the item was not found in the cache
but has been saved for the next request.

```term
cache: [GET /assets/application-95bd4fe1de99c1cd91ec8e6f348a44bd.css] miss, store
cache: [GET /assets/application-95fca227f3857c8ac9e7ba4ffed80386.js] miss, store
cache: [GET /assets/rails-782b548cc1ba7f898cdad2d9eb8420d2.png] miss, store
```

Seeing `fresh` indicates that the item was found in your cache and
will be served from it.

```term
cache: [GET /assets/application-95bd4fe1de99c1cd91ec8e6f348a44bd.css] fresh
cache: [GET /assets/application-95fca227f3857c8ac9e7ba4ffed80386.js] fresh
cache: [GET /assets/rails-782b548cc1ba7f898cdad2d9eb8420d2.png] fresh
```

Congratulations! Your Rails 3.1+ application is now configured to
cache static assets using memcached, freeing up dynos to perform
dynamic application requests.

## Debugging

If a setting is not configured properly, you might see `miss` in your
logs instead of `store` or `fresh`.

```term
cache: [GET /assets/application-95bd4fe1de99c1cd91ec8e6f348a44bd.css] miss
cache: [GET /assets/application-95fca227f3857c8ac9e7ba4ffed80386.js] miss
cache: [GET /assets/rails-782b548cc1ba7f898cdad2d9eb8420d2.png] miss
```

When this happens ensure that the Cache-Control header exists by using
`curl` to inspect asset response headers.

```term
$ curl -I 'http://memcachier-examples-rack.herokuapp.com/assets/shipit-72351bb81da0eca408d9bd8342f1b972.jpg'
HTTP/1.1 200 OK
Age: 632
Cache-Control: public, max-age=2592000
Content-length: 70522
Etag: "72351bb81da0eca408d9bd8342f1b972"
Last-Modified: Sun, 25 Mar 2012 01:51:21 GMT
X-Rack-Cache: fresh
```

The response headers should contain `Cache-Control` with the value
specific in the `config.static_cache_control` setting i.e.: `public,
max-age=2592000`. Also confirm that you are seeing the `X-Rack-Cache`
header indicating the status of your asset (fresh/store/miss). If you
see unexpected results please check your production configuration
settings.

### Inconsistent file versions

If you modify a file and your server continues to serve the old file
check that you committed it to your git repository before deploying.
You can check to see if it exists in your compiled code by using
`heroku run bash` and listing the contents of the `public/assets`
directory. This directory should contain the hashed asset file names.

```term
$ heroku run bash
Running bash attached to terminal... up, run.1
$ ls public/assets
application-95bd4fe1de99c1cd91ec8e6f348a44bd.css      application.css           manifest.yml
application-95bd4fe1de99c1cd91ec8e6f348a44bd.css.gz   application.css.gz        rails-782b548cc1ba7f898cdad2d9eb8420d2.png
application-95fca227f3857c8ac9e7ba4ffed80386.js       application.js            rails.png
application-95fca227f3857c8ac9e7ba4ffed80386.js.gz    application.js.gz
```

Also confirm that the file is listed in Rails' `manifest.yml`.

```term
$ cat public/assets/manifest.yml
rails.png: rails-782b548cc1ba7f898cdad2d9eb8420d2.png
application.js: application-95fca227f3857c8ac9e7ba4ffed80386.js
application.css: application-95bd4fe1de99c1cd91ec8e6f348a44bd.css
```

If the file you're looking for does not show up try running `bundle
exec rake assets:precompile RAILS_ENV=production` locally and ensure
that it is in your own `public/assets` directory.
