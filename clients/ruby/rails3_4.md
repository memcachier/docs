

<h2 id="rails3">Rails 3 & 4</h2>

Start by adding the [dalli](https://github.com/mperham/dalli) gem to your Gemfile.

```ruby
gem 'dalli'
```

Then bundle install:

```text
$ bundle install
```

`Dalli` is a Ruby memcache client. Once it is installed you’ll want to
configure the Rails cache_store appropriately. Modify
`config/environments/production.rb` with the following:

```ruby
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

From here you can use the following code examples to use the cache in your
Rails app:

```ruby
Rails.cache.write("foo", "bar")
puts Rails.cache.read("foo")
```

We’ve built a small Rails example here: [MemCachier Rails sample
app](https://github.com/memcachier/examples-rails).
