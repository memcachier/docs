#!/usr/bin/env bash

# check article for dangling links
./check_links.py heroku_articles/$1.md
# make sure out_heroku dir exists
mkdir -p out_heroku
# overwrite heroku article
rm -f $1.md
devcenter pull $1
mv $1.md out_heroku/$1.old.md
head -n 4 out_heroku/$1.old.md > out_heroku/$1.md
cat heroku_articles/$1.md >> out_heroku/$1.md
