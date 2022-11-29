#!/usr/bin/env bash

# create direct docs
mkdir -p out_direct
rm out_direct/*
# Getting Started / General Info
./flavor.py documentation/intro.md out_direct/getting-started.md direct
./flavor.py documentation/misc/supported_protocols.md out_direct/supported-protocols-ascii-binary.md direct
./flavor.py documentation/clients/supported_clients.md out_direct/client-library-support.md direct
./flavor.py documentation/misc/local_usage.md out_direct/local-usage.md direct
./flavor.py documentation/misc/using_memcachier.md out_direct/using-memcachier.md direct
./flavor.py documentation/misc/value_limit.md out_direct/key-value-size-limit-1mb.md direct
./flavor.py documentation/misc/encrypted_connections.md out_direct/encrypted-connections.md direct
# Getting Started / Language Support
./flavor.py documentation/clients/go/go.md out_direct/go.md direct
./flavor.py documentation/clients/go/gin.md out_direct/gin.md direct
./flavor.py documentation/clients/java/java.md out_direct/java.md direct
./flavor.py documentation/clients/java/spring-boot.md out_direct/spring-boot.md direct
./flavor.py documentation/clients/node.js/node_js.md out_direct/node-js.md direct
./flavor.py documentation/clients/node.js/express_js.md out_direct/express-js.md direct
./flavor.py documentation/clients/php/php.md out_direct/php.md direct
./flavor.py documentation/clients/php/laravel.md out_direct/laravel.md direct
./flavor.py documentation/clients/php/symfony2.md out_direct/symfony2.md direct
./flavor.py documentation/clients/php/cake_php.md out_direct/cakephp.md direct
./flavor.py documentation/clients/php/wordpress.md out_direct/wordpress.md direct
./flavor.py documentation/clients/python/python.md out_direct/python.md direct
./flavor.py documentation/clients/python/django.md out_direct/django.md direct
./flavor.py documentation/clients/python/flask.md out_direct/flask.md direct
./flavor.py documentation/clients/ruby/ruby.md out_direct/ruby.md direct
./flavor.py documentation/clients/ruby/rails.md out_direct/rails.md direct
./flavor.py documentation/clients/ruby/puma.md out_direct/ruby-puma-webserver.md direct
./flavor.py documentation/clients/ruby/rack.md out_direct/rails-rack-cache.md direct
./flavor.py documentation/clients/rust/rust.md out_direct/rust.md direct
# Getting Started / Example Apllications
./flavor.py documentation/clients/sample_apps.md out_direct/sample-applications.md direct

# User Dashboard / Analytics
./flavor.py documentation/analytics/analytics.md out_direct/memcachier-analytics.md direct

# User Dashboard / Features
./flavor.py documentation/misc/changing_plans.md out_direct/upgrading-downgrading.md direct
./flavor.py documentation/analytics/credentials.md out_direct/credentials.md direct
./flavor.py documentation/analytics/disabled_caches.md out_direct/disabled-caches.md direct

# User Dashboard / Dashboard API
./flavor.py documentation/analytics/api.md out_direct/analytics-api.md direct
