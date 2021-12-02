**IF(direct)**
---
title: "Documentation: Rust"
description: "Documentation for using MemCachier with Rust"
---
**ENDIF**

## Rust

For Rust we recommend the use of the
[memcached-rs](https://github.com/zonyitoo/memcached-rs) client library. Since
version 0.4 it supports SASL authentication and can be used to connect to
MemCachier.

Using `memcached-rs` requires the `MEMCACHIER_SERVERS`, `MEMCACHIER_USERNAME` and
`MEMCACHIER_PASSWORD` environment
**IF(heroku)**
variables that the MemCachier add-on setups.
**ENDIF**
**IF(direct)**
variables. The values for these variables are listed on your
[cache overview page](https://www.memcachier.com/caches).
**ENDIF**

The setup looks as follows:

```rust
extern crate memcached;

use std::env;

use memcached::proto::{Operation, ProtoType};
use memcached::Client;

fn main() {
    let servers = env::var("MEMCACHIER_SERVERS").unwrap();
    let username = env::var("MEMCACHIER_USERNAME").unwrap();
    let password = env::var("MEMCACHIER_PASSWORD").unwrap();


    let mut client = Client::connect_sasl(servers.split(',').map(|s| format!("{}{}", "tcp://", s))
                                                            .map(|s| (s, 1))
                                                            .collect::<Vec<(String, usize)>>()
                                                            .as_slice(),
                                          ProtoType::Binary,
                                          &username, &password).unwrap();

    client.set(b"hello", b"MemCachier", 0xdeadbeef, 2).unwrap();
    let (value, flags) = client.get(b"hello").unwrap();


    println!("Got: {}", std::str::from_utf8(&value).unwrap());
    assert_eq!(&value[..], b"MemCachier");
    assert_eq!(flags, 0xdeadbeef);
}
```
