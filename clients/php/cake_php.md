
## CakePHP

The CakePHP framework has excellent support for caching and can be easily used
with MemCachier as the provider. To setup CakePHP with MemCachier, you'll need
to edit the file `app/Config/bootstrap.php` and add the following lines:

```php
Cache::config('default', array(
    'engine' => 'Memcached',
    'prefix' => 'mc_',
    'duration' => '+7 days',
    'servers' => explode(',', <MEMCACHIER_SERVERS>),
    'compress' => false,
    'persistent' => 'memcachier',
    'login' => <MEMCACHIER_USERNAME>,
    'password' => <MEMCACHIER_PASSWORD>,
    'serialize' => 'php'
));
```

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
