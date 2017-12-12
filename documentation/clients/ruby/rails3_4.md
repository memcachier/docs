
## Rails 3 & 4

**IF(direct)**
<p class="alert alert-info">
We’ve built a small Rails example here:
<a href="https://github.com/memcachier/examples-rails">MemCachier Rails sample app</a>.
</p>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Rails example.
><a class="github-source-code" href="https://github.com/memcachier/examples-rails">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-rails).

We also have a tutorial on using MemCachier with Rails [here](building-a-rails-3-application-with-memcache).

Here we explain how you setup and install MemCachier with Rails. Refer
to the [Rails caching
guide](http://guides.rubyonrails.org/caching_with_rails.html)
for information on how you use MemCachier with Rails. Rails supports
automatic whole site caching, per-view caching and fragment caching.
**ENDIF**

Start by adding the [dalli](https://github.com/mperham/dalli) gem to your
Gemfile. `Dalli` is a Ruby memcache client.

```ruby
gem 'dalli'
```

Then run bundle install:

```term
$ bundle install
```

Once this gem is installed you’ll want to configure the Rails `cache_store`
appropriately. Modify your `config/environments/production.rb` with the
following:

```ruby
config.cache_store = :dalli_store,
**IF(direct)**
                    <MEMCACHIER_SERVERS>.split(","),
                    {:username => <MEMCACHIER_USERNAME>,
                     :password => <MEMCACHIER_PASSWORD>
**ENDIF**
**IF(heroku)**
                    (ENV["MEMCACHIER_SERVERS"] || "").split(","),
                    {:username => ENV["MEMCACHIER_USERNAME"],
                     :password => ENV["MEMCACHIER_PASSWORD"],
**ENDIF**
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2,
                     :down_retry_delay => 60
                    }
```

**IF(direct)**
The values for `<MEMCACHIER_SERVERS>`, `<MEMCACHIER_USERNAME>`, and
`<MEMCACHIER_PASSWORD>` are listed on your [cache overview
page](https://www.memcachier.com/caches).

<p class="alert alert-info">
In your development environment, Rails.cache defaults to a simple
in-memory store and so it doesn't require a running memcached.
</p>
**ENDIF**

**IF(heroku)**
>callout
>In your development environment, Rails.cache defaults to a simple
>in-memory store and so it doesn’t require a running memcached.
**ENDIF**

From here you can use the following code examples to use the cache in your
Rails app:

```ruby
Rails.cache.write("foo", "bar")
puts Rails.cache.read("foo")
```

**IF(heroku)**
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
**ENDIF**
