
## Ruby Puma Webserver

If you are using the [Puma](http://puma.io/) webserver for your Ruby app (Rails
or otherwise), then you should take some additional steps due to the
multi-threaded runtime being used. This applies to all threaded webservers for
Ruby, not just Puma.

First, please refer to the documentation on [Rails](#rails-3-includes-rails-4-5) or
[Ruby](#ruby) above appropriately, and then take these additional steps.

Dalli by default uses a single connection to each server. This works fine
normally, but can become a bottleneck in a multi-threaded environment and
limit performance. In this case, Dalli supports connection pooling, where
multiple connections are created to MemCachier's servers. To use this, start by
adding the `connection_pool` gem to your Gemfile:

```ruby
gem 'connection_pool'
```

Next, you'll need to set the `:pool_size` configuration option when setting up
Dalli. For example, in Rails your configuration would become:

```ruby
config.cache_store = :dalli_store,
                    (ENV["MEMCACHIER_SERVERS"] || "").split(","),
                    {:username => ENV["MEMCACHIER_USERNAME"],
                     :password => ENV["MEMCACHIER_PASSWORD"],
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2,
                     :down_retry_delay => 60,
                     :pool_size => 5
                    }
```

Where the number 5 should be chosen according to how many threads you will be
running and the available concurrency on the machines running your webserver.
