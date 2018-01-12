# MemCachier Documentation

MemCachier documentation.

## Build docs

To compile individual \*.md files into the final documentation execute:

```shell
$ ./build_docs.sh
```

This will create `doc.direct.md` with the documentation for our webpage and it
will create the `memcachier.md` file with the Heroku documentation. Push the
changes to Heroku:

```shell
$ devcenter push memcachier.md
```

## Get involved!

We are happy to receive bug reports, fixes, documentation
enhancements, and other improvements.

Please report bugs via the [github issue
tracker](http://github.com/memcachier/docs/issues).

Master [git repository](http://github.com/memcachier/docs):

* `git clone git://github.com/memcachier/docs.git`

## Licensing

<a rel="license"
href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative
Commons License" style="border-width:0"
src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br
/><span xmlns:dct="http://purl.org/dc/terms/"
property="dct:title">MemCachier Docs </span> by <a
xmlns:cc="http://creativecommons.org/ns#"
href="https://github.com/memcachier/docs"
property="cc:attributionName" rel="cc:attributionURL">MemCachier
Inc</a> is licensed under a <a rel="license"
href="http://creativecommons.org/licenses/by/4.0/">Creative Commons
Attribution 4.0 International License</a>.
