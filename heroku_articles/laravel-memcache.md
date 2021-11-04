
Memcache is a technology that improves the performance and scalability of web
apps and mobile app backends. You should consider
using Memcache when your pages are loading too slowly or your app is
having scalability issues. Even for small sites, Memcache can make page loads
snappy and help future-proof your app.

This guide shows how to create a simple [Laravel 5.6](http://laravel.com/)
application, deploy it to Heroku, then add Memcache to alleviate a performance
bottleneck.

>note
>The sample app in this guide can be seen running
>[here](https://memcachier-examples-laravel.herokuapp.com/). You can [view the source code](http://github.com/memcachier/examples-laravel-heroku) or deploy it with this Heroku Button:
>
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-laravel-heroku)

## Prerequisites
Before you complete the steps in this guide, make sure you have all of the following:

* Familiarity with PHP (and ideally some Laravel)
* A Heroku user account ([signup is free and instant](https://signup.heroku.com/signup/dc))
* Familiarity with the steps in [Getting Started with PHP on Heroku](getting-started-with-php)
* PHP, Composer, and the [Heroku CLI](heroku-cli) installed
on your computer

> callout
> This tutorial is based on the
> [Laravel 5.2 tutorial](https://laravel.com/docs/5.2/quickstart) and the
> [Heroku Laravel guide](https://devcenter.heroku.com/articles/getting-started-with-laravel).
> For more details about the creation and deployment of Laravel applications on
> Heroku, please consult these resources.

## Deploying a Laravel application to Heroku

To start, we create a Laravel skeleton app like so:

```term
$ composer create-project laravel/laravel --prefer-dist laravel_memcache
Installing laravel/laravel (v5.6.0)
  - Installing laravel/laravel (v5.6.0): Loading from cache
Created project in laravel_memcache
...

$ cd laravel_memcache
```

### Heroku-specific setup

Before we can create a working Heroku application, we need to add a few Heroku-specific changes to the skeleton:

1. Create a simple [Procfile](procfile) to let Heroku know how to run your application:

    ```term
    $ echo web: vendor/bin/heroku-php-apache2 public/ > Procfile
    ```

2. Your application needs to trust Heroku proxies. Change
`$proxies` and `$headers` in `app/Http/Middleware/TrustProxies.php` as follows:

    ```php
    // ...

    protected $proxies = '**';

    // ...

    protected $headers = Request::HEADER_X_FORWARDED_AWS_ELB;

    // ...
    ```

    > callout
    > This configuration does not work for Laravel <5.6. See
    > [this Stack Overflow answer](https://stackoverflow.com/questions/48681417/laravel-5-6-trustedproxies-error/48684748#48684748)
    >  for older versions.

3. Before we can create a Heroku application, we need to initialize a Git repository
and commit the work we have done so far:

    ```term
    $ git init
    Initialized empty Git repository in ~/laravel_memcache/.git/
    $ git add .
    $ git commit -m "Laravel skeleton for Heroku"
    [master (root-commit) 3099e3b] Laravel skeleton for Heroku
     84 files changed, 7077 insertions(+)
    ...
    ```

### Create and configure the Heroku app

Now we're ready to create the Heroku application:

```term
$ heroku create
Creating app... done, ⬢ serene-castle-14546
https://serene-castle-14546.herokuapp.com/ | https://git.heroku.com/serene-castle-14546.git
```

Before we can deploy the Laravel skeleton, we need to add some configuration in the form of [config vars](config-vars):

1. Set a Laravel encryption key:

    ```term
    $ heroku config:set APP_KEY=$(php artisan key:generate --show)
    Setting APP_KEY and restarting ⬢ serene-castle-14546... done, v3
    APP_KEY: base64:E8Ay5w611tCLkqLnGSualCypRR+s8PGSfK20M+0HNIU=
    ```

2. Configure the logger to write to `errorlog`:

    ```term
    $ heroku config:set LOG_CHANNEL=errorlog
    ```

    You can optionally configure `errorlog` to be your default log channel in `config/loging.php`:

    ```php
    'driver' => env('LOG_CHANNEL', 'errorlog'),
    ```

Now, deploy the Laravel skeleton to Heroku:

```term
$ git push heroku master
Counting objects: 113, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (95/95), done.
Writing objects: 100% (113/113), 181.42 KiB | 5.85 MiB/s, done.
Total 113 (delta 9), reused 0 (delta 0)
remote: Compressing source files... done.
remote: Building source:
remote:
remote: -----> Fetching custom git buildpack... done
remote: -----> PHP app detected
...
remote: Verifying deploy... done.
To https://git.heroku.com/serene-castle-14546.git
 * [new branch]      master -> master
```

Your Laravel app is now deployed to Heroku. Type `heroku open` to open it in your browser.

## Adding task list functionality

Let's add a task list to the app that enables users to view, add, and
delete tasks. To accomplish this, we need to:

1. Set up the database
2. Create a table to store and manage tasks
3. Create the views and controller logic

### Set up the database

Before we can configure the database in Laravel, we need to create the database. On Heroku, you
can add a free development database to your app like so:

```term
$ heroku addons:create heroku-postgresql:hobby-dev
```

This creates a PostgreSQL database for your app and adds a `DATABASE_URL` config var that contains its URL. To use this database,
configure it like so in `config/database.php`:

```php
<?php

$dbopts = parse_url(env('DATABASE_URL'));

return [

  // ...

  'connections' => [

    // ...

    'pgsql' => [
        'driver' => 'pgsql',
        'host' => $dbopts['host'],
        'port' => $dbopts['port'],
        'database' => ltrim($dbopts["path"],'/'),
        'username' => $dbopts['user'],
        'password' => $dbopts['pass'],
        'charset' => 'utf8',
        'prefix' => '',
        'schema' => 'public',
        'sslmode' => 'prefer',
    ],

    // ...
  ],
  // ...
];
```

To make sure this `pgsql` connection is used when the app is running on Heroku, set the `DB_CONNECTION` config var:

```term
$ heroku config:set DB_CONNECTION=pgsql
```

If you want to test your app locally (optional), we recommend using SQLite. To do so, make sure you have `php-sqlite` installed and configure the SQLite
connection in `config/database.php`:

```php
'sqlite' => [
    'driver' => 'sqlite',
    'database' => database_path('database.sqlite'),
    'prefix' => '',
],
```

To use this connection locally, set `DB_CONNECTION=sqlite` in your app's `.env` file.
Additionally, to make sure artisan does not complain about setting up pgsql from
non-existing parameters, you can also add a dummy database URL to `.env`:
`DATABASE_URL=postgres://u:p@localhost:5432/dummy-db`.

Save the changes so far by committing:

```term
$ git commit -am 'Configure DB connections'
```

### Create the Tasks table

Now that we have an empty database, we can add a table to represent the task list. In Laravel, you do this by creating a migration like so:

```term
$ php artisan make:migration create_tasks_table --create=tasks
```

Tasks should have names, so let's add `name` to the `tasks` table in the newly created `database/migrations/<date>_create_tasks_table.php` file:

```php
Schema::create('tasks', function (Blueprint $table) {
    $table->increments('id');
    $table->string('name');
    $table->timestamps();
});
```

To easily access the `tasks` table from our code, we create a corresponding `Task` model:

```term
$ php artisan make:model Task
```

This creates an empty `Task` model in `app/Task.php`.
Laravel automatically infers its fields from the migration.

If you set up SQLite locally, create the database and run the migrations
(optional):

```term
$ touch database/database.sqlite
$ php artisan migrate --force
```

Finally, commit your changes and run the migrations on Heroku:

```term
$ git add .
$ git commit -m 'Add task model'
$ git push heroku master
$ heroku run php artisan migrate --force
...
Do you really wish to run this command? (yes/no) [no]:
> y
...
```

### Add a view for the task list

To view the tasks stored in the database, we create a view that lists
all tasks. We start with a boilerplate layout:

```php
<!-- resources/views/layouts/app.blade.php -->

<!DOCTYPE html>
<html lang="en">
  <head>
    <title>MemCachier Laravel Tutorial</title>

    <!-- Fonts -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css"
          rel='stylesheet' type='text/css'>

    <!-- CSS  -->
    <link href="{{ elixir('css/app.css') }}" rel="stylesheet">

  </head>

  <body>
    <div class="container">
      <nav class="navbar navbar-default">
        <!-- Navbar Contents -->
      </nav>
    </div>

    @yield('content')

    <!-- JavaScripts -->
    <script src="{{ elixir('js/app.js') }}"></script>
  </body>
</html>

```

We can now create the task list view as a child view of the above layout:

```php
<!-- resources/views/tasks.blade.php -->

@extends('layouts.app')

@section('content')

  <div class="container">

    <!-- TODO: New Task Card -->

    <!-- Current Tasks -->
    @if (count($tasks) > 0)
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Current Tasks</h5>

          <table class="table table-striped">
            @foreach ($tasks as $task)
              <tr>
                <td class="table-text">
                  <div>{{ $task->name }}</div>
                </td>

                <td>
                  <!-- TODO Delete Button -->
                </td>
              </tr>
            @endforeach
          </table>
        </div>
      </div>
    @endif

    <!-- TODO: Memcache Stats Card -->

  </div>
@endsection
```

Ignore the `TODOs` for now (we'll fill them out later). To be able to
access this view, connect it to the top route in `routes/web.php`:

```php
<?php

use App\Task;

// Show Tasks
Route::get('/', function () {
    $tasks = Task::orderBy('created_at', 'asc')->get();

    return view('tasks', [
        'tasks' => $tasks
    ]);
});
```

If you have a local setup, you can now start a web server with
`php artisan serve` and visit the view at `localhost:8000`. However, there isn't much to look at yet because the task list is empty.

### Enable task creation

In order for the task list more useful, users need to be able to add tasks. Let's create a card for that:

```php
<!-- resources/views/tasks.blade.php -->

<!-- ... -->

<!-- New Task Card -->
<div class="card">
  <div class="card-body">
    <h5 class="card-title">New Task</h5>

    <!-- Display Validation Errors -->
    @include('common.errors')

    <!-- New Task Form -->
    <form action="{{ url('task') }}" method="POST">
      {{ csrf_field() }}

      <!-- Task Name -->
      <div class="form-group">
        <input type="text" name="name" id="task-name" class="form-control"
               placeholder="Task Name">
      </div>

      <!-- Add Task Button -->
      <div class="form-group">
        <button type="submit" class="btn btn-default">
          <i class="fa fa-plus"></i> Add Task
        </button>
      </div>
    </form>
  </div>
</div>

<!-- Current Tasks -->

<!-- ... -->
```

Because the task name is provided by the user, we need to make sure the input is valid. In this case, the name must exist, and it must not exceed 255 characters. If the input fails to validate according to these rules, we want to display the following error view:

```php
<!-- resources/views/common/errors.blade.php -->

@if (count($errors) > 0)
  <div class="alert alert-danger">
    <strong>Whoops! Something went wrong!</strong>
    <br><br>
    <ul>
      @foreach ($errors->all() as $error)
        <li>{{ $error }}</li>
      @endforeach
    </ul>
  </div>
@endif
```

Let's add these new views to `routes/web.php`:

```php
// ...

use Illuminate\Http\Request;

// Show Tasks
// ...

// Add New Task
Route::post('/task', function (Request $request) {
    // Validate input
    $validator = Validator::make($request->all(), [
        'name' => 'required|max:255',
    ]);

    if ($validator->fails()) {
        return redirect('/')
            ->withInput()
            ->withErrors($validator);
    }

    // Create task
    $task = new Task;
    $task->name = $request->name;
    $task->save();

    return redirect('/');
});
```

Starting a local web server with `php artisan serve` and visiting
`localhost:8000` is now a bit more interesting because you can add tasks.

### Enable task deletion

To complete our task list, we also need to be able to remove completed tasks. To delete a task, we add a Delete button to each item in the task list:

```php
<!-- resources/views/tasks.blade.php -->

<!-- ... -->

<!-- Delete Button -->
<form action="{{ url('task/'.$task->id) }}" method="POST">
  {{ csrf_field() }}
  {{ method_field('DELETE') }}

  <button type="submit" class="btn btn-danger">
    <i class="fa fa-trash"></i> Delete
  </button>
</form>

<!-- ... -->
```

Then we wire this functionality to the appropriate route in `routes/web.php`:

```php
// ...

// Show Tasks & Add New Task
// ...

// Delete Task
Route::delete('/task/{task}', function (Task $task) {
  $task->delete();

  return redirect('/');
});
```

Now we can push the changes to Heroku and see the result:

```term
$ git add .
$ git commit -m 'Add task view'
$ git push heroku master
$ heroku open
```

We now have a functioning task list running on Heroku. With this complete, we
can learn how to improve its performance with Memcache.

## Adding caching to Laravel

Memcache is an in-memory, distributed cache. Its primary API consists of two
operations: `SET(key, value)` and `GET(key)`.
Memcache is like a hashmap (or dictionary) that is spread across
multiple servers, where operations are still performed in constant
time.

The most common use for Memcache is to cache expensive database
queries and HTML renders so that these expensive operations don’t
need to happen over and over again.

### Set up Memcache

To use Memcache in Laravel, you first need to provision an actual Memcache
cache. You can easily get one for free with the
[MemCachier add-on](https://elements.heroku.com/addons/memcachier):

```term
$ heroku addons:create memcachier:dev
```

To use use Memcache on your local machine, you also need to complete the
following steps:

1. Install the `php-memcached` PECL extension via your OS package manager.
2. Uncomment `;extension=memcached.so` in `/etc/php/conf.d/memcached.ini`.
3. Run `php -m` to make sure the `memcached` module is loaded.

(On Heroku, this dependency is already installed and configured.)

To set up Memcache in Laravel, we add the following dependency to
`composer.json`:

```term
$ composer require ext-memcached
```

We then configure the cache in `config/cache.php`:

```php
'memcached' => [
    'driver' => 'memcached',
    'persistent_id' => 'memcached_pool_id',
    'sasl' => [
        env('MEMCACHIER_USERNAME'),
        env('MEMCACHIER_PASSWORD'),
    ],
    'options' => [
        // some nicer default options
        // - nicer TCP options
        Memcached::OPT_TCP_NODELAY => TRUE,
        Memcached::OPT_NO_BLOCK => FALSE,
        // - timeouts
        Memcached::OPT_CONNECT_TIMEOUT => 2000,    // ms
        Memcached::OPT_POLL_TIMEOUT => 2000,       // ms
        Memcached::OPT_RECV_TIMEOUT => 750 * 1000, // us
        Memcached::OPT_SEND_TIMEOUT => 750 * 1000, // us
        // - better failover
        Memcached::OPT_DISTRIBUTION => Memcached::DISTRIBUTION_CONSISTENT,
        Memcached::OPT_LIBKETAMA_COMPATIBLE => TRUE,
        Memcached::OPT_RETRY_TIMEOUT => 2,
        Memcached::OPT_SERVER_FAILURE_LIMIT => 1,
        Memcached::OPT_AUTO_EJECT_HOSTS => TRUE,

    ],
    'servers' => array_map(function($s) {
        $parts = explode(":", $s);
        return [
            'host' => $parts[0],
            'port' => $parts[1],
            'weight' => 100,
        ];
      }, explode(",", env('MEMCACHIER_SERVERS', 'localhost:11211')))
],
```

For Laravel to use Memcache as its cache, you also need to set the
`CACHE_DRIVER` config var:

```term
$ heroku config:set CACHE_DRIVER=memcached
```

### Cache expensive database queries

Memcache is often used to cache the results of expensive database queries. Of course, our simple task list does not have any expensive queries, but let's assume for this tutorial that fetching all of the tasks from the database is a slow operation.

The `rememberForever` function makes it easy to add caching to Laravel. You provide two arguments to it:

* A cache key
* A function that queries your database and returns results

The `rememberForever` function looks up the key in your cache. If the key is present, its corresponding value is returned. Otherwise, the database function you provided is called. Whatever that function returns is then stored in the cache with the corresponding key for future lookups.

This means that the _first_ time you call `rememberForever`, the expensive database function is called, but every successive call to `rememberForever` obtains the value from the cache.

Use the `rememberForever` function to easily add caching to the task view controller in `routes/web.php`:

```php
// Show Tasks
Route::get('/', function () {
  $tasks = Cache::rememberForever('all_tasks', function () {
    return Task::orderBy('created_at', 'asc')->get();
  });

  return view('tasks', [
    'tasks' => $tasks
  ]);
});
```

As you might have noticed, we now have a problem if we add or remove a task.
Because `rememberForever` fetches the task list from the cache, any changes to the database won't be reflected in the task list. For this reason,
whenever we change the tasks in the database, we need to **invalidate** the cache:

```php
// Add New Task
Route::post('/task', function (Request $request) {
    // ...
    $task->save();

    Cache::forget('all_tasks');

    return redirect('/');
});

// Delete Task
Route::delete('/task/{task}', function (Task $task) {
  $task->delete();

  Cache::forget('all_tasks');

  return redirect('/');
});
```

### View Memcache statistics

To help demystify Memcache caching operations, we can visualize what's going on
under the hood.

First, we obtain stats every time the task list is requested in `routes/web.php`:

```php
Route::get('/', function () {
  // ...

  $stats = Cache::getMemcached()->getStats();

  return view('tasks', [
    'tasks' => $tasks,
    'stats' => array_pop($stats)
  ]);
});
```

Then, we add a card for the stats at the bottom of the task view:

```php
<!-- resources/views/tasks.blade.php -->

<!-- ... -->

<!-- Stats Card -->
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Stats</h5>
    <table class="table table-striped">
      <tr>
        <td>Set commands</td>
        <td>{{ $stats['cmd_set'] }}</td>
      </tr>
      <tr>
        <td>Get hits</td>
        <td>{{ $stats['get_hits'] }}</td>
      </tr>
      <tr>
        <td>Get misses</td>
        <td>{{ $stats['get_misses'] }}</td>
      </tr>
    </table>
  </div>
</div>
```

Now push the changes to Heroku and see the how the stats change when you play with the task list:

```term
$ git commit -am 'Add caching with MemCachier'
$ git push heroku master
$ heroku open
```

You can see that the first time you access the page, the `Get misses` increase
by one. This is because the first time `rememberForever` is called, the task
list is not in the cache. The `Set commands` also increase because the task list
is saved to the cache. If you refresh the page, the misses stay the same,
but the `Get hits` increase because the task list is served from the cache.

When you add a new task or delete a task, your misses will
increase again because the cache was invalidated.

>note
>If you want to see stats in your local setup, you need to set
`CACHE_DRIVER=memcached` in your `.env` file and either run a `memcached` server locally or configure your `MEMCACHIER_*` environment variables accordingly.

### Using Memcache for session storage

On Heroku, it's not advisable to store session information on disk, because dynos have an ephemeral filesystem that doesn't persist across restarts.

Memcache works well for storing information for short-lived sessions that time out. However, because Memcache is a cache and therefore not persistent, long-lived sessions are better suited to permanent storage options, such as your database.

Changing the session store from a file (default) to memcached can be done easily by setting the `SESSION_DRIVER` config var:

```term
$ heroku config:set SESSION_DRIVER=memcached
$ heroku restart
```

### Caching rendered partials

With the help of
[laravel-partialcache](https://github.com/spatie/laravel-partialcache), you can cache rendered partials in Laravel. This is similar to
fragment caching in Ruby on Rails. If you have complex partials in your
application, it's a good idea to cache them because rendering HTML can be a
CPU-intensive task.

> warning
> Do not cache partials that include forms with CSRF tokens.

Our example does not include any complex partials, but for the sake of this
tutorial, let's assume that rendering the task name in the task list takes a
lot of CPU cycles and slows down our page.

First, we need to add the `laravel-partialcache` package to our app:

```term
$ composer require spatie/laravel-partialcache
```

Second, let's factor out the task name into a partial:

```php
<!-- resources/views/task/name.blade.php -->

<td class="table-text">
  <div>{{ $task->name }}</div>
</td>
```

Now we can import and cache this partial in our task view:

```php
<!-- resources/views/tasks.blade.php -->

<!-- ... -->
<table class="table table-striped">
  @foreach ($tasks as $task)
    <tr>
      <!-- Task Name -->
      @cache('task.name', ['task' => $task], null, $task->id)

      <!-- Delete Button -->

<!-- ... -->
```

This caches each task name partial with the ID as its key. Note that in
this example, we never have to invalidate a cached partial because the name
of a task can never change. However, if you add the functionality to change the
name of a task, you can easily invalidate the cached partial with `PartialCache::forget('task.name', $task->id);`.

Let's see the effect of caching the task name partials in our application:

```term
$ git add .
$ git commit -m 'Cache task name partial'
$ git push heroku master
$ heroku open
```

You should now see an additional `Get hit` for each task in your list.

### Caching entire responses

In Laravel, it's also easy to cache the entire rendered HTML response by using
[laravel-responsecache](https://github.com/spatie/laravel-responsecache). This
is similar to view caching in Ruby on Rails. This package is easy
to use and has good documentation in its README. However, we cannot use it in
our example because our task list contains forms with CSRF tokens. To use
this package with Memcache, you have to set the config var
`RESPONSE_CACHE_DRIVER` to `memcached`.

## Further reading & resources

* [MemCachier Add-on Page](https://elements.heroku.com/addons/memcachier)
* [MemCachier Documentation](memcachier)
* [Advance Memcache Usage](advanced-memcache)
* [Heroku Laravel guide](getting-started-with-laravel)
* [Laravel Caching Documentation](https://laravel.com/docs/5.6/cache)
