#! /bin/python

# This script plots the stars over time and the star growth rate of a GitHub
# repository.
# This is useful to assess the popularity of a repository.
#
# Note: getting the stargazers takes a ton of time (hours). The script will
# save all stargazers that it already retreived and only get the missing ones.

import json
import csv
from urllib.request import Request, urlopen
import datetime
import time
from matplotlib import pyplot as plt
from datetime import date
import pickle
import numpy as np
from cycler import cycler

access_token = "<YOUR_PERSONAL_ACCESS_TOKEN>"

repos_ruby = ["rails/rails",
              "sinatra/sinatra"]
repos_python = ["django/django",
                "pallets/flask"]
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
              "meteor/meteor",
              "koajs/koa",
              "balderdashy/sails",
              "keystonejs/keystone",
              "linnovate/mean",
              "strongloop/loopback",
              "fastify/fastify",
              "nestjs/nest"]
repos_go = ["gin-gonic/gin",
            "astaxie/beego",
            "revel/revel",
            "labstack/echo",
            "kataras/iris",
            "gobuffalo/buffalo"]
repos_java = ["spring-projects/spring-boot",
              "perwendel/spark",
              "apache/tomcat",
              "eclipse/jetty.project",
              "spring-projects/spring-framework"]
repos_scala = ["playframework/playframework"]
repos_clojure = ["duct-framework/duct"]
repos_kotlin = ["ktorio/ktor"]
repos_rust = ["SergioBenitez/Rocket",
              "iron/iron",
              "nickel-org/nickel.rs",
              "gotham-rs/gotham",
              "tomaka/rouille"]

repos_top = (repos_ruby[0:1] + repos_python[0:2] + repos_php[0:1] +
             repos_node[0:1] + repos_go[0:1] + repos_java[0:1] +
             repos_rust[0:1])

repos_all = (repos_ruby + repos_python + repos_php + repos_node + repos_go +
             repos_java + repos_scala + repos_clojure + repos_kotlin +
             repos_rust)

all_stars = {}
growth = []

for repo in repos_top:
    page_number = 1
    stars_remaining = True
    stargazers = {}

    print("Getting stargazers for", repo)

    pickle_name = './pickles/' + repo.split("/")[1] + '.pickle'
    try:
      f = open(pickle_name, 'rb')
      print('Load ' + pickle_name)
      stargazers = pickle.load(f)
      page_number = max(stargazers.keys())
    except IOError:
      pass

    while stars_remaining:
      query_url = "https://api.github.com/repos/%s/stargazers?page=%s&access_token=%s" % (repo, page_number, access_token)

      req = Request(query_url)
      req.add_header('Accept', 'application/vnd.github.v3.star+json')
      response = urlopen(req)

      data = json.loads(response.read())

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

      if len(data) < 30:
        stars_remaining = False

      page_number += 1

    # save
    f = open(pickle_name, 'wb')
    pickle.dump(stargazers, f)

    print("Done getting stargazers for", repo)

    starred_month = {}
    for stargazer_page in stargazers.values():
      for (_,t) in stargazer_page:
        d = date(t.year, t.month, 1)
        try:
          starred_month[d] += 1
        except KeyError:
          starred_month[d] = 1

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
plt.xticks(x, lables, rotation='vertical')
plt.subplots_adjust(bottom=0.3)
plt.legend(['Stars added in last 3 month', 'Stars added before'])

plt.show()
