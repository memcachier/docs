
## Ruby

**IF(direct)**
<p class="alert alert-info">
We’ve built a small Ruby example using Sinatra here:
<a href="https://github.com/memcachier/examples-sinatra">MemCachier Sinatra Sample App</a>.
</p>
**ENDIF**

**IF(heroku)**
>callout
>We’ve built a small Ruby Sinatra example.
><a class="github-source-code" href="http://github.com/memcachier/examples-sinatra">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-sinatra).
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

You can now start writing some code. First, you'll need to create a
client object with the correct credentials and settings:

```ruby
require 'dalli'
cache = Dalli::Client.new((ENV["MEMCACHIER_SERVERS"] || "").split(","),
                    {:username => ENV["MEMCACHIER_USERNAME"],
                     :password => ENV["MEMCACHIER_PASSWORD"],
                     :failover => true,            # default is true
                     :socket_timeout => 1.5,       # default is 0.5
                     :socket_failure_delay => 0.2, # default is 0.01
                     :down_retry_delay => 60       # default is 60
                    })
```

**IF(direct)**
<p class="alert alert-info">
The values for `MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME`, and
`MEMCACHIER_PASSWORD` are listed on your
[cache overview page](https://www.memcachier.com/caches). Make sure to add them
to your environment.
</p>
**ENDIF**

Now you can use the cache through simple `get` and `set` operations,
as well as many others.

```ruby
cache.set("foo", "bar")
puts cache.get("foo")
```

**IF(direct)**
You can also get an insight into your cache usage (number of keys stored and
bytes) with the `stats` command:

```ruby
cache.stats
=> {"memcachier.example.net:11211" => {"cur_items" => "49982", "bytes" => "89982234"} }
```
**ENDIF**

**IF(heroku)**
### Testing (Ruby)

The easiest way to test that your setup is working is through the
heroku console:

```term
$ heroku run console --app <app>
>> require 'dalli'
>> cache = Dalli::Client.new(ENV["MEMCACHIER_SERVERS"].split(","),
                        {:username => ENV["MEMCACHIER_USERNAME"],
                         :password => ENV["MEMCACHIER_PASSWORD"]
                        })
>> cache.set('memcachier', 'rocks')
=> true
```

And then fetch the value back:

```term
>> cache.get('memcachier')
=> "rocks"
```

You can also get an insight into your cache usage (number of keys
stored and bytes) with the `stats` command:

```term
>> cache.stats
=> {"memcachier.example.net:11211" => {"cur_items" => "49982", "bytes" => "89982234"} }
```
**ENDIF**
