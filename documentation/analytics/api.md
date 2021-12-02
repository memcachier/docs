**IF(direct)**
---
title: "Documentation: Analytics API"
description: "Documentation for using the MemCachier Analytics API"
---
**ENDIF**

## Analytics API

You can also access features available on the [analytics dashboard](#memcachier-analytics)
via the API.

  - [Authenticate](#authentication)
  - [MemCachier API ID](#memcachier-api-id)
  - [Stats](#stats)
  - [History](#history)
  - [Flush](#flush)
  - [List Credentials](#list-credentials)
  - [Create Credentials](#create-credentials)
  - [Update Credentials](#update-credentials)
  - [Promote Credentials](#promote-credentials)
  - [Delete Credentials](#delete-credentials)

### Authentication

MemCachier uses credentials to allow access to the API. After you've created a
cache, you can find your credentials on the
[analytics dashboard](#memcachier-analytics). Only credentials that
have the API capability will be allowed to use this API.

MemCachier expects for your credentials to be included in the header of all API requests.

```term
curl "https://analytics.memcachier.com/api/v1/:memcachier_id/:action"
  --user CRED_USERNAME:CRED_PASSWORD
```

*Make sure to replace `CRED_USERNAME:CRED_PASSWORD` with your credential
username and password found on the analytics dashboard.*

### MemCachier API ID

All of the API paths include a `<memcachier_id>` variable. In order to find
this ID, you'll need to use the `/login` path.

*This is not the same thing as the "MemCachier ID" listed on your analytics dashboard.*

**HTTP Request**

`GET https://analytics.memcachier.com/api/login`

**Response**


<table class="table table-bordered">
<tbody>
<tr>
<th>Status</th>
<th>Response</th>
</tr>
<tr>
<td>200</td>
<td>JSON response with memcachier ID</td>
</tr>
<tr>
<td>403</td>
<td>"You are not authorized to perform this action."</td>
</tr>
<tr>
<td>404</td>
<td>"No cache found."</td>
</tr>
<tr>
<td>500</td>
<td>"Server error"</td>
</tr>
</tbody>
</table>

**Example:**

```term
curl "https://analytics.memcachier.com/api/v1/login"
  --user CRED_USERNAME:CRED_PASSWORD
```

**Returns**:

```json
{
    "cache_id": 1561
}
```

### Stats

This endpoint retrieves all the statistics for your cache.

**HTTP Request**

`GET https://analytics.memcachier.com/api/v1/<memcachier_id>/stats`

**Response**

<table class="table table-bordered">
<tbody>
<tr>
<th>Status</th>
<th>Response</th>
</tr>
<tr>
<td>200</td>
<td>JSON response with stats</td>
</tr>
<tr>
<td>403</td>
<td>"You are not authorized to perform this action."</td>
</tr>
<tr>
<td>500</td>
<td>"Server error: a.b.c.totallyaserver.com:1234,..."</td>
</tr>
</tbody>
</table>

**Example:**

```term
curl "https://analytics.memcachier.com/api/v1/<memcachier_id>/stats"
  --user "CRED_USERNAME:CRED_PASSWORD"
```

**Returns:**

```json
{
    "a.b.c.totallyaserver.com:12345": {
        "auth_cmds": 19,
        "auth_errors": 0,
        "bytes": 0,
        "bytes_read": 960,
        "bytes_written": 22233,
        "cas_badval": 0,
        "cas_hits": 0,
        "cas_misses": 0,
        "cmd_delete": 0,
        "cmd_flush": 0,
        "cmd_get": 0,
        "cmd_set": 0,
        "cmd_touch": 0,
        "curr_connections": 0,
        "curr_items": 0,
        "decr_hits": 0,
        "decr_misses": 0,
        "delete_hits": 0,
        "delete_misses": 0,
        "evictions": 0,
        "expired": 0,
        "get_hits": 0,
        "get_misses": 0,
        "incr_hits": 0,
        "incr_misses": 0,
        "limit_maxbytes": 28835840,
        "time": 1500651085,
        "total_connections": 19,
        "total_items": 0,
        "touch_hits": 0,
        "touch_misses": 0
    }
}
```

### History

This endpoint retrieves the statistical history of a cache.

**HTTP Request**

`GET https://analytics.memcachier.com/api/v1/<memcachier_id>/history`

**Response**

<table class="table table-bordered">
<tbody>
<tr>
<th>Status</th>
<th>Response</th>
</tr>
<tr>
<td>200</td>
<td>JSON response with historical stats</td>
</tr>
<tr>
<td>403</td>
<td>"You are not authorized to perform this action."</td>
</tr>
<tr>
<td>500</td>
<td>"Server error"</td>
</tr>
</tbody>
</table>


**Example:**

```term
curl "https://analytics.memcachier.com/api/v1/<memcachier_id>/history"
  --user "CRED_USERNAME:CRED_PASSWORD"
```

**Returns:**

```json
  [{
    "memcachier_id": "11",
    "server": "a.b.c.totallyaserver.memcachier.com",
    "stats": {
        "auth_cmds": 158,
        "auth_errors": 0,
        "bytes": 0,
        "bytes_read": 3840,
        "bytes_written": 178754,
        "cas_badval": 0,
        "cas_hits": 0,
        "cas_misses": 0,
        "cmd_delete": 0,
        "cmd_flush": 0,
        "cmd_get": 0,
        "cmd_set": 0,
        "cmd_touch": 0,
        "curr_connections": 2,
        "curr_items": 0,
        "decr_hits": 0,
        "decr_misses": 0,
        "delete_hits": 0,
        "delete_misses": 0,
        "evictions": 0,
        "expired": 0,
        "get_hits": 0,
        "get_misses": 0,
        "incr_hits": 0,
        "incr_misses": 0,
        "limit_maxbytes": 1153433600,
        "time": 1490731542,
        "total_connections": 158,
        "total_items": 0,
        "touch_hits": 0,
        "touch_misses": 0
    },
    "timestamp": "1490731541096"
    }, … ]
```

### Flush

This endpoint will flush all of the data from the cache cache.

**HTTP Request**

`POST https://analytics.memcachier.com/api/v1/<memcachier_id>/flush`

**Response**

<table class="table table-bordered">
<tbody>
<tr>
<th>Status</th>
<th>Response</th>
</tr>
<tr>
<td>200</td>
<td>""</td>
</tr>
<tr>
<td>403</td>
<td>"You are not authorized to perform this action."</td>
</tr>
<tr>
<td>500</td>
<td>"Server error: a.b.c.totallyaserver.com:1234,..."</td>
</tr>
</tbody>
</table>

**Example:**

```term
curl "https://analytics.memcachier.com/api/v1/<memcachier_id>/flush" -X POST
  --user "CRED_USERNAME:CRED_PASSWORD"
```

*Certain credentials may not have permission to flush the cache, which will produce a 403 error.*

### List Credentials

The endpoint returns a list of all the credentials connected to the cache.

**HTTP Request**

`GET https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials`

**Response**

<table class="table table-bordered">
<tbody>
<tr>
<th>Status</th>
<th>Response</th>
</tr>
<tr>
<td>200</td>
<td>JSON list of credentials</td>
</tr>
<tr>
<td>403</td>
<td>"You are not authorized to perform this action."</td>
</tr>
<tr>
<td>500</td>
<td>"Server error"</td>
</tr>
</tbody>
</table>

**Example:**

```term
curl "https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials"
  --user "CRED_USERNAME:CRED_PASSWORD"
```

**Returns:**

```json
  [
    {
        "cache_id": 14,
        "flush_capability": false,
        "id": 44,
        "sasl_username": "CRED_USERNAME",
        "uuid": null,
        "write_capability": true,
        "api_capability": true,
        "primary": true,
    },
    {
        "cache_id": 14,
        "flush_capability": false,
        "id": 43,
        "sasl_username": "789101",
        "uuid": null,
        "write_capability": true,
        "api_capability": true,
        "primary": false,
    }, ...
]
```

### Create Credentials

This endpoint creates a new set of credentials which can be used to connect to the cache.

**HTTP Request**

`POST https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials`

**Response**

<table class="table table-bordered">
<tbody>
<tr>
<th>Status</th>
<th>Response</th>
</tr>
<tr>
<td>200</td>
<td>JSON of new credential set</td>
</tr>
<tr>
<td>403</td>
<td>"You are not authorized to perform this action."</td>
</tr>
<tr>
<td>500</td>
<td>"Server error"</td>
</tr>
</tbody>
</table>

**Example:**

```term
curl "https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials" -X POST
  --user "CRED_USERNAME:CRED_PASSWORD"
```

**Returns:**

```json
{
    "cache_id": 14,
    "id": null,
    "sasl_password": "CRED_PASSWORD",
    "sasl_username": "CRED_USERNAME",
    "uuid": null,
    "primary": false,
    "flush_capability": true,
    "write_capability": true,
    "api_capability": true,
}
```

### Update Credentials

This endpoint updates the capabilities of a specific set of credentials.

**HTTP Request**

`POST https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials/<cred_id>`

**Query Parameters**

<table class="table table-bordered">
<tbody>
<tr>
<th>Parameter</th>
<th>Default</th>
<th>Description</th>
</tr>
<tr>
<td>flush_capability</td>
<td>true</td>
<td>Authorize this set of credentials to flush the cache.</td>
</tr>
<tr>
<td>write_capability</td>
<td>true</td>
<td>Authorize this set of credentials to write to the cache.</td>
</tr>
<tr>
<td>api_capability</td>
<td>true</td>
<td>Authorize this set of credentials to use this API.</td>
</tr>
</tbody>
</table>

**Response**

<table class="table table-bordered">
<tbody>
<tr>
<th>Status</th>
<th>Response</th>
</tr>
<tr>
<td>200</td>
<td>JSON of new credential properties</td>
</tr>
<tr>
<td>403</td>
<td>"You are not authorized to perform this action."</td>
</tr>
<tr>
<td>500</td>
<td>"Server error"</td>
</tr>
</tbody>
</table>

**Example:**

```term
curl "https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials/<cred_username>" -X PATCH
  -d '{"flush_capability":"false"}'
  --user "CRED_USERNAME:CRED_PASSWORD"
```

**Returns:**

```json
{
    "flush_capability": false,
    "write_capability": true,
    "api_capability": true,
}
```

### Promote Credentials

This endpoint promotes a set of credentials to primary.

**HTTP Request**

`POST https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials/primary/<cred_id>`

**Response**

<table class="table table-bordered">
<tbody>
<tr>
<th>Status</th>
<th>Response</th>
</tr>
<tr>
<td>200</td>
<td>JSON of promoted credential set</td>
</tr>
<tr>
<td>403</td>
<td>"You are not authorized to perform this action."</td>
</tr>
<tr>
<td>500</td>
<td>"Server error"</td>
</tr>
</tbody>
</table>

**Example:**

```term
curl "https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials/primary/<cred_username>" -X POST
  --user "CRED_USERNAME:CRED_PASSWORD"
```

**Returns:**

```json
{
    "cache_id": 14,
    "id": null,
    "sasl_username": "CRED_USERNAME",
    "uuid": null,
    "primary": true,
    "flush_capability": false,
    "write_capability": true,
    "api_capability": true,
}
```

### Delete Credentials

This endpoint deletes a set of credentials

**HTTP Request**

`POST https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials/primary/<cred_id>`

**Response**

<table class="table table-bordered">
<tbody>
<tr>
<th>Status</th>
<th>Response</th>
</tr>
<tr>
<td>200</td>
<td>""</td>
</tr>
<tr>
<td>403</td>
<td>"You are not authorized to perform this action."</td>
</tr>
<tr>
<td>500</td>
<td>"Server error"</td>
</tr>
</tbody>
</table>

**Example:**

```term
curl "https://analytics.memcachier.com/api/v1/<memcachier_id>/credentials/primary/<cred_username>" -X DELETE
  --user "CRED_USERNAME:CRED_PASSWORD"
```
