
Despite being the go-to scaling solution for most production websites,
Memcache often isn’t used to its full potential. Most developers only
know about the `get`, `set`, and `delete` operations. However,
Memcache has a broader set of operations that help developers build
more advanced apps with less code and even further improved
performance.

This article will outline the more useful advanced Memcache operations
with a series of real-world use-cases and show their impact on app
implementation and performance.

## Prerequisites

This article assumes you have the following:

* A Heroku account. [Signup is free and
  instant.](https://signup.heroku.com/devcenter-advanced-memcache)
* The [Heroku CLI](https://cli.heroku.com/) installed.
* Basic familiarity with Memcache.

## Test environment

Start by deploying the following Rails app to Heroku:  
<a class="github-source-code" href="http://github.com/memcachier/rails_sandbox">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/rails_sandbox)

This will give you a sandbox environment complete with the [MemCachier
add-on](https://elements.heroku.com/addons/memcachier) and a simple command
line, allowing you to run advanced Memcache operations yourself.
Entering the commands directly instead of just reading over their
description will reinforce their syntax and increase your familiarity
with them.

You now have a copy of the test app deployed to your Heroku account.
Take note of the URL of your new app. It resembles something like
`http://serene-mesa-2821.herokuapp.com/` where `serene-mesa-2821` is
the name of your application on Heroku. You will need this name to
establish an interactive shell.

## Interactive shell

Use `heroku run console` from your terminal with your app name to
connect to an instance of your app running on Heroku. Load the
Memcache client libraries and perform basic `set` and `get` commands
to confirm setup.

```ruby
$ heroku run console -a app-name
irb> cache = Dalli::Client.new
irb> cache.set("foo", "bar")
=> true
irb> cache.get("foo")
=> "bar"
```

>note
>This example uses an interactive Ruby shell with the Dalli client to
>load and interact with Memcache. This is only for demonstration
>purposes as any language's Memcache driver will support similar
>commands.

The rest of this guide assumes you have this shell running and client
libraries loaded.

## Cache expiration

The biggest challenge when using Memcache is avoiding cache staleness
while still writing clean code. Most developers store data to
Memcache and delete or update data when it changes. This strategy
can get messy very quickly -- Memcache code becomes riddled
throughout an application. Rails’
[Sweepers](http://guides.rubyonrails.org/caching_with_rails.html#sweepers)
can help with this problem, but other languages and frameworks don’t
have similar alternatives.

One simple strategy to avoid code complexity is to write data to
Memcache with an expiration. Data with an expiration will
automatically expire when the expiration is reached. Most
applications can benefit from time-based cache expiration with
infrequently changing content such as static assets, headers, footers,
blog posts, etc.

In the sandbox shell, run the following commands to set a value that
will expire after 10 seconds.

>callout
>Setting the expiration to “0” means the value will never expire.

```ruby
irb> cache.set("expires", "bar", ttl=10.seconds)
irb> cache.get("expires")
=> "bar"
.. wait 10 seconds ..
irb> cache.get("expires")
=> nil
```

You can see that no action is required to explicitly expire the given
content. After the `ttl` value has passed any `get`s for the key
simply return a nil result.

>warning
>When the expiration time specified is 30 days or more in seconds,
>Memcache treats the expiration as an absolute date by converting the
>amount of seconds specified to a Unix epoch date. Be careful, because
>specifying 40 days in seconds will set the expiration to a time in
>1970, which will yield unknown results.

## Cache clearing

Developers often change their caching strategies several times as they
write new cache code. Rapidly changing cache strategies create a
dirty cache and make debugging difficult. Whenever a cache strategy
is changed in development, a `flush` command should be issued to
Memcache to clear the cache of all values.

In the sandbox console, run the following commands to experiment with
flush:

```ruby
irb> cache.set("foo", "bar")
irb> cache.get("foo")
=> "bar"
irb> cache.flush
irb> cache.get("foo")
=> nil
```

`flush` can also be used when deploying to production. But be careful
-- the application may not be able to withstand a cache flush. Apps
with large caches and heavy traffic are advised to not issue a `flush`
in production or to do so only when traffic is low enough to be
handled without caching.

>note
>The MemCachier Heroku add-on has a web dashboard that can issue a
>flush command for you. Access the MemCachier dashboard by clicking on
>the add-on from your Heroku dashboard or by running `heroku
>addons:open memcachier` from the CLI.

## Lightweight counters

A lightweight counter stored in Memcache can be useful for tracking
how often a certain event happens in your app without degrading your
app’s performance. Counters can be used for debugging, profiling, and
usage tracking.

For example, an app that depends on a 3rd party API may want to know
how often the 3rd party API is unavailable or returns bad data. A
Memcache counter is an ideal solution because page load time will
hardly be impacted and the database won’t see additional load.

In the sandbox console, run the following commands to experiment with
`incr` (increment) and `decr` (decrement):

```ruby
irb> cache.incr("my_counter", 1, nil, 0)
irb> cache.get("my_counter")
=> "0"
irb> cache.incr("my_counter")
irb> cache.get("my_counter")
=> "1"
irb> cache.incr("my_counter", amt=5)
irb> cache.get("my_counter")
=> "6"
irb> cache.decr("my_counter")
irb> cache.get("my_counter")
=> "5"
```

`incr` and `decr` should be used in favor of manual changes with `get`
and `set` because `incr` and `decr` are thread safe and will require
fewer TCP round trips. For an explaination of `incr`'s arguments, see the Dalli
[documentation](http://rubydoc.info/gems/dalli/2.6.4/Dalli/Client:incr).

## List management

A simple list stored in Memcache can be useful for maintaining
denormalized relationships. For example, an e-commerce website may
want to store a small table of recent purchases. Rather than keeping
a serialized list in Memcache and recalculating it when a new purchase
is made, `append` and `prepend` can be used to store denormalized
data, avoiding a database query.

Instead of using a traditional `set` operation to update a customer’s
list of recent purchases:

```ruby
cache.set("user_1_recent_purchases", Purchases.recent)
```

`prepend` can be used with only the new data to the same effect:

```ruby
cache.prepend("user_1_recent_purchases", product.name + "||")
```

This approach creates a smaller Memcache footprint and avoids a
database query to get all the user’s recent purchases.

In the sandbox console, run the following commands to experiment with
`append` and `prepend`:

>callout
>`ttl=0` means the key won't expire and `:raw => true` specifies the
>value is stored as raw bytes, which is required to use `append` and
>`prepend`.

```ruby
irb> cache.set("my_list", "foo", ttl=0, options={:raw => true})
irb> cache.get("my_list")
=> "foo"
irb> cache.prepend("my_list", "bar||")
irb> cache.get("my_list")
=> "bar||foo"
irb> cache.append("my_list", "||baz")
irb> cache.get("my_list")
=> "bar||foo||baz"
```

>note
>This example uses an arbitrary delimiter (`||`). A delimiter should
>be chosen based on the expected value of each item in the list such
>that the list items will never contain the delimiter string.
>Additionally, a fix-lengthed string implementation may be better for
>certain applications.

`append` and `prepend` should be used in favor of manual changes with
`get` and `set` because `append` and `prepend` are thread safe.

>warning
>Memcache only supports a max value size of 1 MB. Be careful creating
>lists that may grow larger in size than the maximum allowed value
>size. Some clients, including Dalli, support compression. In Dalli,
>set the `:compress` option to `true` when connecting to Dalli.

## Thread safe set

A simple JSON hash stored in Memcache can be useful for maintaining
configuration that is accessed frequently. For example, a website may
want to track which features are currently turned on, or which AB
tests are running. Often these configurations are conveniently stored
together in a JSON hash.

`append` and `prepend` aren’t relevant for a JSON hash, because hashes
are unordered. And `set` is dangerous because two concurrent changes
to the JSON hash may cause one change to be lost.

Compare and swap, with the `cas` operator, compares the original value
with the new value and swaps the values _only if the old value hasn’t
been changed by another writer_. In other words, `cas` is a
thread-safe `set`.

In the sandbox console, run the following commands to experiment with
`cas`:

>callout
>`cache.cas` in this example expects a block, which is required by
>Dalli, the chosen Ruby Memcache client. Other clients may not share
>this approach.

```ruby
irb> cache.set("my_json", "{}")
irb> cache.get("my_json")
=> "{}"
irb> cache.cas("my_json") { {key: "val"}.to_json }
irb> cache.get("my_json")
=> "{\"key\":\"val\"}"
```

>note
>The Memcache protocol doesn't directly implement a `cas` operation.
>Instead, it supports `set` with a version number, where the `set` only
>takes place if the version number matches the version of the key
>stored Memcache. Using versions as opposed to implementing `cas`
>directly in the protocol addresses the classic [ABA
>problem](http://en.wikipedia.org/wiki/ABA_problem).
>
>Some clients may require `cas` to be implemented manually by passing a version to `set`.

## Reference

Each Memcache operation discussed here is listed for quick reference
below. The API isn’t documented in detail because each client and
language will have a different API.

<table>
  <tr>
    <th>Operation</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Set with expiration</td>
    <td style="text-align: left">Sets a key and value along with an expiration in seconds. Once the key has expired it will be removed from the cache. An expiration of up to 30 days is interpreted as time interval from the current time, whereas an expiration of 30 days or more is interpreted as an absolute Unix date.</td>
  </tr>
  <tr>
    <td>Flush</td>
    <td style="text-align: left">Removes all data from the cache. Be careful using this command in production -- production apps may experience downtime if an empty cache puts too much stress on the database.</td>
  </tr>
  <tr>
    <td>Increment</td>
    <td style="text-align: left">Increments an integer value by a specified amount. Thread safe.</td>
  </tr>
  <tr>
    <td>Decrement</td>
    <td style="text-align: left">Decrements an integer value by a specified amount. Thread safe.</td>
  </tr>
  <tr>
    <td>Append</td>
    <td style="text-align: left">Appends to the end of a value. The original value must be stored as raw bytes in certain clients. Thread safe.</td>
  </tr>
  <tr>
    <td>Prepend</td>
    <td style="text-align: left">Prepends to the start of a value. The original value must be stored as raw bytes in certain clients. Thread safe.</td>
  </tr>
  <tr>
    <td>CAS (or set with a version)</td>
    <td style="text-align: left">Sets a new value as long as the value hasn’t been changed by another process. Thread safe.</td>
  </tr>
</table>
