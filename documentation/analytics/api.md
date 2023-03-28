**IF(direct)**
---
title: "Documentation: Analytics API V2"
description: "Documentation for using the MemCachier Analytics API version 2."
---
**ENDIF**

## Analytics API V2

Note, you can also access features available on the
**IF(direct)**
 [analytics dashboard](/documentation/memcachier-analytics)
**ENDIF**
**IF(heroku)**
 [analytics dashboard](#memcachier-analytics)
**ENDIF**
via the API.

- [Authentication](#authentication)
- [Info](#info)
- **[Credentials](#credentials)**
  - [List Credentials](#list-credentials)
  - [Create Credentials](#create-credentials)
  - [Update Credentials](#update-credentials)
  - [Delete Credentials](#delete-credentials)
  - [Promote Credentials](#promote-credentials)
- **[Management](#management)**
  - [Rotate SSO Token](#rotate-sso-token)
  - [Enable Cache](#enable-cache)
  - [Switch Cluster](#switch-cluster)
- **[Commands](#commands)**
  - [Flush](#flush)
  - [Reset Stats](#reset-stats)
  - [Get Stats](#get-stats)
- **[Insight](#insight)**
  - [Get Processed Stats Aggregate](#get-processed-stats-aggregate)
  - [Get Processed Stats Per Server](#get-processed-stats-per-server)
  - [Get Latency](#get-latency)
- **[Alerts](#alerts)**
  - [List Alerts](#list-alerts)
  - [Create Alert](#create-alert)
  - [Get Alert](#get-alert)
  - [Update Alert](#update-alert)
  - [Delete Alert](#delete-alert)
  - [List Delivery Configs](#list-delivery-configs)
  - [Create Delivery Config](#create-delivery-config)
  - [Delete Delivery Config](#delete-delivery-config)
- **[Introspection](#introspection)**
  - [Get Logs](#get-logs)
  - [Get Compound Stats](#get-compound-stats)
  - [Get Popular Items](#get-popular-items)
  - [Get Key Stats](#get-key-stats)
  - [Get Watched Prefixes](#get-watched-prefixes)
  - [Watch Prefix](#watch-prefix)
  - [Unwatch Prefix](#unwatch-prefix)
  - [Get Prefix Stats](#get-prefix-stats)

### Authentication

MemCachier uses credentials to allow access to the API. After you've created a
cache, you can find your cache ID and credentials on the **Settings** page of your
[analytics dashboard](/documentation/memcachier-analytics). Only credentials that
have the API capability will be allowed to use this API.

MemCachier expects for your credentials to be included in the header of all API requests.

```term
curl https://analytics.memcachier.com/api/v2/caches/<cache_id>/<action> \
  --user <username>:<password>
```

*Make sure to replace `<username>:<password>` and `<cache_id>` with your credential
username and password, and your cache ID, found on the Settings page of your analytics dashboard.*

### Info

Returns all information relating to a cache. This includes cache, credential, and cluster related information.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/info
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>A cache object</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/info \
  --user <username>:<password>
```

##### Returns

```json
{
  "id": 4,
  "name": "ABCDEF",
  "label": "string",
  "cache_type": "memcachier",
  "plan": 26214400,
  "provider": "ec2",
  "enabled": true,
  "cluster_name": "string",
  "servers": [
    "string"
  ],
  "credentials": [
    {
      "id": 0,
      "cache_id": 0,
      "sasl_username": "string",
      "sasl_password": "pa$$word",
      "write_capability": true,
      "flush_capability": true,
      "api_capability": true,
      "primary": true
    }
  ],
  "can_switch": true,
  "can_manage_credentials": true,
  "can_update_capabilities": true
}
```

### Credentials

#### List Credentials

The endpoint returns a list of all the credentials connected to the cache.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>A list of credentials</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials \
  --user <username>:<password>
```

##### Returns

```json
[
  {
    "id": 0,
    "cache_id": 0,
    "sasl_username": "string",
    "sasl_password": "pa$$word",
    "write_capability": true,
    "flush_capability": true,
    "api_capability": true,
    "primary": true
  },
  // ...
]
```

#### Create Credentials

This endpoint creates a new set of credentials which can be used to connect to the cache.

Note, development caches cannot manage credentials.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>201</td><td>The newly created credential set.</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Not allowed to manage credentials, or Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials \
  --user <username>:<password>
```

##### Returns

```json
{
  "id": 0,
  "cache_id": 0,
  "sasl_username": "string",
  "sasl_password": "pa$$word",
  "write_capability": true,
  "flush_capability": true,
  "api_capability": true,
  "primary": true
}
```

#### Update Credentials

This endpoint updates the capabilities of a specific set of credentials.

Note, `sasl_username` is your `credential_username`.

##### HTTP Request

```term
PATCH https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials/<credential_username>
```

##### Request Body

Note, if you omit a capability from the request body its value will be set to `false`.

```json
{
  "write_capability": boolean,
  "flush_capability": boolean,
  "api_capability": boolean
}
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Update successful</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Not allowed to manage credentials, or Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X PATCH https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials/<credential_username> \
  --user <username>:<password> \
  -H 'Content-Type: application/json' \
  -d '{"write_capability":true,"flush_capability":false,"api_capability":true}'
```

##### Returns

```json
{
  "flush_capability": false,
  "write_capability": false,
  "api_capability": true,
}
```

#### Delete Credentials

This endpoint deletes a set of credentials.

##### HTTP Request

```term
DELETE https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials/<credential_username>
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Delete successful</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Not allowed to manage credentials, or Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X DELETE https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials/<credential_username> \
  --user <username>:<password>
```

#### Promote Credentials

This endpoint promotes a set of credentials to be your primary credentials.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials/primary/<credential_username>
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Update successful</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/credentials/primary/<credential_username> \
  --user <username>:<password>
```

##### Returns

```json
{
  "id": 0,
  "cache_id": 0,
  "sasl_username": "string",
  "sasl_password": "pa$$word",
  "write_capability": true,
  "flush_capability": true,
  "api_capability": true,
  "primary": true
}
```

### Management

#### Rotate SSO Token

Rotate SSO secret for analytics dashboard, invalidating dashboard URLs.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/rotate_sso
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>SSO rotation successful</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/rotate_sso \
  --user <username>:<password>
```

##### Returns

`string`

#### Enable Cache

Enable a disabled cache.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/enable_cache
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Enabled cache successfully</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/enable_cache \
  --user <username>:<password>
```

#### Switch Cluster

Switch to a different cluster.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/switch_cluster
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Cluster change successful</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/switch_cluster \
  --user <username>:<password>
```

##### Returns

New cluster name.

`string`

### Commands

#### Flush

Flush the cache.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/flush
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>204</td><td>Flushed cache successfully</td></tr>
<tr><td>400</td><td>Failed to flush cache, or The specified cache ID is invalid (not a number).</td></tr>
<tr><td>404</td><td>Cache not found.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/flush \
  --user <username>:<password>
```

#### Reset Stats

Reset stats.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/reset_stats
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>204</td><td>Reset stats successfully</td></tr>
<tr><td>400</td><td>Failed to reset stats, or The specified cache ID is invalid (not a number).</td></tr>
<tr><td>404</td><td>Cache not found.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/reset_stats \
  --user <username>:<password>
```

#### Get Stats

Get stats for a cache.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/stats
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Stats for this cache</td></tr>
<tr><td>400</td><td>Failed to get stats, or The specified cache ID is invalid (not a number).</td></tr>
<tr><td>404</td><td>Cache not found.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/stats \
  --user <username>:<password>
```

##### Returns

```json
{
  "auth_cmds": 0,
  "auth_errors": 0,
  "bytes": 0,
  "bytes_read": 0,
  "bytes_written": 0,
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
  "limit_maxbytes": 0,
  "time": 0,
  "total_connections": 0,
  "total_items": 0,
  "touch_hits": 0,
  "touch_misses": 0
}
```

### Insight

#### Get Processed Stats Aggregate

Get processed stats aggregate for all servers.

The granularity of the timeseries
depends on the start and end time. Up to 24 hours gets 1 minute granularity,
up to 1 week gets 10 minute granularity, up to 3 month gets hour
granularity, and above that gets day granularity.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/insight/processed_stats
```

##### Query Parameters

<table class="table table-bordered">
<tbody>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr><td>names</td><td>No default. Required.</td><td>The name(s) of the stats. Possible values: auth_cmds_rate, auth_errors_rate, bytes, bytes_read_rate, bytes_write_rate, cas_badval_rate, cas_fraction, cas_hit_rate, cas_rate, connection_rate, connections, decr_fraction, decr_hit_rate,decr_rate, delete_fraction, delete_hit_rate, delete_rate, eviction_rate, flush_fraction, flush_rate, get_expired_rate, get_fraction, get_hit_rate, get_rate, hit_rate, incr_fraction, incr_hit_rate, incr_rate, items,max_bytes, request_rate, set_fraction, set_rate, touch_fraction, touch_hit_rate, touch_rate</td></tr>
<tr><td>startTime</td><td>24h ago</td><td>The start time of the timeseries data.</td></tr>
<tr><td>endTime</td><td>Now</td><td>The end time of the timeseries data.</td></tr>
</tbody>
</table>

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Processed stats for this cache.</td></tr>
<tr><td>400</td><td>Failed to query InfluxDB, or InfluxDB query returned error, or query parameter names is required, or the specified cache ID is invalid (not a number).</td></tr>
<tr><td>404</td><td>Cache not found.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/insight/processed_stats?names=auth_cmds_rate,auth_errors_rate,bytes&startTime=2023-01-08T15:20:00Z&endTime=2023-01-10T15:20:00Z \
  --user <username>:<password>
```

##### Returns

```json
[
  {
    "name": "processed_stats",
    "columns": [
      "time",
      "auth_cmds_rate",
      "auth_errors_rate",
      "bytes"
    ],
    "values": [
      [
        "2023-01-10T15:20:00Z",
        0,
        0,
        0
      ],
      ...
    ]
  }
]
```

#### Get Processed Stats Per Server

Get processed stats per server.

The granularity of the timeseries
depends on the start and end time. Up to 24 hours gets 1 minute granularity,
up to 1 week gets 10 minute granularity, up to 3 month gets hour
granularity, and above that gets day granularity.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/insight/processed_stats/per_server
```

##### Query Parameters

<table class="table table-bordered">
<tbody>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr><td>names</td><td>No default. Required.</td><td>The name(s) of the stats. Possible values: auth_cmds_rate, auth_errors_rate, bytes, bytes_read_rate, bytes_write_rate, cas_badval_rate, cas_fraction, cas_hit_rate, cas_rate, connection_rate, connections, decr_fraction, decr_hit_rate,decr_rate, delete_fraction, delete_hit_rate, delete_rate, eviction_rate, flush_fraction, flush_rate, get_expired_rate, get_fraction, get_hit_rate, get_rate, hit_rate, incr_fraction, incr_hit_rate, incr_rate, items,max_bytes, request_rate, set_fraction, set_rate, touch_fraction, touch_hit_rate, touch_rate</td></tr>
<tr><td>startTime</td><td>24h ago</td><td>The start time of the timeseries data.</td></tr>
<tr><td>endTime</td><td>Now</td><td>The end time of the timeseries data.</td></tr>
</tbody>
</table>

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Processed stats for this cache.</td></tr>
<tr><td>400</td><td>Failed to query InfluxDB, or InfluxDB query returned error, or query parameter names is required, or the specified cache ID is invalid (not a number).</td></tr>
<tr><td>404</td><td>Cache not found.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/insight/processed_stats/per_server?names=auth_cmds_rate,auth_errors_rate,bytes&startTime=2023-01-08T15:20:00Z&endTime=2023-01-10T15:20:00Z \
  --user <username>:<password>
```

##### Returns

```json
[
  {
    "name": "processed_stats",
    "tags": {
      "server": "your.server.memcachier.com:11211"
    },
    "columns": [
      "time",
      "hit_rate",
      "bytes",
      "max_bytes"
    ],
    "values": [
      [
        "2023-01-10T15:20:00Z",
        0,
        0,
        0
      ],
      ...
    ]
  },
  ...
]
```

#### Get Latency

Get latency for cache in nanoseconds, grouped by server. The granularity of the timeseries
depends on the start and end time. Up to 24 hours gets 20s granularity,
up to 1 week gets 10 minute granularity, up to 3 month gets hour
granularity, and above that gets day granularity.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/insight/latency
```

##### Query Parameters

<table class="table table-bordered">
<tbody>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr><td>startTime</td><td>24h ago</td><td>The start time of the timeseries data.</td></tr>
<tr><td>endTime</td><td>Now</td><td>The end time of the timeseries data.</td></tr>
</tbody>
</table>

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Latency for this cache in nanoseconds.</td></tr>
<tr><td>400</td><td>Failed to query InfluxDB, or InfluxDB query returned error, or query parameter names is required, or the specified cache ID is invalid (not a number).</td></tr>
<tr><td>404</td><td>Cache not found.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/insight/latency?startTime=2023-01-08T15:20:00Z&endTime=2023-01-10T15:20:00Z \
  --user <username>:<password>
```

##### Returns

```json
[
  {
    "name": "latency",
    "tags": {
      "server": "your.server.memcachier.com:11211"
    },
    "columns": [
      "time",
      "duration"
    ],
    "values": [
      [
        "2023-01-08T15:20:00Z",
        2416805.75
      ],
      ...
    ]
  },
  ...
]
```

### Alerts

#### List Alerts

Get all alerts.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>An array of alert objects.</td></tr>
<tr><td>400</td><td>Alerts could not be retrieved.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts \
  --user <username>:<password>
```

##### Returns

```json
[
  {
  "id": 4,
  "trigger_type": "string", // "hit_rate" or "memory_usage"
  "trigger_threshold": 90,  // percentage 0-100
  "delivery_config_id": 4,
  "description": "string",
  "enabled": true
  },
  ...
]
```

#### Create Alert

Create a new alert.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts
```

##### Request Body

```json
{
  "trigger_type": "string", // "hit_rate" or "memory_usage"
  "trigger_threshold": 0, // percentage 0-100
  "delivery_config_id": 0,
  "description": "string",
  "enabled": boolean
}
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>201</td><td>Added alert successfully.</td></tr>
<tr><td>400</td><td>The alert could not be added. An alert requires a type.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts \
  --user <username>:<password> \
  -H 'Content-Type: application/json' \
  -d '{"trigger_type":"hit_rate","trigger_threshold":50,"delivery_config_id":1,"description":"This is a description.","enabled":true}'
```

##### Returns

```json
{
  "id": 4,
  "trigger_type": "hit_rate",
  "trigger_threshold": 50,
  "delivery_config_id": 1,
  "description": "This is a description.",
  "enabled": true
}
```

#### Get Alert

Get an alert by ID.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/<alert_id>
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>An alert object.</td></tr>
<tr><td>400</td><td>The specified alert ID is invalid (not a number).</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/<alert_id> \
  --user <username>:<password>
```

##### Returns

```json
{
  "id": 4,
  "trigger_type": "string", // "hit_rate" or "memory_usage"
  "trigger_threshold": 80, // percentage 0-100
  "delivery_config_id": 4,
  "description": "string",
  "enabled": true
}
```

#### Update Alert

Updates an alert.

##### HTTP Request

```term
PUT https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/<alert_id>
```

##### Request Body

```json
{
  "id": 0,
  "trigger_type": "string", // "hit_rate" or "memory_usage"
  "trigger_threshold": 0, // percentage 0-100
  "delivery_config_id": 0,
  "description": "string",
  "enabled": boolean
}
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>201</td><td>Updated alert successfully.</td></tr>
<tr><td>400</td><td>The specified alert ID is invalid (not a number), or the alert could not be updated.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X PUT https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/<alert_id> \
  --user <username>:<password> \
  -H 'Content-Type: application/json' \
  -d '{"id":<alert_id>,"enabled":false}'
```

##### Returns

```json
{
  "id": 4,
  "trigger_type": "string", // "hit_rate" or "memory_usage"
  "trigger_threshold": 50, // percentage 0-100
  "delivery_config_id": 1,
  "description": "string",
  "enabled": false,
}
```

#### Delete Alert

Deletes an alert.

##### HTTP Request

```term
DELETE https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/<alert_id>
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>201</td><td>Deleted alert successfully.</td></tr>
<tr><td>400</td><td>The specified alert ID is invalid (not a number), or the alert could not be deleted.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X DELETE https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/<alert_id> \
  --user <username>:<password>
```

#### List Delivery Configs

List alert delivery configs.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/configs
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>An array of alert delivery configs.</td></tr>
<tr><td>400</td><td>Alert delivery configs could not be retrieved.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/configs \
  --user <username>:<password>
```

##### Returns

```json
[
  {
    "id": 1,
    "delivery_type": "string", // "email" or "slack"
    "email": "string",
    "slack_url": "string",
    "slack_channel": "string"
  },
  ...
]
```

#### Create Delivery Config

Create an alert delivery config.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/configs
```

##### Request Body

```json
{
  
"delivery_type": "string", // "email" or "slack"
"email": "string",
"slack_url": "string",
"slack_channel": "string"
}
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>201</td><td>Added alert delivery config successfully.</td></tr>
<tr><td>400</td><td>The alert delivery config could not be added. An alert delivery config requires a type.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/configs \
  --user <username>:<password> \
  -H 'Content-Type: application/json' \
  -d '{"delivery_type":"slack","slack_url":"https://hooks.slack.com/services/...","slack_channel":"#alerts"}'
```

##### Returns

```json
{
  "id": 1,
  "delivery_type": "slack",
  "email": "",
  "slack_url": "https://hooks.slack.com/services/...",
  "slack_channel": "#alerts"
}
```

#### Delete Delivery Config

Delete an alert delivery config.

##### HTTP Request

```term
DELETE https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/configs/<config_id>
```

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>204</td><td>Delete successful.</td></tr>
<tr><td>400</td><td>The specified alert delivery config ID is invalid (not a number), or the alert delivery config could not be deleted.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X DELETE https://insight.memcachier.com/api/v2/caches/<cache_id>/alerts/configs/<config_id> \
  --user <username>:<password>
```

### Introspection

#### Get Logs

Get the last 100 log lines for cache.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/recent_logs
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Recent logs per server.</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/recent_logs \
  --user <username>:<password>
```

##### Returns

```json
{
  "a.b.c.example-server.com:12345": [
    {
      "timestamp": "2023-01-11T10:10:44Z",
      "key": "",
      "command": "STATS",
      "status": "OK",
      "size": 0
    },
    ...  
  ]
}
```

#### Get Compound Stats

Get compound stats for cache.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/compound_stats
```

##### Query Parameters

<table class="table table-bordered">
<tbody>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr><td>startTime</td><td>24h ago</td><td>The start time of the timeseries data.</td></tr>
<tr><td>endTime</td><td>Now</td><td>The end time of the timeseries data.</td></tr>
</tbody>
</table>

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>An array of compound stats.</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/compound_stats?startTime=2023-01-08T15:20:00Z&endTime=2023-01-10T15:20:00Z \
  --user <username>:<password>
```

##### Returns

```json
[
  {
    "name": "compound_stats",
    "columns": [
      "time",
      "num_keys",
      "total_size",
      "total_hits_rate",
      "total_misses_rate",
      "total_mutations_rate"
    ],
    "values": [
      [
        "2023-01-10T15:20:00Z",
        0,
        0,
        0,
        0,
        0
      ],
      ...
    ]
  }
]
```

#### Get Popular Items

Get popular items for cache.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/popular_items
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>A popular items object</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/popular_items \
  --user <username>:<password>
```

##### Returns

```json
{
  "time_slice": 186554450945,
  "most_hit_keys": [
    {
      "name": "string",
      "popularity": 0
    },
    ...
  ],
  "most_missed_keys": [
    {
      "name": "string",
      "popularity": 0
    },
    ...
  ],
  "most_mutated_keys": [
    {
      "name": "string",
      "popularity": 0
    },
    ...
  ],
  "popular_prefixes": [
    {
      "name": "string",
      "popularity": 0
    },
    ...
  ]
}
```

#### Get Key Stats

Get stats for a key by its name.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/key_stats
```

##### Query Parameters

<table class="table table-bordered">
<tbody>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr><td>key</td><td>No default. Required.</td><td>The name of the key.</td></tr>
</tbody>
</table>

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>A popular items object</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/key_stats?key=<key_name> \
  --user <username>:<password>
```

##### Returns

```json
[
  {
    "timestamp": "2019-08-24T14:15:22Z",
    "name": "string",
    "size": 0,
    "hit_count": 0,
    "miss_count": 0,
    "mutation_count": 0,
    "in_cache": true
  }
]
```

#### Get Watched Prefixes

Get all watched prefixes for cache.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>An array of prefixes.</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes \
  --user <username>:<password>
```

##### Returns

```json
[
  {
    "id": 1,
    "name": "string",
  },
  ...
]
```

#### Watch Prefix

Watch a prefix. Start collecting stats for a prefix.

##### HTTP Request

```term
POST https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>Prefix watched. Returns a prefix.</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X POST https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes \
  --user <username>:<password> \
  -H 'Content-Type: application/json' \
  -d '{"name":"my_prefix"}'
```

##### Returns

```json
{
  "id": 1,
  "name": "string",
}
```

#### Unwatch Prefix

Unwatch a prefix. Stop collecting stats for a prefix.

##### HTTP Request

```term
DELETE https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes/<prefix_id>
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>204</td><td>Prefix unwatched.</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl -X DELETE https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes/<prefix_id> \
  --user <username>:<password> \
```

#### Get Prefix Stats

Get stats for a watched prefix.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes/<prefix_id>/stats
```

##### Query Parameters

<table class="table table-bordered">
<tbody>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr><td>startTime</td><td>24h ago</td><td>The start time of the timeseries data.</td></tr>
<tr><td>endTime</td><td>Now</td><td>The end time of the timeseries data.</td></tr>
</tbody>
</table>

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>An array of prefix stats.</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes/<prefix_id>/stats?startTime=2023-01-08T15:20:00Z&endTime=2023-01-10T15:20:00Z \
  --user <username>:<password>
```

##### Returns

```json
[
  {
    "name": "prefix_stats",
    "columns": [
      "time",
      "num_keys",
      "total_size",
      "total_hits_rate",
      "total_misses_rate",
      "total_mutations_rate"
    ],
    "values": [
      [
        "2023-01-16T10:50:00Z",
        0,
        0,
        0,
        0,
        0
      ],
      ...
    ]
  }
]
```

#### Get Prefix Popular Items

Get popular items for a watched prefix.

##### HTTP Request

```term
GET https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes/<prefix_id>/popular_items
```

##### Responses

<table class="table table-bordered">
<tbody>
<tr><th>Status</th><th>Response</th></tr>
<tr><td>200</td><td>An popular items object.</td></tr>
<tr><td>400</td><td>The specified cache ID is invalid (not a number).</td></tr>
<tr><td>401</td><td>Unauthorized to access cache with this ID.</td></tr>
<tr><td>403</td><td>Forbidden to access cache with this ID.</td></tr>
<tr><td>5XX</td><td>Unexpected error.</td></tr>
</tbody>
</table>

##### Example

```term
curl https://insight.memcachier.com/api/v2/caches/<cache_id>/introspection/prefixes/<prefix_id>/popular_items \
  --user <username>:<password>
```

##### Returns

```json
{
  "time_slice": 186554450945,
  "most_hit_keys": [
    {
      "name": "string",
      "popularity": 0
    },
    ...
  ],
  "most_missed_keys": [
    {
      "name": "string",
      "popularity": 0
    },
    ...
  ],
  "most_mutated_keys": [
    {
      "name": "string",
      "popularity": 0
    },
    ...
  ],
  "popular_prefixes": [
    {
      "name": "string",
      "popularity": 0
    },
    ...
  ]
}
```
