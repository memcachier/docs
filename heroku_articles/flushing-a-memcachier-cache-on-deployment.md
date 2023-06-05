
The [MemCachier](https://elements.heroku.com/addons/memcachier) add-on provides an [HTTP API](memcachier#analytics-api-v2) endpoint for flushing the contents of a cache. The [`flush`](memcachier#flush) endpoint allows you to set up a Heroku [App Webhook](app-webhooks) that flushes your cache every time you deploy, ensuring that your cache is clean after each deployment.

## Step 1: Obtain your MemCachier credentials

To communicate with the MemCachier API, you need your MemCachier username, password, and cache ID. You can find your credentials and cache ID on the **Settings** page of your
[analytics dashboard](/documentation/memcachier-analytics).

>note
>Only credentials that have the API capability can access the MemCachier API. You can also manage capabilities from the analytics dashboard **Settings** page.

To access your application's MemCachier analytics dashboard, run the following [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) command in your terminal:

```term
$ heroku addons:open memcachier
```

## Step 2: Test out flushing the cache

To test flushing your cache, you'll perform a cURL request. You'll pass a basic Authorization header to authenticate the request. The Authorization header requires a Base64-encoded value: a username and password separated by a colon. For example, `username:password` would be Base64-encoded to `dXNlcm5hbWU6cGFzc3dvcmQ=`.

On Unix-like operating systems such as macOS and Linux, you can Base64 encode your username and password with the following command, adding your actual username and password values:

```term
$ echo -n <username>:<password> | base64
```

`echo -n` removes the trailing newline character. If a newline character is accidentally added when encoding, authorization will fail with the error, `code=401, message=Bad user`.

You can now flush your cache with the following cURL request. Make sure to substitute your cache ID and Base64-encoded credentials:

```term
$ curl -X POST https://analytics.memcachier.com/api/v2/caches/<cache_id>/flush \
  -H 'Authorization: Basic <base64_encoded_username:password>'
```

## Step 3: Subscribe to Webhook notifications

After you verify the cURL flush command is working by successfully flushing your cache, you're ready to subscribe to deploy webhook notifications.

To trigger the flush command when you deploy your app, you'll subscribe to notifications from the [`api:release`](https://devcenter.heroku.com/articles/app-webhooks#step-2-determine-which-events-to-subscribe-to) entity. In your terminal, run the `webhooks:add` Heroku CLI command. Again, make sure to substitute your cache ID and Base64-encoded credentials:

```term
$ heroku webhooks:add \
-i api:release \
-l notify \
-u https://analytics.memcachier.com/api/v2/caches/<cache_id>/flush  \
-t 'Basic <base64_encoded_username:password>'
```

See the Heroku [App Webhooks documentation](https://devcenter.heroku.com/articles/app-webhooks#step-3-subscribe) to explain the options used in that command.

Now, any time you deploy to Heroku, your cache will automatically flush its old data.

>note
>If you ever update your MemCachier credentials, you must also update your webhook.

## Additional resources

See the [Webhook documentation](https://devcenter.heroku.com/articles/app-webhooks) for more information on setting up Heroku Webhooks.

To learn more about the MemCachier API, see our [documentation](memcachier#analytics-api-v2).
The [MemCachier](https://elements.heroku.com/addons/memcachier) add-on provides an [HTTP API](memcachier#analytics-api-v2) endpoint for flushing the contents of a cache. The `flush` endpoint allows you to set up a Heroku [App Webhook](app-webhooks) that flushes your cache every time you deploy, ensuring that your cache is clean and ready to go.