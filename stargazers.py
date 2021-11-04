#! /bin/python

# This script plots the stars over time and the star growth rate of a GitHub
# repository.
# This is useful to assess the popularity of a repository.
#
# Note: getting the stargazers takes a ton of time (hours). The script will
# save all stargazers that it already retreived and only get the missing ones.

import json
import csv
import datetime
import time
from matplotlib import pyplot as plt
from datetime import date, timedelta
import pickle
import numpy as np
from cycler import cycler
import requests

github_user = "<YOUR_GITHUB_USER>"
access_token = "<YOUR_PERSONAL_ACCESS_TOKEN>"

repos_ruby = ["rails/rails",
              "sinatra/sinatra"]
repos_python = ["django/django",
                "pallets/flask",
                "tornadoweb/tornado",
                "channelcat/sanic",
                "bottlepy/bottle",
                "plotly/dash",
                "Pylons/pyramid",
                "web2py/web2py"]
repos_php = ["laravel/laravel",
             "symfony/symfony",
             "bcit-ci/CodeIgniter",
             "yiisoft/yii2",
             "phalcon/cphalcon",
             "slimphp/Slim",
             "cakephp/cakephp",
             "zendframework/zendframework",
             "bcosca/fatfree",
             "fuel/fuel",
             "WordPress/WordPress"]
repos_node = ["expressjs/express",
              "nestjs/nest",
              "fastify/fastify",
              "meteor/meteor",
              # "zeit/next.js", // not really a framework?
              "koajs/koa",
              "balderdashy/sails",
              "keystonejs/keystone",
              "linnovate/mean",
              "strongloop/loopback",
              "hapijs/hapi",
              "prerender/prerender"]
repos_go = ["gin-gonic/gin",
            "labstack/echo",
            "kataras/iris",
            "astaxie/beego",
            "revel/revel",
            "go-chi/chi",
            "gobuffalo/buffalo"]
repos_java = ["spring-projects/spring-boot",
              "perwendel/spark",
              "apache/tomcat",
              "eclipse/jetty.project",
              "spring-projects/spring-framework"]
repos_scala = ["playframework/playframework"]
repos_clojure = ["duct-framework/duct"]
repos_kotlin = ["ktorio/ktor",
                "perwendel/spark-kotlin"]
repos_rust = ["SergioBenitez/Rocket",
              "actix/actix-web",
              "iron/iron",
              "seanmonstar/warp",
              "http-rs/tide",
              "carllerche/tower-web",
              "nickel-org/nickel.rs",
              "gotham-rs/gotham",
              "tomaka/rouille",
              "fengsp/pencil",
              "rustless/rustless"]

repos_wasm = [
  "perlin-network/life", # Go
  "bytecodealliance/lucet", # Rust
  "wasm3/wasm3", # C
  "wasmerio/wasmer", # Rust?
  "paritytech/wasmi", # Rust
  "bytecodealliance/wasmtime",
  "WAVM/WAVM", # C++
  "bytecodealliance/wasm-micro-runtime", # C
]

repos_baas = [
  "rethinkdb/rethinkdb",
  "mongodb/mongo",
  "supabase/supabase",
  "supabase/realtime",
  "ionic-team/ionic",
  "parse-community/parse-server",
  "rethinkdb/horizon",
  "hoodiehq/hoodie",
  "kuzzleio/kuzzle",
  "appwrite/appwrite",
]

repos_top = (repos_ruby[0:1] + repos_python[0:2] + repos_php[0:1] +
             repos_node[0:3] + repos_go[0:3] + repos_java[0:1] +
             repos_rust[0:2])

repos_all = (repos_ruby + repos_python + repos_php + repos_node + repos_go +
             repos_java + repos_scala + repos_clojure + repos_kotlin +
             repos_rust)

all_stars = {}
growth = []

