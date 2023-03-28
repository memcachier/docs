
The [MemCachier](https://elements.heroku.com/addons/memcachier) add-on provides an HTTP API for flushing its cache contents. This allows you to set up a Heroku HTTP [deploy hook](deploy-hooks) that flushes your cache every time you deploy to staging or production, ensuring that your cache is clean and ready to go.

## Step 1: Obtain your MemCachier credentials

To communciate with the MemCachier API, you need the values of your app's `MEMCACHIER_USERNAME` and `MEMCACHIER_PASSWORD` config vars. You can obtain these values with the `heroku config` CLI command, or by looking them up on your MemCachier analytics dashboard.

After you obtain these values, you can use them to obtain your cache's unique ID. Send the following cURL request, providing your MemCachier username and password where indicated:

```term
$ curl "https://analytics.memcachier.com/api/v1/login" \
> --user "REPLACE_WITH_MEMCACHIER_USERNAME:REPLACE_WITH_MEMCACHIER_PASSWORD"
```

The body of the API's response includes your cache's unique ID:

```json
{
  "cache_id": 123456
}
```

## Step 2: Test out flushing the cache

After you have your MemCachier username, password, and cache ID, you can flush your cache with the following cURL request (substitute your credentials where indicated):

```term
$ curl "https://analytics.memcachier.com/api/v1/REPLACE_WITH_MEMCACHIER_CACHE_ID/flush" \
> -X POST --user "REPLACE_WITH_MEMCACHIER_USERNAME:REPLACE_WITH_MEMCACHIER_PASSWORD"
```

If the above request returns an error, ensure that your credentials are configured for API access on your analytics dashboard:

![Analytics dashboard credentials](https://s3.amazonaws.com/heroku-devcenter-files/article-images/1508409957-screen-shot-2017-09-07-at-11-14-48-am.png)

## Step 3: Set up a deploy hook

After you successfully flush your cache with a cURL request, you can set up a deploy hook with the same set of credentials, like so (substitute your credentials where indicated):

```term
$ heroku addons:create deployhooks:http \
> --url="https://REPLACE_WITH_MEMCACHIER_USERNAME:REPLACE_WITH_MEMCACHIER_PASSWORD@\
> analytics.memcachier.com/api/v1//REPLACE_WITH_MEMCACHIER_CACHE_ID/flush"
```

And that’s it! Pretty simple. Now, any time you deploy a new commit to Heroku, your cache will automatically flush its old data away, allowing you to run tests on relevant data.

>note
>If you ever update replace your MemCachier credentials, you’ll need to manually update your deploy hook as well.

## Additional resources

See [Deploy Hooks](https://devcenter.heroku.com/articles/deploy-hooks#http-post-hook) for more information on setting up Heroku deploy hooks.

To learn more about the features of the MemCachier API, see the [full documentation](memcachier#analytics-api-v2).
