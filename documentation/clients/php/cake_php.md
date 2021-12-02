**IF(direct)**
---
title: "Documentation: CakePHP"
description: "Documentation for using MemCachier with CakePHP"
---
**ENDIF**

## CakePHP

The CakePHP framework has excellent support for caching and can be easily used
with MemCachier as the provider. To setup CakePHP with MemCachier, you'll need
to edit the file `app/Config/bootstrap.php` and add the following lines:

```php
Cache::config('default', array(
    'engine' => 'Memcached',
    'prefix' => 'mc_',
    'duration' => '+7 days',
    'compress' => false,
    'persistent' => 'memcachier',
    'servers' => explode(',', getenv('MEMCACHIER_SERVERS')),
    'login' => getenv('MEMCACHIER_USERNAME'),
    'password' => getenv('MEMCACHIER_PASSWORD'),
    'serialize' => 'php'
));
```

**IF(direct)**
<p class="alert alert-info">
The values for <code>MEMCACHIER_SERVERS</code>, <code>MEMCACHIER_USERNAME</code>, and
<code>MEMCACHIER_PASSWORD</code> are listed on your
<a href="https://www.memcachier.com/caches">cache overview page</a>. Make sure to add them
to your environment.
</p>
**ENDIF**

After that, you should be able to use caching throughout your application like so:

```php
class Post extends AppModel {

    public function newest() {
        $model = $this;
        return Cache::remember('newest_posts', function() use ($model){
            return $model->find('all', array(
                'order' => 'Post.updated DESC',
                'limit' => 10
            ));
        }, 'longterm');
    }
}
```

The above will fetch the value associated with the key `newest_posts` from the
cache if it exists. Otherwise, it will execute the function and SQL query,
storing the result in the cache using the `newest_posts` key.

You can find much more information on how to use caching with CakePHP
[here](http://book.cakephp.org/2.0/en/core-libraries/caching.html).
