# Why am I seeing evictions before 100% cache usage?

We shard your data over many servers and this can create some
imbalance in how data is distributed. This means that you'll get some
evictions before 100%. Essentially, as you approach 100%, the
probability of an eviction increases until it is guaranteed.

# Does MemCachier use an LRU for evicting items?

We evict items in an LRU fashion, but it is not a strict, single LRU.

Memcached (and MemCachier) divides memory up into buckets, where each bucket manages key-value pairs of similar sizes. I.e., all key-value pairs of size 129 - 256 bytes will be in bucket B1, while key-value pairs of size 257 - 512 bytes will be in different bucket B2.

For various performance reasons, memcached has a separate LRU per bucket. This allows it to guarantee O(1) operations for everything.  This means though that when an item is evicted, the LRU used depends on the size of the new item being stored. If the item being store is 183 bytes, then the LRU and only the LRU for bucket B1 is used. This then isn't strict LRU but a sharded form.

What can sometimes happen though is a data imbalance. Say you start with a new cache and store only items of N bytes up until your limit.  They'll all end up in one bucket Bx. This means bucket Bx will have taken all the memory your cache has. If you try to store another item that is say 2N+1 bytes in size, it'll end up in a different bucket By However, you are out of memory and something needs to be evicted.  Bucket By though has no items yet, so we can't evict anything! In Memcached this situation leads to an error, in MemCachier we allow it to succeed and you'll go slightly above your memory limit. However, any future stores to bucket By will immediately evict the previously stored item. Essentially, bucket By has room for 1 key only.  

The only way to fix this right now sadly is to flush your cache. Once memory has been assigned to a particular bucket, it can never be used by a different bucket. Generally the issue doesn't occur as customers store data across all buckets, the above example is an extreme of what can occur as an imbalance.

If you use MemCachier for say two or more very distinctive use cases (i.e., a session store and a HTML fragment cache), we generally recommend you use two separate caches as it helps avoid the above issue occurring.

# How do you guarantee locality of MemCachier servers with my Heroku Dynos?

Sadly we can't. We make sure that we are in the same Amazon data
centre as your Heroku dynos. So right now for Heroku that is either EU
or US-East.

However, Amazon data centres also have availability zones (AZ), which
are marketed as physically isolated sub-data-centres providing fault
tolerance (separate power, networks... etc). Going from one AZ to
another is more expensive than going between two machines in the same
AZ. Latency in same AZ is pretty stable and around 0.3ms. Latency
across AZ is higher, around 0.5 - 1.5ms and much more variability
(outliers can be 100's of ms).

Heroku spins up your dynos in multiple AZ and chooses them randomly.
So there is no way for us to be in the same AZ as all your dynos.

This is generally fine as cross AZ is fast enough but the outliers in
the network latency do cause some problems as its often the case that
when a customers sees time outs on rare occasions in their logs they
are caused by this fundamental issue and not something we can address.
These occurrences are rare though so overall cause no issue, just
annoying log messages.

# I noticed that one particular Dyno couldn't connect to MemCachier. What is best practices for handling this?

Sadly this seems to be an issue in the underlying Heroku and Amazon
network. Occasionally customers report to us just one certain dyno
not being able to connect.

In general we recommend restarting that particular dyno, although
usually this is done by hand. Since doing this automatically (naively)
would cause your app to not function if MemCachier went down.

Our is that your app ideally should function as well as possible with
MemCachier being 'down'. This applies for all services you are using.
Now, that said it makes sense to have an automated way to detect when
any service is down. It then makes sense to try just restarting the
dyno a few times automatically, but only a few times, not infinitely.

This is similar to how upstart or systemd works if you are familiar
with running services using these Linux frameworks. They have an
ability to restart a service if they detect it has crashed but will
only do so up to some limit (i.e., 5 times) before killing the process
completely.

So in summary, our best practice suggestion is:
* Design your app to function as well as possible with any service
  being down.
* Have an automated way to detect a service being 'down' to any
  particular dyno.
* Have an automated way to restart that dyno but with a limit on how
  many times in a short space of time this can occur.
* When the limit is hit, the dyno should be started again so it can
  run as well as possible without access to the service.
* In this final case, a notification should be sent to a team member
  to be resolved by a human.

Now having all of this would be awesome and make your app quite fault
tolerant and one of the best designed on Heroku! It's also a
reasonable amount of work, so the easiest solution may just be an
automated notification system that brings a human in when needed to
either restart one particular dyno or take other actions.

# Should I increase the size of my plan?

The best way is to generally look at your analytics dashboard and compare your
'Hit Rate' to your 'Usage'.

Basically, if your hit rate is low but your usage is high, then this is often
indicative that you could get better performance from a larger cache.

Secondly, we designed MemCachier to be easy to test different plans with.
Moving between any of the paid plans doesn't loose any of your data. And you
are only charged by the hour, so you can easily try out a much larger plan and
test if it improves performance. If it doesn't, simply downgrade back to your
old plan!

# Rails + multi_get

https://github.com/n8/multi_fetch_fragments