for repo in repos_top:
    page_number = 1
    stars_remaining = True
    stargazers = {}
    num_stargazers = 0

    print("Getting stargazers for", repo)

    pickle_name = './stargazers/pickles/' + repo.split("/")[1] + '.pickle'
    try:
      f = open(pickle_name, 'rb')
      print('Load ' + pickle_name)
      stargazers = pickle.load(f)
      page_number = max(stargazers.keys())
    except IOError:
      pass

    while stars_remaining:
      query_url = "https://api.github.com/repos/%s/stargazers?page=%s&per_page=100" % (repo, page_number)
      headers = {'Accept': 'application/vnd.github.v3.star+json', 'User-Agent': github_user}
      response = requests.get(query_url, auth=(github_user, access_token), headers=headers)
      if response.status_code == 422:
          # We get a 422 when repos have more than 40k stars
          query_url = "https://api.github.com/repos/%s" % (repo)
          response = requests.get(query_url, auth=(github_user, access_token), headers=headers)
          data = response.json()
          num_stargazers = data['stargazers_count']
          break
      elif response.status_code != 200:
          print(response.status_code)
          print(response.text)

      data = response.json()

      page_stargazers = []
      for user in data:
        username = user['user']['login']
        star_time = datetime.datetime.strptime(user['starred_at'],'%Y-%m-%dT%H:%M:%SZ')

        page_stargazers.append((username, star_time))

      stargazers[page_number] = page_stargazers

      if page_number % 50 == 0:
        # save every 50 pages
        f = open(pickle_name, 'wb')
        pickle.dump(stargazers, f)
        print('Saved ' + pickle_name + ' with ' + str(page_number) + ' pages')

      if len(data) < 100:
        stars_remaining = False

      page_number += 1

    # save
    f = open(pickle_name, 'wb')
    pickle.dump(stargazers, f)
    if num_stargazers > 0:
      print("- There are more than 40k stars: saving count")
      pickle_name = './stargazers/' + repo.split("/")[1] + '.pickle'
      stars = {}
      try:
        f = open(pickle_name, 'rb')
        print('- Load ' + pickle_name)
        stars = pickle.load(f)
      except IOError:
        pass
      stars[date.today()] = num_stargazers
      f = open(pickle_name, 'wb')
      pickle.dump(stars, f)

    print("Done getting stargazers for", repo)

    starred_month = {}
    max_date = date(2000, 1,1)
    for stargazer_page in stargazers.values():
      for (_,t) in stargazer_page:
        dt = date(t.year, t.month, t.day)
        if dt > max_date:
          max_date = dt
        d = date(t.year, t.month, 1)
        try:
          starred_month[d] += 1
        except KeyError:
          starred_month[d] = 1

    if num_stargazers > 0:
      tot_stars = sum(starred_month.values()) # should be 40k
      for s in sorted(stars.keys()):
          diff_stars = stars[s] - tot_stars
          diff_days = (s - max_date).days
          if diff_days > 0:
              stars_per_day = diff_stars/diff_days
              for nd in range(1, diff_days+1):
                  t = max_date + timedelta(days=nd)
                  d = date(t.year, t.month, 1)
                  try:
                    starred_month[d] += stars_per_day
                  except KeyError:
                    starred_month[d] = stars_per_day
          # move to next date
          tot_stars = stars[s]
          max_date = s

    start = min(starred_month.keys())
    end = date.today()
    month_list = []
    for y in range(start.year, end.year + 1):
      for m in range(1, 13):
        if y == start.year and m < start.month:
          pass
        if y == end.year and m == end.month:
          break
        month_list.append(date(y, m, 1))

    starred_list = []
    for d in month_list:
      if d in starred_month:
        starred_list.append(starred_month[d])
      else:
        starred_list.append(0)

    all_stars[repo] = (month_list, starred_list)

    growth.append((repo, sum(starred_list[-3:]), sum(starred_list[:-3])))

plt.rc('axes', prop_cycle=(
    cycler('color', ['r', 'g', 'b', 'y', 'c', 'k']*4) +
    cycler('linestyle', ['-']*6 + ['--']*6 + [':']*6 + ['-.']*6)))

# Plot monthly stars
leg = all_stars.keys()
for repo in leg:
    plt.figure(1)
    plt.plot(all_stars[repo][0], np.cumsum(all_stars[repo][1]))
    plt.figure(2)
    plt.plot(all_stars[repo][0], all_stars[repo][1])

plt.figure(1)
plt.legend(leg)
plt.figure(2)
plt.legend(leg)

# Plot growth
growth.sort(key=lambda x: -x[1])
x = range(1, len(growth)+1)
lables = [l for (l, _, _) in growth]
grow = [g for (_, g, _) in growth]
tot = [t for (_, _, t) in growth]

fig, ax = plt.subplots()
ax.bar(x, grow)
ax.bar(x, tot, bottom=grow)
ax.set_yscale("log", nonposy='clip')
ax.set_ylim([1,max(tot)*2])
plt.xticks(x, lables, rotation='vertical')
plt.subplots_adjust(bottom=0.3)
plt.legend(['Stars added in last 3 month', 'Stars added before'])

plt.show()
