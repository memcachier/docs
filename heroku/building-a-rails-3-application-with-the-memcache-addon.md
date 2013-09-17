---
title: Building a Rails 3 Application with the MemCachier Add-on
id: 493
markdown_flavour: maruku


Adding caching to your web applications can drastically improve
performance. The results of complex database queries, expensive
calculations, or slow calls to external resources can be archived in a
simple key-value store that can be accessed via fast O(1) lookups.

<div class="callout" markdown="1">
Static asset caching in Rails 3.1+ using Rack::Cache is outlined in
[this article](rack-cache-memcached-rails31)
</div>

This tutorial will walk you through the steps of creating a simple
Rails 3.2 application, deploying to Heroku, and using the [MemCachier
Add-on](memcachier) to cache expensive queries.

<p class="note" markdown="1">
Sample code for the [demo Rails
application](https://github.com/memcachier/examples-rails3-heroku) is
available on GitHub. A running version of the example can be found
[here](http://memcachier-examples-rails3.herokuapp.com/).
</p>

# Prerequisites

* Basic Ruby/Rails knowledge, including an installed version of Ruby
  1.9.2, Rubygems, Bundler, and Rails 3.
* Basic Git knowledge
* A Heroku user account. [Signup is free and
  instant](https://api.heroku.com/signup/devcenter).

## Create your application

Use the `rails` command to generate your app skeleton:

    :::term
    $ rails new memcache-example
    $ cd memcache-example/

Next setup the database. In your
[Gemfile](http://devcenter.heroku.com/articles/bundler), change the
line that reads:

    :::ruby
    gem 'sqlite3'

to

    :::ruby
    group :development do
      gem 'sqlite3'
    end
   
    group :production do
      gem 'pg'
    end

This ensures the app will make use of the Postgres database in
production.

Next run:

    :::term
    $ bundle install --without production

to install the specified gems and create your `Gemfile.lock` file.
The `--without production` option will prevent the pg gem from
being installed locally.

Make this project a Git repository and commit your changes:

    :::term
    $ git init
    $ git add .
    $ git commit -m "first commit"

## Deploy to heroku

Use the `heroku` command to provision a new Heroku app:

    :::term
    $ heroku create

then deploy to Heroku:

    :::term
    $ git push heroku master

## Install the MemCachier add-on and configure caching

As noted in the [MemCachier](memcachier#rails) article, you need to
install the add-on and the `dalli` gem. The optional `memcachier` gem
is also recommended.

At the terminal, run:

    :::term
    $ heroku addons:add memcachier:dev

Modify your Gemfile to include `dalli`, a memcache client library, and
`memcachier`, a simple gem that helps with setup:

    :::ruby
    gem 'dalli'
    gem 'memcachier'

Now configure the default Rails caching to utilise the cache store
provided by `dalli` by modifying `config/environments/production.rb`
to include:

    :::ruby
    config.cache_store = :dalli_store

To make it easier to see how this example works, temporarily turn off
built-in caching by commenting out this line:

    :::ruby
    # config.action_controller.perform_caching = true

## Add some functionality

Use the Rails scaffold generator to create an interface for storing
and viewing a simple directory of names and email addresses:

    :::term
    $ rails g scaffold contact name:string email:string
    $ rake db:migrate

Edit `config/routes.rb` to set `contacts#index` as the root route,

    :::ruby
    root :to => 'contacts#index'

and delete `public/index.html`.

Commit the changes, push to Heroku and use the following command to
migrate your remote database:

    :::term
    $ heroku run rake db:migrate

You should now be able to navigate to your app using `heroku open` to
view your list of contacts. Follow the "New Contact" link and create a
few records.

## Add some caching

The code in your `ContactsController` looks something like this:

    :::ruby
    def index
        @contacts = Contact.all
    
        respond_to do |format|
          format.html # index.html.erb
          format.json { render json: @contacts }
        end
    end

Every time `/contacts` is requested, the `index` method will execute
and a database query to fetch all of the records in the contacts table
is run.  
    
When the table is small and request volume is low this isn't much of
an issue, but as your database and user volume grow, queries like
these can impact the performance of your app. Let's cache the results
of `Contact.all` so that a database query isn't run every time this
page is visited.

<div class="callout" markdown="1">
The `Rails.cache.fetch` method takes a key argument and a block. If
the key is present, then the corresponding value is returned. If
not, the block is executed and the value is stored with the given
key, then returned.
</div>

In `app/models/contact.rb`, add the following method:

    :::ruby
    def self.all_cached
      Rails.cache.fetch('Contact.all') { all }
    end

In `app/controllers/contacts_controller.rb` change

    :::ruby
    @contacts = Contact.all

to

    :::ruby
    @contacts = Contact.all_cached

Let's also display some statistics on the index page. Add the
following line to the `index` method in
`app/controllers/contacts_controller.rb`:

    :::ruby
    @stats = Rails.cache.stats.first.last

And add the following markup to the bottom of
`app/views/contacts/index.html.erb`:

    :::html
    <h1>Cache Stats</h1>
   
    <table>
      <tr>
        <th>Metric</th>
        <th>Value</th>
      </tr>
      <tr>
        <td>Cache hits:</td>
        <td><%= @stats['get_hits'] %></td>
      </tr>
      <tr>
        <td>Cache misses:</td>
        <td><%= @stats['get_misses'] %></td>
      </tr>
      <tr>
        <td>Cache flushes:</td>
        <td><%= @stats['cmd_flush'] %></td>
      </tr>
    </table>

Commit the results and push to Heroku. Refresh the `/contacts` page
and you'll see "Cache misses: 1". This is because you attempted to
fetch the 'Contact.all' key, but it wasn't present.  Refresh again and
you'll now see "Cache hits: 1".  This time the 'Contact.all' key was
present because it was stored during your previous request.

You can see this effect again if you clear the cache at the heroku
console:

    :::term
    $ heroku run console
    >> Rails.cache.clear

## Expiring the cache

Now that `Contact.all` is cached, what happens when that table
changes? Try adding a new contact and returning to the listing page.
You'll see that your new contact isn't displayed. Since `Contact.all`
is cached, the old value is still being served. You need a way of
expiring cache values when something changes.  This can be
accomplished with filters in the `Contact` model.

Add the following code to `app/models/contact.rb`:

    :::ruby
    after_save    :expire_contact_all_cache
    after_destroy :expire_contact_all_cache
   
    def expire_contact_all_cache
      Rails.cache.delete('Contact.all')
    end

Commit these changes and push to Heroku. Now you can see that every
time you save (create or update) or destroy a contact, the
`Contact.all` cache key is deleted. Every time you make one of these
changes and return to `/contacts`, you should see the "Cache misses"
count get incremented by 1.

## Built-in rails action caching

The examples above explain how to fetch and expire caches explicitly.
Conveniently, Rails builds in much of this functionality for you.  If
you want to cache the results of the `show` action, for example, add
the following line in `app/controllers/contacts_controller.rb`:

    :::ruby
    caches_action :show

For proper expiration, add the following line in both the `update` and
`destroy` methods in `contacts_controller.rb`

    :::ruby
    expire_action :action => :show

Action caching stores objects and views in a very similar to page
caching, but requests actually hit the application stack so that
before filters can be applied for things like authentication.

For further reading, the [Rails Guide on
Caching](http://guides.rubyonrails.org/caching_with_rails.html) has
excellent information on action, fragment, and other types of caching
built into Rails.

## Code

The full source of the application built in this tutorial is freely
available for download on [GitHub][repo].

[repo]: https://github.com/mattmanning/memcache-example "Examples Rails app with MemCache"
