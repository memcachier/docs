**IF(direct)**
---
title: "Documentation: Rails"
description: "Documentation for using MemCachier with Rails"
---
**ENDIF**

## Rails

**IF(direct)**
<div class="alert alert-info">
  <p><a href="https://github.com/memcachier/examples-rails">MemCachier Rails sample app</a>.</p>
  <p>Related tutorials:</p>
  <ul>
    <li><a href="https://blog.memcachier.com/2023/06/07/deploy-rails-and-memcache-on-render/">Deploy Rails and Memcache on Render: A How-To Guide</a></li>
    <li><a href="https://devcenter.heroku.com/articles/building-a-rails-3-application-with-memcache">Building a Rails 5 Application with Memcache on Heroku</a></li>
  </ul>
</div>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Rails example.
><a class="github-source-code" href="https://github.com/memcachier/examples-rails">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-rails).

We also have a tutorial on using MemCachier with Rails
[here](building-a-rails-3-application-with-memcache).

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
config.cache_store = :mem_cache_store,
                    (ENV["MEMCACHIER_SERVERS"] || "").split(","),
                    {:username => ENV["MEMCACHIER_USERNAME"],
                     :password => ENV["MEMCACHIER_PASSWORD"],
                     :failover => true,
                     :socket_timeout => 1.5,
                     :socket_failure_delay => 0.2,
                     :down_retry_delay => 60
                    }
```

**IF(direct)**
<p class="alert alert-info">
The values for <code>MEMCACHIER_SERVERS</code>, <code>MEMCACHIER_USERNAME</code>, and
<code>MEMCACHIER_PASSWORD</code> are listed on your
<a href="https://www.memcachier.com/caches">cache overview page</a>. Make sure to add them
to your environment.
</p>

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

### Rails 2

When adding the [dalli](https://github.com/mperham/dalli) gem to your Rails 2
Gemfile you will need to use dalli **v1.0.5** as later versions of Dalli don't
support Rails 2.

```ruby
gem 'dalli', '~>1.0.5'
```

Also modify `config/environment.rb` to contain:

```ruby
config.gem 'dalli'
```

Else proceed just as newer Rails versions.
