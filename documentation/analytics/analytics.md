**IF(direct)**
---
title: "Documentation: MemCachier Analytics"
description: "Our analytics dashboard provides an advanced set of tools that gives you powerful insight into how
you’re using memcache."
---
**ENDIF**

## MemCachier Analytics

MemCachier analytics surfaces the most important metrics for you, so you can understand your cache's performance at a glance.

The analytics dashboard enables developers to measure performance and troubleshoot issues for Memcached. Make sure your caching strategy is working as planned with unique insight into its performance.

**IF(direct)**
<img class="dashboard-img" src="/images/memcached-analytics-dashboard-1440x658.png" alt="Memcached analytics dashboard" loading="lazy" width="1440" height="658">

To access your cache's analytics dashboard login to your
[account](https://www.memcachier.com/caches) and view one of your caches.
**ENDIF**

**IF(heroku)**
![Analytics Dashboard](https://www.memcachier.com/images/memcached-analytics-dashboard-1440x658.png)

To access your application's analytics dashboard run:

```term
$ heroku addons:open memcachier
```
**ENDIF**

MemCachier analytics are powered by CacheSight. See the [CacheSight documentation](https://www.cachesight.com/docs/the-cache-dashboard) for a detailed explanation of all of our analytics dashboard features.

All dashboard features are also available via our 
**IF(direct)**
[API](/documentation/analytics-api)
**ENDIF**
**IF(heroku)**
[API](#analytics-api-v2)
**ENDIF**
