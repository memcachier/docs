---
title: "Documentation: Encrypted Connections (TLS)"
description: "Documentation for using MemCachier and encrypted connections with TLS"
---

## Encrypted Connections (TLS)

**IF(direct)**
<p class="alert alert-info">
We generally don't recommend using TLS to secure your connection. Why?
Memcache is normally only used when performance is important and so
low latency is critical. This means we expect your MemCachier cache
and your application that accesses it runs in the same datacenter, for
example the Amazon EC2 <code>us-east-1</code> datacenter. All your traffic are
running over, and only over, the internal datacenter network. This is
a <strong>highly secure</strong> network that can't be sniffed on or
tampered with. For example, your web application is probably speaking
HTTPS, but the HTTPS connection is very likely terminated at a load
balancer, and then unsecured HTTP used to talk between the load
balancer and your application.
</p>
**ENDIF**

**IF(heroku)**
>note
>We generally don't recommend using TLS to secure your connection. Why?
>Memcache is normally only used when performance is important and so
>low latency is critical. This means we expect your MemCachier cache
>and your application that accesses it runs in the same datacenter, for
>example the Amazon EC2 `us-east-1` datacenter. All your traffic are
>running over, and only over, the internal datacenter network. This is
>a <strong>highly secure</strong> network that can't be sniffed on or
>tampered with. For example, your web application is probably speaking
>HTTPS, but the HTTPS connection is very likely terminated at a load
>balancer, and then unsecured HTTP used to talk between the load
>balancer and your application.
**ENDIF**

It is possible to connect to MemCachier using TLS encrypted sockets.
While no existing clients support TLS connections natively, we provide
a [buildpack](https://github.com/memcachier/memcachier-tls-buildpack)
for Heroku customers that proxies the connection to MemCachier and
wraps it in a TLS connection. This can be useful for the extra
paranoid among us, or to securely access your cache from outside the
datacenter.

The buildpack installs and sets up
[stunnel](https://www.stunnel.org/index.html) on localhost listening
on port 11211. It configures stunnel to connect to the MemCachier
servers specified in your environment variable and to verify
certificates as signed by the [MemCachier Root
CA](https://www.memcachier.com/MemCachierRootCA.pem).

Use the buildpack in conjunction with another buildpack that actually
runs your app, using Heroku's [multiple
buildpack](https://devcenter.heroku.com/articles/using-multiple-buildpacks-for-an-app)
feature:

```term
$ heroku buildpacks:add https://github.com/memcachier/memcachier-tls-buildpack.git
```

Finally, configure your app to connect to `localhost:11211` instead of
using the `MEMCACHIER_SERVERS` environment variable, but, **leave your
`MEMCACHIER_SERVERS` environment variable unchanged as the TLS
buildpack uses it to connect to MemCachier**.
