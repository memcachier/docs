**IF(direct)**
<a href="https://github.com/memcachier/docs"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://github-camo.global.ssl.fastly.net/e7bbb0521b397edbd5fe43e7f760759336b5e05f/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f677265656e5f3030373230302e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_green_007200.png"></a>

# Getting Started with MemCachier

MemCachier is an implementation of the
[Memcache](http://memcached.org) in-memory key/value store used for
caching data. Memcache a key technology in modern web applications for
scaling and reducing server loads. MemCachier manages and
scales clusters of memcache servers so you can focus on your app. Tell
us how much memory you need and get started for free instantly. Add
capacity later as you need it.

Below is our user guide for using MemCachier, you can also find answers
in our <a href="/faq">FAQ</a>.

## Table of Contents

1. [Supported Protocols: ASCII & Binary](#supported-protocols-ascii-binary)
2. [Ruby](#ruby)
3. [Rails 3+ (includes Rails 4 & 5)](#rails-3-4)
4. [Rails 2](#rails-2)
5. [Ruby Puma Webserver](#ruby-puma-webserver)
6. [Rack::Cache](#rails-rack-cache)
7. [Python](#python)
8. [Django](#django)
9. [PHP](#php)
10. [WordPress](#wordpress)
11. [CakePHP](#cakephp)
12. [Symfony2](#symfony2)
13. [Laravel](#laravel)
14. [Node.js](#node-js)
15. [Java](#java)
16. [Supported client libraries](#client-library-support)
17. [Example applications](#sample-applications)
18. [Local usage](#local-usage)
19. [MemCachier analytics](#memcachier-analytics)
20. [Advanced analytics](#advanced-analytics)
21. [Analytics API](#analytics-api)
22. [New Relic integration](#new-relic-integration)
23. [Credentials](#credentials)
24. [Disabled caches](#disabled-caches)
25. [Encrypted Connections (TLS)](#encrypted-connections-tls)
26. [Changing plans](#upgrading-and-downgrading)
27. [Usage Documentation](#using-memcachier)
28. [Key-Value size limit](#key-value-size-limit-1mb)
29. [Errors connecting to localhost](#errors-about-app-trying-to-connect-to-localhost)
30. [Getting support](#support)
**ENDIF**

**IF(heroku)**
[MemCachier](http://www.memcachier.com) is an implementation of the
[Memcache](http://memcached.org) in-memory key/value store used for
caching data. It is a key technology in modern web applications for
scaling and reducing server loads. The MemCachier add-on manages and
scales clusters of memcache servers so you can focus on your app. Tell
us how much memory you need and get started for free instantly. Add
capacity later as you need it.

Follow our [blog](http://blog.memcachier.com) or twitter
([@memcachier](http://twitter.com/MemCachier)), for status and product
announcements.

## Getting started

Start by installing the add-on:

```term
$ heroku addons:create memcachier:dev
```

You can start with more memory if you know you’ll need it:

```term
$ heroku addons:create memcachier:100
$ heroku addons:create memcachier:500
 ... etc ...
```

Once the add-on has been added you’ll notice three new variables in
`heroku config`:

```term
$ heroku config
...
MEMCACHIER_SERVERS    => mcX.ec2.memcachier.com
MEMCACHIER_USERNAME   => bobslob
MEMCACHIER_PASSWORD   => l0nGr4ndoMstr1Ngo5strang3CHaR4cteRS
...
```

Next, setup your app to start using the cache. We have documentation
for the following languages and frameworks:

* [Ruby](#ruby)
* [Rails 3+ (includes Rails 4 & 5)](#rails-3-4)
* [Rails 2](#rails-2)
* [Ruby Puma Webserver](#ruby-puma-webserver)
* [Rack::Cache](#rails-rack-cache)
* [Python](#python)
* [Django](#django)
* [PHP](#php)
* [WordPress](#wordpress)
* [CakePHP](#cakephp)
* [Symfony2](#symfony2)
* [Laravel](#laravel)
* [Node.js](#node-js)
* [Java](#java)

>note
>Your credentials may take up to three (3) minutes to
>be synced to our servers. You may see authentication errors if you
>start using the cache immediately.

**ENDIF**
