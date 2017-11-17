
## MemCachier analytics

Our analytics dashboard is a simple tool that gives you more insight into how
you’re using memcache. Here's a screenshot of the dashboard:

<p style="text-align:center;">
<img style="width:80%;" src="/images/analytics.png" alt="Analytics dashboard">
</p>

To access your application's analytics dashboard login to your
[account](https://www.memcachier.com/caches) and view one of your caches.

The analytics displayed are:

  - *Limit* -- Your current cache size and memory limit. Once usage comes
    close to this amount you will start seeing evictions.
  - *Live Connections* -- Number of connections currently open to your
    cache.
  - *Total connections* -- Number of connections ever made to your cache.
    (So always larger than live connections).
  - *Items* -- Number of items currently stored in your cache.
  - *Evictions* -- Number of items ever evicted from your cache due to
    memory pressure. Items are evicted in an LRU order.
  - *New Evictions* -- Number of evictions that have occured since the
    last time we sampled your cache.
  - *Hit Rate* -- The ratio of `get` commands that return an item (hit)
    vs. the number that return nothing (miss). This ratio is for the
    period between now and when we last sampled your cache.
  - *Set Cmds* -- Number of times you have ever performed a set command.
  - *Flush Cmds* -- Number of times you have ever performned a flush
    command.

With the basic analytics dashboard we sample your cache once per hour.
With the advance dashboard we sample it once every 30 minutes.

### Advanced analytics

We offer higher paying customers an advance version of our analytics
dashboard. Currently, this offers two primary advantages:

  - *Higher Sample Rate* -- We sample the cache for collecting analytics
    once every thirty minutes, twice the rate of the basic analytics
    dashboard. We don't sample more often than that as a higher
    granularity hasn't proven to be useful, it leads to more noise and
    less signal.
  - *More Graphs* -- We offer two additional graphs for the advanced
    analytics dashboard.
      - *Eviction Graph* -- Your new evictions tracked over time.
      - *Connection Graph* -- Your new connecions tracked over time.

Please note that our graph only allows two data sources to be selected at a
time. So if two are already selected, say "Usage" and "Hit Rate", to select a
different data source, say "Evictions", you'll need to deselect an existing
data source first before selecting the new one to display.
