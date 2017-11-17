
## Credentials

In order to connect a memcache client to MemCachier, you use a
username and password listed on the [analytics dashboard](#memcachier-analytics)
for your cache. Each cache can have multiple sets of credentials.
One of these sets of credentials is distinguished as
*primary*, meaning that, for hosted platforms like Heroku,
it is linked to the hosted platform MemCachier addon.

From the *Credentials* panel on the analytics dashboard, it
is possible to create new credentials, delete existing credentials and
promote secondary credentials to primary credentials. This makes it
possible to rotate credentials by creating a new set of secondary
credentials and promoting them to primary. For caches associated with
hosted platforms, promoting a set of secondary credentials to primary
causes the configuration variables on the hosted platform to be
updated. For example, rotating the credentials on a Heroku-associated
cache causes an update of the `MEMCACHIER_USERNAME` and
`MEMCACHIER_PASSWORD` configuration variables on your Heroku app and a
restart of your dynos to pick up the new values.

Each set of credentials for a cache can be given different
*capabilities*, in the sense that sets of credentials can be
restricted to read-only access to the cache, or prevented from
flushing the cache via the memcache API. These capabilities are
controlled by checkboxes on the *Credentials* panel of the analytics
dashboard. (The exact error conditions that a client will receive if
it attempts to perform an action for which it does not have the
capability depends on the details of the client library used. The
most common cases are likely to be for the Dalli Ruby library and the
pylibmc Python library. For both of these client libraries,
attempting to set a cache entry using credentials that do not have the
write capability will simply result in a "value not set" response from
the library.)
