#! /bin/bash

# check article for dangling links
./check_links.py heroku_articles/$1.md
# make sure out dir exists
mkdir -p out
# overwrite heroku article
rm -f $1.md
devcenter pull $1
mv $1.md out/$1.old.md
head -n 4 out/$1.old.md > out/$1.md
cat heroku_articles/$1.md >> out/$1.md
