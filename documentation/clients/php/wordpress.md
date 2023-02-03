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

We support WordPress through two different options. The first you can find
[here](https://github.com/memcachier/wordpress-cache), and uses the binary
memcache protocol and is supported by us. It should be easy to install, simply
follow the instructions on the Git repo.

We also have a community support alternative approach that uses the ASCII
memcache protocol, which is far easier to get running on your own servers if
you aren't using a hosted platform like Heroku. You can find it on GitHub
[here](https://github.com/hubertnguyen/memcachier). Please follow the
instructions on the repo page.
