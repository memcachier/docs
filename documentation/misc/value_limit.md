---
title: "Documentation: Key-Value size limit (1MB)"
description: "MemCachier has a maximum size that a key-value object can be of 1MB."
---

## Key-Value size limit (1MB)

MemCachier has a maximum size that a key-value object can be of
**1MB**. This applies to both key-value pairs created through a `set`
command, or existing key-value pairs grown through the use of an
`append` or `prepend` command. In the later case, the size of the
key-value pair with the new data added to it, must still be less than
1MB.

The 1MB limit applies to the size of the key and the value together. A
key of size 512KB with a value of 712KB would be in violation of the
1MB limit.

The reason for this has partially to do with how memory is managed in
MemCachier. A limitation of the high performance design is a
restriction on how large key-value pairs can become. Another reason is
that storing values larger than 1MB doesn't normally make sense in a
high-performance key-value store. The network transfer time in these
situations becomes the limiting factor for performance. A disk cache
or even a database makes sense for this size value.
