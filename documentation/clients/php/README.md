# Examples

| Name | Library | Framework | Deploy |
| ---  | ---     | ---       | ---    |
| [Prime numbers](https://github.com/memcachier/examples-php) | `php-memcached` for `php-5.3` |  | [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-php) |

# PHP clients

| Library | Supported / Documented | Binary / SASL | Version | Activity | Stars |
| ---     | ---                    | ---           | ---     | ---      | ---   |
| [php-memcached](https://github.com/php-memcached-dev/php-memcached)<sup>1</sup> | yes / yes\* | yes / yes |  ![release](https://img.shields.io/github/release/php-memcached-dev/php-memcached.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/php-memcached-dev/php-memcached/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/php-memcached-dev/php-memcached.svg?style=social&maxAge=3600) |
| [php-memcache-sasl](https://github.com/memcachier/PHPMemcacheSASL) | yes / yes | yes / yes | ![release](https://img.shields.io/packagist/v/memcachier/php-memcache-sasl.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/memcachier/PHPMemcacheSASL/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/memcachier/PHPMemcacheSASL.svg?style=social&maxAge=3600) |
| [memcached.php](https://github.com/clickalicious/memcached-php) | ? / no | no / no | ![release](https://img.shields.io/packagist/v/clickalicious/memcached.php.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/clickalicious/memcached-php/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/clickalicious/memcached-php.svg?style=social&maxAge=3600) |
| [php-memcache](https://github.com/tricky/php-memcache) | no / no | yes / yes |   ![release](https://img.shields.io/github/release/tricky/php-memcache.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/tricky/php-memcache/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/tricky/php-memcache.svg?style=social&maxAge=3600) |

\* Recommended.  
<sup>1</sup> Requires `libmemcached`.  

# Wordpress

| Integration | Client | Supported / Documented | Version | Activity | Stars |
| ---                   | ---    | ---                    | ---     | ---      | ---   |
| [wordpress-cache](https://github.com/memcachier/wordpress-cache) | php-memcached | yes / no*<sup>2</sup> | ![release](https://img.shields.io/github/release/memcachier/wordpress-cache.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/memcachier/wordpress-cache/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/memcachier/wordpress-cache.svg?style=social&maxAge=3600) |
| [memcachier](https://github.com/hubertnguyen/memcachier) | php-memcache | yes / no<sup>2</sup> | ![release](https://img.shields.io/github/release/hubertnguyen/memcachier.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/hubertnguyen/memcachier/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/hubertnguyen/memcachier.svg?style=social&maxAge=3600) |

\* Recommended.  
<sup>2</sup> Documented in GitHub README.  

## Plugins

On Wordpress.org there are plugins we should check out. [Clinical MemCachier](https://wordpress.org/plugins/clinical-memcachier/) is made
specifically for us. Based on the description it seems it is based on
`memcachier/wordpress-cache` but based on the code it seems to be based on
`hubertnguyen/memcachier`. Another plugin we should check for compatability is
[Memcached Redux](https://wordpress.org/plugins/memcached-redux/). It is more
popular, based on `php-memcached`, and apparently still
[maintained](https://github.com/Ipstenu/memcached-redux).


# Web frameworks

We document Laravel, Symfony, and CakePHP but maybe should add documentation for others such as CodeIgniter, Yii 2, Slim, and Phalcon. See popularity
[here](http://www.timqian.com/star-history/#laravel/laravel&bcit-ci/CodeIgniter&symfony/symfony&zendframework/zendframework&phalcon/cphalcon&cakephp/cakephp&yiisoft/yii2&slimphp/Slim&fuel/fuel&bcosca/fatfree).

## Laravel

| Integration | Client | Supported / Documented | Version | Activity | Stars |
| ---         | ---    | ---                    | ---     | ---      | ---   |
| [native](https://github.com/laravel/laravel)<sup>3</sup> | php-memcached | yes / no* | ![release](https://img.shields.io/packagist/v/laravel/laravel.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/laravel/laravel/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/laravel/laravel.svg?style=social&maxAge=3600) |
| [laravel-memcached-plus](https://github.com/b3it/laravel-memcached-plus)<sup>4</sup> | php-memcached | yes / no* | ![release](https://img.shields.io/packagist/v/b3it/laravel-memcached-plus.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/b3it/laravel-memcached-plus/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/b3it/laravel-memcached-plus.svg?style=social&maxAge=3600) |
| [laravel-memcache](https://github.com/swiggles/laravel-memcache) | php-memcache | ? / no | ![release](https://img.shields.io/packagist/v/swiggles/memcache.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/swiggles/laravel-memcache/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/swiggles/laravel-memcache.svg?style=social&maxAge=3600) |

\* Recommended.  
<sup>3</sup> Since Laravel 5.3.  
<sup>4</sup> Obsolete as of Laravel 5.3.  

## Symfony

| Integration | Client | Supported / Documented | Version | Activity | Stars |
| ---         | ---    | ---                    | ---     | ---      | ---   |
| [native](https://github.com/symfony/symfony) | php-memcached | yes / yes* | ![release](https://img.shields.io/packagist/v/symfony/symfony.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/symfony/symfony/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/symfony/symfony.svg?style=social&maxAge=3600) |

\* Recommended.  

## CakePHP

| Integration | Client | Supported / Documented | Version | Activity | Stars |
| ---         | ---    | ---                    | ---     | ---      | ---   |
| [native](https://github.com/cakephp/cakephp) | php-memcached | yes / outdated* | ![release](https://img.shields.io/packagist/v/cakephp/cakephp.svg?maxAge=3600) | ![commit](https://img.shields.io/github/last-commit/cakephp/cakephp/master.svg?maxAge=3600) | ![stars](https://img.shields.io/github/stars/cakephp/cakephp.svg?style=social&maxAge=3600) |

\* Recommended.  
