
## Ruby

Start by adding the [dalli](https://github.com/mperham/dalli) gem to your
Gemfile.

```ruby
gem 'dalli'
```

Then bundle install:

```shell
$ bundle install
```

`Dalli` is a Ruby memcache client. Once it is installed you can start writing
code. The following is a basic example showing get and set.

```ruby
cache = Dalli::Client.new(<MEMCACHIER_SERVERS>.split(","),
                    {:username => <MEMCACHIER_USERNAME>,
                     :password => <MEMCACHIER_PASSWORD>
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2,
                     :down_retry_delay => 60
                    })
```

The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and
`<MEMCACHIER_PASSWORD>` are listed on your [cache overview
page](https://www.memcachier.com/caches).

From here you can use the following code examples to use the cache in your Ruby
app:

```ruby
cache.set("foo", "bar")
puts cache.get("foo")
```

You can also get an insight into your cache usage (number of keys stored and
bytes) with the `stats` command:

```ruby
cache.stats
=> {"memcachier.example.net:11211" => {"cur_items" => "49982", "bytes" => "89982234"} }
```

We’ve built a small Ruby example using Sinatra here: [MemCachier Sinatra Sample
App](https://github.com/memcachier/examples-sinatra).
