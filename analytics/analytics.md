

<h2 id="analytics">MemCachier analytics</h2>

Our analytics dashboard is a simple tool that gives you more insight into how
you’re using memcache. Here's a screenshot of the dashboard:

<p style="text-align:center;">
<img style="width:80%;" src="/images/analytics.png" alt="Analytics dashboard">
</p>

To access your application's analytics dashboard login to your
[account](https://www.memcachier.com/caches) and view one of your caches.

The analytics displayed are:

* _Limit_ -- Your current cache size and memory limit. Once usage comes
  close to this amount you will start seeing evictions.
* _Live Connections_ -- Number of connections currently open to your
  cache.
* _Total connections_ -- Number of connections ever made to your cache.
  (So always larger than live connections).
* _Items_ -- Number of items currently stored in your cache.
* _Evictions_ -- Number of items ever evicted from your cache due to
  memory pressure. Items are evicted in an LRU order.
* _New Evictions_ -- Number of evictions that have occured since the
  last time we sampled your cache.
* _Hit Rate_ -- The ratio of `get` commands that return an item (hit)
  vs. the number that return nothing (miss). This ratio is for the
  period between now and when we last sampled your cache.
* _Set Cmds_ -- Number of times you have ever performed a set command.
* _Flush Cmds_ -- Number of times you have ever performned a flush
  command.

With the basic analytics dashboard we sample your cache once per hour.
With the advance dashboard we sample it once every 30 minutes.

<h3 id="advanced-analytics">Advanced analytics</h3>

We offer higher paying customers an advance version of our analytics
dashboard. Currently, this offers two primary advantages:

* _Higher Sample Rate_ -- We sample the cache for collecting analytics
  once every thirty minutes, twice the rate of the basic analytics
  dashboard. We don't sample more often than that as a higher
  granularity hasn't proven to be useful, it leads to more noise and
  less signal.
* _More Graphs_ -- We offer two additional graphs for the advanced
  analytics dashboard.
  * _Eviction Graph_ -- Your new evictions tracked over time.
  * _Connection Graph_ -- Your new connecions tracked over time.

Please note that our graph only allows two data sources to be selected at a
time. So if two are already selected, say "Usage" and "Hit Rate", to select a
different data source, say "Evictions", you'll need to deselect an existing
data source first before selecting the new one to display.
