
Adding caching to your web applications can drastically improve
performance. The results of complex database queries, expensive
calculations, or slow calls to external resources can be archived in a
simple key-value store that can be accessed via fast O(1) lookups.

>callout
>Static asset caching in Rails 3.1+ using Rack::Cache is outlined in
>[this article](rack-cache-memcached-rails31)

This tutorial will walk you through the steps of creating a simple
Rails 5 application, deploying to Heroku, and using the [MemCachier
Add-on](memcachier) to cache expensive queries.

>note
>We've built a small demo Rails example that you can see running
>[here](https://memcachier-examples-rails5.herokuapp.com/). <br>
><a class="github-source-code" href="https://github.com/memcachier/examples-rails-heroku">Source code</a> or
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-rails-heroku)

## Prerequisites

* Basic Ruby/Rails knowledge
* A locally installed version of Ruby 2.2+, Rubygems, Bundler, and Rails 5+.
  *Note: this guide should also work for Rails 3 and 4.*
* Basic Git knowledge
* A Heroku user account.
  [Signup is free and instant](https://signup.heroku.com/devcenter).

## Create your application

Use the `rails` command to generate your app skeleton:

```term
$ rails new memcache-example
$ cd memcache-example/
```

First, specify the ruby version in you
[Gemfile](http://devcenter.heroku.com/articles/bundler):

```ruby
ruby '2.5.0'
```

Next setup the database. In your Gemfile, change the line that reads:

```ruby
gem 'sqlite3'
```

to

```ruby
group :development do
  gem 'sqlite3'
end

group :production do
  gem 'pg', '~>0.21'
end
```

This ensures the app will make use of the Postgres database in
production. *Note: you may not need to add a version constraint to `pg` in the
future but the current Rails version `5.1.4` is incompatible with the current
pg version `1.0.0`.*

Now run

```term
$ bundle install --without production
```
to update your `Gemfile.lock` file. The `--without production` option will
prevent the pg gem from being installed locally.

Commit your changes (Note: if you use an older version of Rails you might need
to create a Git repository first with `git init`):

```term
$ git add .
$ git commit -m "Initial rails app."
```

## Deploy to Heroku

Use the `heroku` command to provision a new Heroku app:

```term
$ heroku create
```

then deploy to Heroku:

```term
$ git push heroku master
```

## Install the MemCachier add-on and configure caching

As noted in the [MemCachier](memcachier#rails) article, you need to
install the add-on and the `dalli` gem. The optional `memcachier` gem
is also recommended.

At the terminal, run:

```term
$ heroku addons:create memcachier:dev
```

Modify your Gemfile to include `dalli`, a memcache client library, and
`memcachier`, a simple gem that helps with setup:

```ruby
gem 'dalli'
gem 'memcachier'
```
Next run

```term
$ bundle install --without production
```

to install the added gems and update your `Gemfile.lock` file.

Now configure the default Rails caching to utilise the cache store
provided by `dalli` by modifying `config/environments/production.rb`
to include:

```ruby
config.cache_store = :mem_cache_store
```

To make it easier to see how this example works, temporarily turn off
built-in caching:

```ruby
config.action_controller.perform_caching = false
```

## Add some functionality

Use the Rails scaffold generator to create an interface for storing
and viewing a simple directory of names and email addresses:

```term
$ rails g scaffold contact name:string email:string
$ rake db:migrate
```

Edit `config/routes.rb` to set `contacts#index` as the root route,

```ruby
root :to => 'contacts#index'
```

Note: In Rails 3 apps you can now delete `public/index.html`.

Commit the changes, push to Heroku and use the following command to
migrate your remote database:

```term
$ git add .
$ git commit -m "Added first model."
$ git push heroku master
$ heroku run rake db:migrate
```

You should now be able to navigate to your app using `heroku open` to
view your list of contacts. Follow the "New Contact" link and create a
few records.

## Add some caching

The code in your `ContactsController` looks something like this:

```ruby
def index
    @contacts = Contact.all
end
```

Every time `/contacts` is requested, the `index` method will execute
and a database query to fetch all of the records in the contacts table
is run.  

When the table is small and request volume is low this isn't much of
an issue, but as your database and user volume grow, queries like
these can impact the performance of your app. Let's cache the results
of `Contact.all` so that a database query isn't run every time this
page is visited.

>callout
>The `Rails.cache.fetch` method takes a key argument and a block. If
>the key is present, then the corresponding value is returned. If
>not, the block is executed and the value is stored with the given
>key, then returned.

In `app/models/contact.rb`, add the following method to the Contact class:

```ruby
def self.all_cached
  Rails.cache.fetch('Contact.all') { all.to_a }
end
```

In `app/controllers/contacts_controller.rb` change

```ruby
@contacts = Contact.all
```

to

```ruby
@contacts = Contact.all_cached
```

*Note that we cache `all.to_a` instead of `all`. This is because since Rails 4
`Model.all` is executed lazily and you need to convert `Contact.all` into an
array with `to_a` in order to cache the actual contacts.*

Let's also display some statistics on the index page. Add the
following line to the `index` method in
`app/controllers/contacts_controller.rb`:

```ruby
@stats = Rails.cache.stats.first.last
```

And add the following markup to the bottom of
`app/views/contacts/index.html.erb`:

```html
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
```

Commit the results and push to Heroku.

```term
$ git commit -am "Add caching."
$ git push heroku master
```

Refresh the `/contacts` page
and you'll see *"Cache misses: 1"*. This is because you attempted to
fetch the `'Contact.all'` key, but it wasn't present.  Refresh again and
you'll now see *"Cache hits: 1"*.  This time the `'Contact.all'` key was
present because it was stored during your previous request.

You can see this effect again if you clear the cache at the heroku
console:

```term
$ heroku run console
>> Rails.cache.clear
```

## Expiring the cache

Now that `Contact.all` is cached, what happens when that table
changes? Try adding a new contact and returning to the listing page.
You'll see that your new contact isn't displayed. Since `Contact.all`
is cached, the old value is still being served. You need a way of
expiring cache values when something changes.  This can be
accomplished with filters in the `Contact` model.

Add the following code to `app/models/contact.rb` to the Contact class:

```ruby
class Contact < ApplicationRecord
  after_save    :expire_contact_all_cache
  after_destroy :expire_contact_all_cache

  def expire_contact_all_cache
    Rails.cache.delete('Contact.all')
  end

  #...

end
```

Commit these changes and push to Heroku:

```term
$ git commit -am "Expire cache."
$ git push heroku master
```

Now you can see that every
time you save (create or update) or destroy a contact, the
`Contact.all` cache key is deleted. Every time you make one of these
changes and return to `/contacts`, you should see the "Cache misses"
count get incremented by 1.

## Built-in Rails caching

The examples above explain how to fetch and expire caches explicitly.
Conveniently, Rails builds in much of this functionality for you.
By setting

```ruby
config.action_controller.perform_caching = true
```

in `config/environments/production.rb` Rails allows you to do fragment, action,
and page caching.

>callout
>Here we just briefly introduce these caching techniques. For more details and
>other techniques such as russian doll caching, please refer to the
>[Rails Guide on Caching](http://guides.rubyonrails.org/caching_with_rails.html).

### Fragment caching

Pages in Rails are generally built from various components. These components
can be cached with fragment caching so they do not need to be rebuilt each time
the page is requested.

Our `/contacts` page for example is built from contact components, each showing
the name, the email, and 3 actions (show, edit, and destroy). We can cache
these fragments by adding the following to `@contacts.each` loop in
`app/views/contacts/index.html.erb`:

```ruby
# ...
<% @contacts.each do |contact| %>
  <% cache contact do %>
    # ...
  <% end %>
<% end %>
# ...
```

### Action caching

In addition to fragments, Rails can also cache the whole page with page and
action caching. Page caching is more efficient as it allows to completely bypass
the Rails stack but it does not work for pages with before filters, such as
authentication and it is a bit tricky to set up on Heroku because there is no
file storage. Action caching stores objects and views similar to page caching,
but it is served by the Rails stack.

To use action caching you need to add the
[actionpack-action_caching gem](https://github.com/rails/actionpack-action_caching)
to your Gemfile and run `bundle install`:

```ruby
gem 'actionpack-action_caching'
```

To cache the results of the `show` action, for example, add
the following line in `app/controllers/contacts_controller.rb`:

```ruby
class ContactsController < ApplicationController
  caches_action :show
  # ...
end
```

For proper expiration, add the following line in both the `update` and
`destroy` methods in `contacts_controller.rb`

```ruby
def update
  expire_action :action => :show
  # ...
end

def destroy
  expire_action :action => :show
  # ...
end
```

*Note that even if you use action caching, fragment caching remains important.
If a page expires, fragment caching makes sure the whole page does not have to
be rebuilt from scratch but can use already cached fragments. This technique is
similar to russian doll caching.*

### Other caching techniques

There is more ways to use caching in a Rails application such as for session
storage and asset caching.

To use your cache for session storage create (Rails 5) or edit (Rails 3 and 4)
the file `config/initializers/session_store.rb` to contain:

```ruby
# Be sure to restart your server when you modify this file.
Rails.application.config.session_store :cache_store, key: '_memcache-example_session'
```

Asset caching can be done with Rack::Cache. A guide on how to use Rack::Cache
can be found [here](https://devcenter.heroku.com/articles/rack-cache-memcached-rails31).
Note that Rack:Cache can be used to enable Rails page caching on Heroku.

## Further reading and resources

The full source of the application built in this tutorial is freely
available for download on
[GitHub](https://github.com/memcachier/examples-rails3-heroku).

* [Rails Guide on Caching](http://guides.rubyonrails.org/caching_with_rails.html)
* [Caching Strategies for Rails](https://devcenter.heroku.com/articles/caching-strategies)
* [Using Rack::Cache with Memcached](https://devcenter.heroku.com/articles/rack-cache-memcached-rails31)
* [Advance Memcache Usage](https://devcenter.heroku.com/articles/advanced-memcache)
* [MemCachier Documentation](https://devcenter.heroku.com/articles/memcachier)
* [MemCachier Add-on Page](https://elements.heroku.com/addons/memcachier)
