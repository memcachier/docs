**IF(direct)**
---
title: "Documentation: Getting Started with MemCachier"
description: "MemCachier is an implementation of the Memcached in-memory key/value store used for caching data."
---

**IF(direct)**
# Getting Started with MemCachier

MemCachier is an implementation of the
[Memcache](https://memcached.org) in-memory key/value store used for
caching data. Memcache a key technology in modern web applications for
scaling and reducing server loads. MemCachier manages and
scales clusters of memcache servers so you can focus on your app. Tell
us how much memory you need and get started for free instantly. Add
capacity later as you need it.

Browse through our user guide to find best practices for setting up and using
MemCachier. If you find you still have unanswered questions,
<a href="/contact">we're happy to answer them</a>.
**ENDIF**

**IF(heroku)**
[MemCachier](https://www.memcachier.com) is an implementation of the
[Memcache](https://memcached.org) in-memory key/value store used for
caching data. It is a key technology in modern web applications for
scaling and reducing server loads. The MemCachier add-on manages and
scales clusters of memcache servers so you can focus on your app. Tell
us how much memory you need and get started for free instantly. Add
capacity later as you need it.

Follow our [blog](https://blog.memcachier.com) or twitter
([@memcachier](https://twitter.com/MemCachier)), for status and product
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
* [Rails](#rails)
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
