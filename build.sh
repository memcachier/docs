#! /bin/bash

# construct doc.md
cat intro.md > doc.md
cat misc/supported_protocols.md >> doc.md
cat clients/ruby/ruby.md >> doc.md
cat clients/ruby/rails3_4.md >> doc.md
cat clients/ruby/rails2.md >> doc.md
cat clients/ruby/puma.md >> doc.md
cat clients/ruby/rack.md >> doc.md
cat clients/python/python.md >> doc.md
cat clients/python/django.md >> doc.md
cat clients/php/php.md >> doc.md
cat clients/php/wordpress.md >> doc.md
cat clients/php/cake_php.md >> doc.md
cat clients/php/symfony2.md >> doc.md
cat clients/php/laravel.md >> doc.md
cat clients/js/node_js.md >> doc.md
cat clients/java/java.md >> doc.md
cat clients/supported_clients.md >> doc.md
cat clients/sample_apps.md >> doc.md
cat misc/local_usage.md >> doc.md
cat analytics/analytics.md >> doc.md
cat analytics/api.md >> doc.md
cat analytics/new_relic.md >> doc.md
cat analytics/credentials.md >> doc.md
cat analytics/disabled_caches.md >> doc.md
cat misc/encrypted_connections.md >> doc.md
cat misc/changing_plans.md >> doc.md
cat misc/using_memcachier.md >> doc.md
cat misc/value_limit.md >> doc.md
cat misc/localhost_error.md >> doc.md
cat misc/support.md >> doc.md
# check doc.md for dangling links
./check_links.py
# create direct and heroku version of doc.md
./flavor.py doc.md doc.direct.md direct
./flavor.py doc.md doc.heroku.md heroku
# overwrite heroku doc
rm -f memcachier.md
devcenter pull https://devcenter.heroku.com/articles/memcachier
mv memcachier.md memcachier.old.md
head -n 4 memcachier.old.md > memcachier.md
cat doc.heroku.md >> memcachier.md
