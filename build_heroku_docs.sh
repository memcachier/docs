#!/usr/bin/env bash

# create Heroku docs
cat documentation/intro.md > doc.md
cat documentation/misc/supported_protocols.md >> doc.md
cat documentation/clients/ruby/ruby.md >> doc.md
cat documentation/clients/ruby/rails.md >> doc.md
cat documentation/clients/ruby/puma.md >> doc.md
cat documentation/clients/ruby/rack.md >> doc.md
cat documentation/clients/python/python.md >> doc.md
cat documentation/clients/python/django.md >> doc.md
cat documentation/clients/python/flask.md >> doc.md
cat documentation/clients/php/php.md >> doc.md
cat documentation/clients/php/laravel.md >> doc.md
cat documentation/clients/php/symfony2.md >> doc.md
cat documentation/clients/php/cake_php.md >> doc.md
cat documentation/clients/php/wordpress.md >> doc.md
cat documentation/clients/node.js/node_js.md >> doc.md
cat documentation/clients/java/java.md >> doc.md
cat documentation/clients/java/spring-boot.md >> doc.md
cat documentation/clients/go/go.md >> doc.md
cat documentation/clients/go/gin.md >> doc.md
cat documentation/clients/rust/rust.md >> doc.md
cat documentation/clients/supported_clients.md >> doc.md
cat documentation/clients/sample_apps.md >> doc.md
cat documentation/misc/local_usage.md >> doc.md
cat documentation/analytics/analytics.md >> doc.md
cat documentation/analytics/api.md >> doc.md
cat documentation/analytics/credentials.md >> doc.md
cat documentation/analytics/disabled_caches.md >> doc.md
cat documentation/misc/encrypted_connections.md >> doc.md
cat documentation/misc/changing_plans.md >> doc.md
cat documentation/misc/using_memcachier.md >> doc.md
cat documentation/misc/value_limit.md >> doc.md
cat documentation/misc/localhost_error.md >> doc.md
cat documentation/misc/support.md >> doc.md
# create heroku version of doc.md
./flavor.py doc.md doc.heroku.md heroku
# check doc.md for dangling links
./check_links.py doc.heroku.md
# overwrite heroku doc
mkdir -p out_heroku
rm -f memcachier.md
devcenter pull memcachier
mv memcachier.md out_heroku/memcachier.old.md
head -n 4 out_heroku/memcachier.old.md > out_heroku/memcachier.md
cat doc.heroku.md >> out_heroku/memcachier.md
# clean up
rm doc.heroku.md
rm doc.md
