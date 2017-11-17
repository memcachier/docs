
## Rails 2

Start by adding the [dalli](https://github.com/mperham/dalli) gem to your
Gemfile. You will need to use dalli **v1.0.5** as later versions of Dalli don't
support Rails 2.

```ruby
gem 'dalli', '~>1.0.5'
```

Then bundle install:

```shell
$ bundle install
```

`Dalli` is a Ruby memcache client. Once it is installed you’ll want to
configure the Rails cache_store appropriately. Modify
`config/environments/production.rb` with the following:

```ruby
require 'active_support/cache/dalli_store23'
config.cache_store = :dalli_store, <MEMCACHIER_SERVERS>.split(","),
                    {:username => <MEMCACHIER_USERNAME>,
                     :password => <MEMCACHIER_PASSWORD>
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2,
                     :down_retry_delay => 60
                    }
```

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and
`<MEMCACHIER_PASSWORD>` are listed on your [cache overview
page](https://www.memcachier.com/caches).

<p class="alert alert-info">
In your development environment, Rails.cache defaults to a simple
in-memory store and so it doesn't require a running memcached.
</p>

Also modify `config/environment.rb` to contain:

```ruby
config.gem 'dalli'
```

From here you can use the following code examples to use the cache in your
Rails app:

```ruby
Rails.cache.write("foo", "bar")
puts Rails.cache.read("foo")
```

We’ve built a small Rails (3 & 4) example here: [MemCachier Rails sample
app](https://github.com/memcachier/examples-rails).
