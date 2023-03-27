**IF(direct)**
---
title: "Documentation: WordPress"
description: "Documentation for using MemCachier with WordPress"
---
**ENDIF**

## WordPress

**IF(direct)**
<div class="alert alert-info">
Related tutorials:
<ul>
  <li><a href="https://blog.memcachier.com/2019/10/14/wordpress-on-digital-ocean/">Build a WordPress One-Click application on DigitalOcean and scale it with Memcache</a></li>
</ul>
</div>
**ENDIF**

### Using MemCachier with the W3 Total Cache WordPress plugin

The [W3 Total Cache](https://wordpress.org/plugins/w3-total-cache/) WordPress plugin supports Memcached as a caching method. MemCachier is protocol-compliant with Memcached (and has several [advantages over Memcached](https://www.memcachier.com/why-memcachier#memcachier-vs-memcached)) so W3 Total Cache can be configured to use MemCachier to speed up your WordPress site.

Configuring W3 Total Cache to use MemCachier involves two steps:

1. Install the [Memcached PHP extension](https://www.php.net/manual/en/book.memcached.php)
2. Update the appropriate W3 Total Cache settings from WordPress Admin.

#### Install the Memcached PHP extension

First, check to see if the Memcached PHP extension is installed.

From the WordPress Admin left-hand menu, click **Performance**, then **Dashboard**. Then, from the W3 Total Cache dashboard, click **compatibility check**.

**IF(direct)**
<img class="dashboard-img" src="/images/w3-total-cache-memcached-compatibility-check.jpg" alt="W3 Total Cache screenshot showing the 'compatibility check' button" loading="lazy" width="1440" height="496">
**ENDIF**
**IF(heroku)**
![Total Cache screenshot showing the 'compatibility check' button](https://www.memcachier.com/images/w3-total-cache-memcached-compatibility-check.jpg)
**ENDIF**

This will run a compatibility check for the various server modules and resources W3 Total Cache can make use of.

**IF(direct)**
<img class="dashboard-img" src="/images/w3-total-cache-memcached-compatibility-check-results.jpg" alt="W3 Total Cache screenshot showing the compatibility check results" loading="lazy" width="1440" height="1144">
**ENDIF**
**IF(heroku)**
![W3 Total Cache screenshot showing the compatibility check results](https://www.memcachier.com/images/w3-total-cache-memcached-compatibility-check-results.jpg)
**ENDIF**

Notice, the Memcached PHP extension is shown as **Not available**, meaning it is not installed.

Next, install the Memcached PHP extension (not the Memcache extension). Make sure to install a version compatible with your installed version of PHP. Refer to the Compatibility Check results to see your PHP version. In the screenshot `8.0.28` is shown.

**Note**, the Memcached PHP extension is used because it supports SASL authentication, which is required to connect to your MemCachier cache using its username and password. The Memcache PHP extension, on the other hand, does not support SASL authentication.

To install the Memcached PHP extension on Ubuntu, run the following command:

```bash
sudo apt-get install -y php8.0-memcached
```

Restart your web server.

Once that is complete, refresh your WordPress Admin browser window and click **Compability Check** again. The Memcached extension should now show as **Installed**.

W3 Total Cache can now use Memcached as a caching method.

#### Update the W3 Total Settings to use Memcached

Next, update the appropriate W3 Total Cache settings from WordPress Admin to use your MemCachier cache as its Memcached caching method.

Memcached can be used as a caching method for the following W3 Total Cache features:

- Page Cache
- Minify
- Database Cache
- Object Cache
- Fragment Cache

Configuring each one involves the same two steps:

1. Enable the feature, selecting **Memcached** as the caching method.
2. Configure the feature to use your MemCachier cache.

In the following section, you'll configure the Object Cache. As mentioned, other Memcached-supported features require a very similar configuration process, so these following instructions should enable you to configure any of the other features.

#### Configuring the W3 Total Cache Object Cache

To enable the Object Cache, from the WordPress Admin left-hand menu, click **Performance**, then **General Settings**. Then, scroll down to the **Object Cache** settings.

Check the **Enable** checkbox to enable the object cache. Then, select **Memcached** and save settings.

Provided you con't have a local Memcached server running, you'll see the following warning:

> The following memcached servers are not responding or not running:
> Object Cache: 127.0.0.1:11211.
> This message will automatically disappear once the issue is resolved.

This is because W3 Total Cache is configured by default to look for a Memcached server running on host `127.0.0.1` and port `11211`.

Next, to configure your cache, click **Performance**, then **Object Cache**.

Under **Advanced**, enter your MemCachier cache's server(s) in **Memcached hostname:port / IP:port**.

Then, enter your MemCachier cache's username and password in **Memcached username** and **Memcached password** respectively.

Make sure **Binary protocol** is checked.

Finally, save the settings.

**IF(direct)**
<img class="dashboard-img" src="/images/w3-total-cache-object-cache-settings.jpg" alt="W3 Total Cache screenshot showing object cache settings" loading="lazy" width="1440" height="1144">
**ENDIF**
**IF(heroku)**
![W3 Total Cache screenshot showing object cache settings](https://www.memcachier.com/images/w3-total-cache-object-cache-settings.jpg)
**ENDIF**

The W3 Total Cache Object Cache is now configured to use MemCachier.

**Note**, because of a known bug with testing Memcached with using SASL authentication, you'll see the following notice after saving settings:

> The following memcached servers are not responding or not running:
> Object Cache: your_server.memcachier.com:11211.
> This message will automatically disappear once the issue is resolved.

Also, due to the same bug, if you click the **Test** button beside **Memcached hostname:port / IP:port**, you'll get an error notification **Test Failed**.

In spite of these, your cache should be working. To verify it is, check your
**IF(direct)**
 [MemCachier Analytics dashboard](/documentation/memcachier-analytics)
**ENDIF**
**IF(heroku)**
 [MemCachier Analytics dashboard](#memcachier-analytics)
 **ENDIF**
 and notice the stats change as requests are made to your WordPress website.

The bug was reported here: <https://wordpress.org/support/topic/memcached-tests-when-use-sasl/>

And has a corresponding open GitHub issue: <https://github.com/BoldGrid/w3-total-cache/issues/448>

### WP Object Cache

Another way to use MemCachier with WordPress is with [our WordPress Object Cache backend](https://github.com/memcachier/wordpress-cache). It integrates the MemCachier caching service with [WP Object Cache](https://developer.wordpress.org/reference/classes/wp_object_cache/).

**Note**, the W3 Total Cache plugin features object caching, so there is no need to use this technique if you are using that plugin. In fact, it would likely be problematic to do so.

If you still want to use WP Object Cache instead of W3 Total Cache, see our tutorial [Build a WordPress One-Click application on DigitalOcean and scale it with Memcache](https://blog.memcachier.com/2019/10/14/wordpress-on-digital-ocean/). The tutorial uses DigitalOcean as hosting but the WP Object Cache installation part is generally applicable.
