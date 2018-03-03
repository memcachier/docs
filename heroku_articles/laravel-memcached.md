
Memcached is a technology that helps web apps and mobile app backends
in two main ways: *performance* and *scalability*. You should consider
using memcache when your pages are loading too slowly or your app is
having scalability issues. Even for small sites it can be a great
technology, making page loads snappy and future proofing for scale.

This guide will show you how to create a simple [Laravel 5.6](http://laravel.com/)
application, deploy it to Heroku, then add caching with Memcache to alleviate a
performance bottleneck.

>note
>The sample sample app built in this guide can be seen running
>[here](https://memcachier-examples-laravel.herokuapp.com/).<br>
><a class="github-source-code" href="http://github.com/memcachier/examples-laravel">Source code</a> or
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=http://github.com/memcachier/examples-laravel)

## Prerequisites

* PHP (and ideally some Laravel) knowledge.
* A Heroku user account. [Signup is free and instant.](https://signup.heroku.com/signup/dc)
* Familiarity with the [getting Started with PHP on Heroku](getting-started-with-php)
guide, with PHP, Composer and the [Heroku CLI](https://cli.heroku.com) installed
on your computer.

> callout
> This tutorial is based on the
> [Laravel 5.2 tutorial](https://laravel.com/docs/5.2/quickstart) and the
> [Heroku Laravel guide](https://devcenter.heroku.com/articles/getting-started-with-laravel).
> For more details about the creation and deployment of Laravel applications on
> Heroku, please consult these resources.

## Creating a Laravel application on Heroku

We will start by bootstrapping a Laravel skeleton app:

```term
$ composer create-project laravel/laravel --prefer-dist laravel_memcache
Installing laravel/laravel (v5.6.0)
  - Installing laravel/laravel (v5.6.0): Loading from cache
Created project in laravel_memcache
...

$ cd laravel_memcache
```

### Heroku specific setup

Before we can create a working Heroku application we need to add a few Heroku
specific changes. First, we need to create a [Procfile](procfile) to let Heroku
know how to run your application:

```term
$ echo web: vendor/bin/heroku-php-apache2 public/ > Procfile
```

Second, your application needs to trust the Heroku proxies. For this, change
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
> [this](https://stackoverflow.com/questions/48681417/laravel-5-6-trustedproxies-error/48684748#48684748)
> Stackoverflow answer for older versions.

Before we can create a Heroku application, we need to initialize a Git repository
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

### Create and configure Heroku app

Now we are ready to create the Heroku application:

```term
$ heroku create
Creating app... done, ⬢ serene-castle-14546
https://serene-castle-14546.herokuapp.com/ | https://git.heroku.com/serene-castle-14546.git
```

Before we can deploy our Laravel skeleton we need to add a couple of
configurations in the form of environment variables. First, we need to set a
Laravel encryption key:

```term
$ heroku config:set APP_KEY=$(php artisan key:generate --show)
Setting APP_KEY and restarting ⬢ serene-castle-14546... done, v3
APP_KEY: base64:E8Ay5w611tCLkqLnGSualCypRR+s8PGSfK20M+0HNIU=
```

Second, you need to configure the logger to write to `errorlog`:

```term
$ heroku config:set LOG_CHANNEL=errorlog
```

Note, if you prefer you may also configure `errorlog` to be your default log
channel in `config/loging.php`:

```php
'driver' => env('LOG_CHANNEL', 'errorlog'),
```

Next, it's time to deploy to Heroku:

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

And that's it! Type `heroku open` to see the application in your browser.


## Let's create a task list

Having set up the skeleton Laravel application on Heroku it is time to add some
functionality. We will be creating a task list that allows us to view, add, and
delete tasks. For this we will first need to set up the database, create a
table to store tasks and then create the actual views and controller logic.

### Set up the database

Before configuring the database in Laravel we actually need one. On Heroku you
can add a free development database to your app as follows:

```term
$ heroku addons:create heroku-postgresql:hobby-dev
```

This will creat a PostgreSQL database and add a `DATABASE_URL` with the access
information to your environment variables. To use this database, you need to
configure it in `config/database.php`:

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
```

To make sure this `pgsql` connection is used when the app is running on Heroku
set the `DB_CONNECTION` variable:

```term
$ heroku config:set DB_CONNECTION=pgsql
```

If you want to test your app locally (optional), we recommend you use SQLite.
For this, make sure you have `php-sqlite` installed and configure the sqlite
connection in `config/database.php`:

```php
'sqlite' => [
    'driver' => 'sqlite',
    'database' => database_path('database.sqlite'),
    'prefix' => '',
],
```

To use this connection locally, set `DB_CONNECTION=sqlite` in the `.env` file.
Additionally, to make sure artisan does not complain about setting up pgsql from
non-existing parameters, you can also set a dummy database URL:
`DATABASE_URL=postgres://u:p@localhost:5432/dummy-db`.

Save the changes so far by committing:

```term
$ git commit -am 'Configure DB connections'
```

### Create Task table

Now it is time to create the data that will go into the database. In Laravel we
do this by creating a task list migration:

```term
$ php artisan make:migration create_tasks_table --create=tasks
```

We want our tasks to have names so lets add `name` to the `tasks` table in
`database/migrations/<date>_crate_tasks_table.php`:

```php
Schema::create('tasks', function (Blueprint $table) {
    $table->increments('id');
    $table->string('name');
    $table->timestamps();
});
```

To easily access the tasks table we create a `Task` model:

```term
$ php artisan make:model Task
```
This will create an empty `Task` model in `app/Task.php`. Don't worry about it,
Laravel will infer it's fields from the migration.

In case you set up SQLite locally, create the database and run the migrations
(optional):

```term
$ touch database/database.sqlite
$ php artisan migrate --force
```

Finally, commit and run the migrations on Heroku:

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

### Add the view tasks functionality

To view the tasks stored in the database we will now create a view that lists
all tasks.
Before we code the actual task view, we add a layout to put all the
boilerplate:

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

The task view can now be created as a child view of our layout:

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

    <!-- TODO: Memcached Stats Card -->

  </div>
@endsection
```

Ignore the `TODOs` for now, we will fill them out later. To actually
access this view we will now connect it to the top route in `routes/web.php`:

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

If you have a local setup, you could now start a web server with
`php artisan serve` and visit the view at `localhost:8000`. However, it will
be a pretty boring site as the task list is empty.

### Add the add task functionality

To make our task list more useful we will need to be able to add tasks. So let
us create a card for that:

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

Since the task name is provided by the user we need to make sure the input is
sound. In our case we want to make sure the user provides an actual name and
said name should not exceed 255 characters. If the input fails to validate
according to this rules we will display the following error view:

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

With the views created we need to properly route them in `routes/web.php`:

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

Now starting a local web server with `php artisan serve` and visiting
`localhost:8000` will be a bit more interesting as you can add actual tasks.
However, to complete our task list we need to be able to remove completed tasks.

### Add the delete task functionality

To delete a task we will add a button to each item in the task list:

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

Then we wire this functionaility to the appropriate route in `routes/web.php`:

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

Having a working task list, it is time to learn how to use memcache.

## Add caching to Laravel

Memcache is an in-memory, distributed cache. The primary API for
interacting with it are `SET(key, value)` and `GET(key)` operations.
Memcache is like a hashmap (or dictionary) that is spread across
multiple servers, where operations are still performed in constant
time.

The most common usage of memcache is to cache expensive database
queries and HTML renders such that these expensive operations don’t
need to happen over and over again.

### Set up memcached

In order to use memcached in Laravel you first need to have an actual memcached
cache. You can easily get one for free with the
[MemCachier addon](https://elements.heroku.com/addons/memcachier):

```term
$ heroku addons:create memcachier:dev
```

Before you can use memcached on your local machine, you need to install the
`php-memcached` PECL extention via your OS package manager. Then you need to
uncomment `;extension=memcached.so` in `/etc/php/conf.d/memcached.ini`. On
Heroku this dependency is already installed and configured.

Now, to set up memcached in Laravel we need to add dependency to
`composer.json`:

```term
$ composer require ext-memcached
```

Then we need to config the cache in `config/cache.php`:

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

For Laravel to use memcached as its cache you will need to set the `CACHE_DRIVER`
environment variable:

```term
$ heroku config:set CACHE_DRIVER=memcached
```

### Caching expensive database queries

Memcache is often used to cache expensive database queries. Of course our simple
task list does not have any expensive queries but for the sake of this tutorial
let's assume getting all the tasks from the database is a slow operation.

A nice way to add caching to Laravel is with the `rememberForever` function.
This function takes a key and a function that returns a value as its arguments.
It will then lookup the key in the cache. If the value is in the cache it will
return that value. If not, it will execute the function, store the returned
value in the cache with the given key, and return the value. This means that
the first time you call `rememberForever` it will execute the expensive
function but every successive call to `rememberForever` will get the value out
of the cache.

With `rememberForever` it is trivial to add caching to the task view controller
in `routes/web.php`:

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

As you might have noticed we now have a problem if we add or remove a task.
Since `rememberForever` will get the task list from the cache any changes to
the data in the database will not show on the task list. For this reason,
whenever we change the tasks in the database we need to invalidate the cache:

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

### Add some stats

To demystify the caching operations a bit we can visualize what is going on
under the hood by showing some memcache stats. First we need to get the
stats each time the task list is requested in `routes/web.php`:

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

Then we add an extra card for the stats at the bottom of the task view:

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

Now push the changes to Heroku and see the how the stats change when you play
with the task list:

```term
$ git commit -am 'Add caching with MemCachier'
$ git push heroku master
$ heroku open
```

You can see that the first time you access the page, the `Get misses` increase
by one. This is because the first time `rememberForever` is called, the task
list is not in the cache. The `Set commands` also increased because the task list
got saved to the cache. If you refresh the page, the misses will stay the same
but the `Get hits` will increase. Now the task list is served from the cache.
When you add a new task or delete a cache you will see that your misses will
increase again since the cache was invalidated.

Note: if you want to see stats in your local setup, you will need to set
`CACHE_DRIVER=memcached` in your `.env` file and either run a `memcached` server
locally or configure the `MEMCACHIER_*` variables accordingly.

### Use memcached for session storage

On Heroku it is a good idea to store sessions in memcached instead of in a file
on disk because dynos only have an ephemeral filesystem that is not persistent
across dyno restarts. Memcached works well for sessions that time out, however,
since memcached is a cache and thus not persistent, saving long-lived
sessions in memcached might not be ideal. For long-lived sessions consider a
permanent storage option such as you database.

Changing the session store from a file (default) to memcached can be done easily
by just setting an environment variable:

```term
$ heroku config:set SESSION_DRIVER=memcached
$ heroku restart
```

### Caching rendered partials

With the help of
[laravel-partialcache](https://github.com/spatie/laravel-partialcache) you can
also cache rendered partials in Laravel. This is essentially the same as
fragment caching in Ruby on Rails. If you have complex partials in your
application it is a good idea to cache them because rendering HTML can be a
CPU intensive task.

> warning
> Do not cache partials that include forms with CSRF tokens.

Our example does not have any complex partials but for the sake of this
tutorial let us assume that rendering the task name in the task list takes a
lot of CPU cycles and slows down our page.

First, we need to add the package to our app:

```term
$ composer require spatie/laravel-partialcache
```

Second, let us factor out the task name into a partial:

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

This will cache each task name partial with the ID as it's key. Note that in
this example we will never have to invalidate a cached partial because the name
of a task can never change. However, if you add the functionality to change the
name of a task you could easily invalidate the cached partial for that given
task with `PartialCache::forget('task.name', $task->id);`.

Let us see the effect of caching the task name partials in our application:

```term
$ git add .
$ git commit -m 'Cache task name partial'
$ git push heroku master
$ heroku open
```

You should now see an additional get hit for each task in your list.

### Caching entire reponses

In Laravel it is also easy to cache the entire rendered HTML response by using
[laravel-responsecache](https://github.com/spatie/laravel-responsecache). This
is essentially the same as view caching in Ruby on Rails. This package is easy
to use and has good documentation in it's README. However, we cannot use it in
our example because our task list contains forms with CSRF tokens. To use
this package with memcached you have to set the environment variable
`RESPONSE_CACHE_DRIVER` to `memcached`.

## Further reading & resources

* [MemCachier Add-on Page](https://elements.heroku.com/addons/memcachier)
* [MemCachier Documentation](memcachier)
* [Advance Memcache Usage](advanced-memcache)
* [Heroku Laravel guide](getting-started-with-laravel)
* [Laravel Caching Documentation](https://laravel.com/docs/5.6/cache)
