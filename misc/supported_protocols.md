
## Supported Protocols: ASCII & Binary

MemCachier supports both the memcache binary and ASCII protocols. Our preferred
method is to use the binary protocol as it natively supports user
authentication and improves the performance slightly over the ASCII protocol.
All our documentation is written for using the binary protocol.

The ASCII protocol does not natively support user authentication. For
MemCachier, where all connections require authentication, we extend the ASCII
protocol in a very simple way. Once the connection is established, you should
send a `set` command with your username as the key and your password as the
value. For example:

```shell
$ telnet 35865.1e4cfd.us-east-3.ec2.prod.memcachier.com 11211
>
> set 15F38e 0 0 32
> 52353F9F1C4017CC16FD348B982ED47D
> STORED
```

You'll need to do this quickly! As we timeout connections that don't
authenticate within a few seconds. Once authenticated, the full ASCII protocol
is available to you.
