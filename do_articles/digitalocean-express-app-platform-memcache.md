# How To Deploy an Express Application and Scale with MemCachier on DigitalOcean App Platform

*The author selected the [Free and Open Source Fund](https://www.brightfunds.org/funds/foss-nonprofits) to receive a donation as part of the [Write for DOnations](https://do.co/w4do-cta) program.*

### Introduction

[Express](https://expressjs.com/) is a popular framework for building fast web apps and APIs with [Node](https://nodejs.org/en/). DigitalOcean’s [App Platform](https://www.digitalocean.com/products/app-platform) is a [Platform as a Service (PaaS)](https://www.digitalocean.com/community/tutorials/what-is-platform-as-a-service-paas) product to configure and deploy applications from a code repository. It offers a quick and efficient way to deploy your Express app. In this tutorial, you'll deploy an Express application to DigitalOcean App Platform and then scale it by adding caching with the [DigitalOcean Marketplace Add-On for MemCachier](https://marketplace.digitalocean.com/add-ons/memcachier). MemCachier is compliant with the [memcached object caching system](https://memcached.org/) but has several advantages, such as better failure scenarios with high availability clusters.

You'll first build an Express app that calculates a prime number, has a **Like** button, and uses a template engine. Those features will enable you to implement several caching strategies later. You'll then push your app's code to GitHub and deploy it on App Platform. Finally, you'll implement three object caching techniques to make your app faster and more scalable. By the end of this tutorial, you'll be able to deploy an Express application to App Platform, implementing techniques for caching resource-intensive computations, rendered views, and sessions.

## Prerequisites

- Node.js installed on your machine, which you can setup with [How To Install Node.js on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-22-04). On other operating systems, follow the appropriate guide on [How To Install Node.js and Create a Local Development Environment](https://www.digitalocean.com/community/tutorial_series/how-to-install-node-js-and-create-a-local-development-environment).
- A basic Express server with Node.js. Follow Steps 1-2 in our tutorial on [How To Get Started with Node.js and Express](https://www.digitalocean.com/community/tutorials/nodejs-express-basics).
- A [GitHub account](https://github.com/) and [Git installed](https://github.com/git-guides/install-git) on your local machine. These are necessary as you'll push the code to GitHub to deploy from DigitalOcean App Platform. You can follow our tutorial on [How To Install Git](https://www.digitalocean.com/community/tutorial_collections/how-to-install-git) to get set up.
- A [DigitalOcean account](https://cloud.digitalocean.com/registrations/new) for deploying to [App Platform](https://www.digitalocean.com/products/app-platform/). Running this app on App Platform will incur a charge. See [App Platform Pricing](https://docs.digitalocean.com/products/app-platform/details/pricing/) for details.
- A web browser like [Firefox](https://www.mozilla.org/en-US/firefox/new/) or [Chrome](https://www.google.com/chrome/).
- An understanding of [Express template engines](https://www.digitalocean.com/community/tutorials/nodejs-express-template-engines).
- An understanding of Express middleware. You can read more about this topic in our tutorial, [How To Create a Custom Middleware in Express.js](https://www.digitalocean.com/community/tutorials/nodejs-creating-your-own-express-middleware).

## Step 1 — Setting Up an Express Template Rendered View

In this step, you'll install a [template engine for Express](http://expressjs.com/en/guide/using-template-engines.html#using-template-engines-with-express), create a template for your app's home route (`GET /`), and update the route to use that template. A template engine enables you to cache rendered views later, increasing the speed of request handling and decreasing resource use.

To start, navigate to the project directory of the Express server with your editor if it is not already open. You can return to the prerequisite tutorial on [How To Get Started with Node.js and Express](https://www.digitalocean.com/community/tutorials/nodejs-express-basics) to identify where you have saved your project files.

You will install a template engine for Express to use static template files in your application. A template engine replaces variables in a template file with values and transforms the template into an HTML file, which is sent as the response to a request. Using templates makes it easier to work with HTML.

Install the [Embedded JavaScript templates (`ejs`)](https://github.com/mde/ejs) library. If you prefer, you could use one of the other [template engines that Express supports](https://expressjs.com/en/resources/template-engines.html), like Mustache, Pug, or Nunjucks.

```command
npm install ejs
```

With `ejs` now installed, you will configure your Express app to use it.

Open the file `server.js` in your editor. Then, add the highlighted line:

```js
[label server.js]
const express = require('express');

const app = express();

<^>app.set('view engine', 'ejs');<^>

app.get('/', (req, res) => {
  res.send('Successful response.');
});

...
```

This line sets the [application setting property](https://expressjs.com/en/4x/api.html#app.settings.table) `view engine` to `ejs`.

Save the file.

<$>[note]
**Note:** For this tutorial, you will use the `view engine` setting, but another useful setting is `views`. The `views` setting tells an Express app where to find template files. The default value is `./views`.
<$>

Next, create a `views` directory. Then, create the file `views/index.ejs` and open it in your editor.

Add the starting template markup to that file:

```ejs
[label views/index.ejs]
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Find the largest prime number</title>
  </head>
  <body>
    <h1>Find the largest prime number</h1>

    <p>
      For any number N, find the largest prime number less than or equal to N.
    </p>
  </body>
</html>
```

Save the file.

With the template created, you will update your route to use it.

Open the file `server.js` and update the highlighted code:

```js
[label server.js]
...

app.get('/', (req, res) => {
  <^>res.render('index');<^>
});

...
```

The response `render` method takes the name of a template as its first parameter. In this case, `index` matches the file `views/<^>index<^>.ejs`.

Restart your app to load the changes. Stop the server if it's running by pressing `CTRL+C` in your terminal. Then start the server again:

```command
node server.js
```

Visit `localhost:3000` in your web browser, which will now display the contents of your template.

![Your rendered template with a heading and paragraph](https://deved-images.nyc3.digitaloceanspaces.com/CART-68717/FRhjviO.png)

Your app now has a template-rendered view, but it doesn't do anything yet. You'll add functionality to find a prime number next.

## Step 2 — Adding Functionality to Your Express App

In this step, you'll add the features to find a prime number and to like numbers using a **Like** button. You'll use these features to interact with the app once you have deployed to App Platform in [Step 4](https://www.digitalocean.com/community/tutorials/how-to-deploy-an-express-application-and-scale-with-memcached-on-digitalocean-app-platform#step-4-deploying-on-app-platform).

### Finding a Prime Number

In this section, you'll add a function to your app that finds the largest prime number less than or equal to `N`, where `N` refers to any number.

`N` will be submitted via a form with the `GET` method to the home route (`/`), with `N` appended as a query parameter: `localhost:3000/?n=<^>10<^>` (where `<^>10<^>` is a sample query). The home route can have multiple URLs that produce rendered views, which can each be cached individually.

In `views/index.ejs`, add a form with an input element for entering `N`:

```ejs
[label views/index.ejs]
...

<p>
  For any number N, find the largest prime number less than or equal to N.
</p>

<^><form action="/" method="get"><^>
  <^><label><^>
    <^>N<^>
    <^><input type="number" name="n" placeholder="e.g. 10" required><^>
  <^></label><^>
  <^><button>Find Prime</button><^>
<^></form><^>

...
```

The form's action submits to `/`, which is handled by the home route `app.get('/' ...)` in `server.js`. As the form's method is set to `get`, the data `n` will be appended to the action URL as a query parameter.

Save the file.

Next, when a request is made with a query parameter of `n`, you'll pass that data to the template.

In `server.js`, add the highlighted code:

```js
[label server.js]
...

app.get('/', (req, res) => {
  <^>const n = req.query.n;<^>
  
  <^>if (!n) {<^>
    res.render('index');
    <^>return;<^>
  <^>}<^>
  
  <^>const locals = { n };<^>
  <^>res.render('index', locals);<^>
});

...
```

These lines will check if the request has a query parameter named `n`. If so, you render the `index` view and pass the value of `n` to it. Otherwise, you generate the `index` view without data.

<$>[note]
**Note:** User input cannot always be trusted, so the best practice for a production-ready app would be to validate the input with a library such as [Joi](https://joi.dev/api).
<$>

The `render` method has a second optional parameter, `locals`. This parameter defines local variables passed to a template to render a view. A shorthand property name defines the `n` property of the `locals` object. When a variable has the same name as the object property it's being assigned to, the variable name can be omitted. So `{ n: n }` can be written as `{ n }`.

Save the file.

Now that the template has some data, you can display it.

In `views/index.ejs`, add the highlighted lines to display the value of `N`:

```ejs
[label views/index.ejs]
...

<form action="/" method="get">
  <label>
    N
    <input type="number" name="n" placeholder="e.g. 10" required>
  </label>
  <button>Find Prime</button>
</form>

<^><% if (locals.n) { %><^>
  <^><p>N: <%= n %></p><^>
<^><% } %><^>

...
```

If a local variable `n` exists for this view, you tell the app to display it.

Save the file, then restart your server to refresh the app. The form will now load with a button to **Find Prime**. The app will be able to accept user input and display it under the form.

![Your rendered template now with a form to find a prime number](https://deved-images.nyc3.digitaloceanspaces.com/CART-68717/b28fUGz.png)

Submit any number to the form. After submitting the form, the URL will change to include an `n` query parameter, such as `http://localhost:3000/?n=<^>40<^>` if you put in `<^>40<^>`. The value you submitted will also load under the form as **N: <^>40<^>**.

![Your rendered template now showing the number submitted below the form](https://deved-images.nyc3.digitaloceanspaces.com/CART-68717/YV64Q98.png)

Now that a value for `N` can be submitted and displayed, you'll add a function to find the largest prime number less than or equal to `N`. Then, you'll display that result in your view.

Create a `utils` directory. Then, create the file `utils/findPrime.js`.

Open `findPrime.js` in your editor and add the prime number finding function:

```js
[label utils/findPrime.js]
/**
 * Find the largest prime number less than or equal to `n`
 * @param {number} n A positive integer greater than the smallest prime number, 2
 * @returns {number}
 */
module.exports = function (n) {
  let prime = 2; // initialize with the smallest prime number
  for (let i = n; i > 1; i--) {
    let isPrime = true;
    for (let j = 2; j < i; j++) {
      if (i % j == 0) {
        isPrime = false;
        break;
      }
    }
    if (isPrime) {
      prime = i;
      break;
    }
  }
  return prime;
};
```

A [JSDoc](https://jsdoc.app/) comment documents the function. The algorithm starts with the first prime number (`2`), then loops through numbers, starting at `n` and decrementing the number by `1` in each loop. The function will continue looping and searching for a prime number until the number is `2`, the smallest prime number.

Each loop assumes the current number is a prime number, then tests that assumption. It will check if the current number has a factor other than `1` and itself. If the current number can be divided by any number greater than `1` and less than itself without a remainder, then it is not a prime number. The function will then try the next number.

Save the file.

Next, import the find prime function into `server.js`:

```js
[label server.js]
const express = require('express');
<^>const findPrime = require('./utils/findPrime');<^>

...
```

Update your home route controller to find a prime number and pass its value to the template. Still in `server.js`, add the highlighted code:

```js
[label server.js]
...

app.get('/', (req, res) => {
  const n = req.query.n;

  if (!n) {
    res.render('index');
    return;
  }
  
  <^>const prime = findPrime(n);<^>

  const locals = { n<^>, prime<^> };
  res.render('index', locals);
});

...
```

Save the file.

Now, you will add code to display the result in your template. In `views/index.ejs`, display the value of `N`:

```ejs
[label views/index.ejs]
...

<form action="/" method="get">
  <label>
    N
    <input type="number" name="n" placeholder="e.g. 10" required>
  </label>
  <button>Find Prime</button>
</form>

<% if (locals.n<^> && locals.prime<^>) { %>
  <^><p><^>
    <^>The largest prime number less than or equal to <%= n %> is <strong><%= prime %></strong>.<^>
  <^></p><^>
<% } %>
...
```

Save the file.

Now restart the server.

To test the functionality, submit any number. As an example, this tutorial will use `<^>10<^>`. If you submit the number `<^>10<^>`, you will receive a response stating, `The largest prime number less than or equal to <^>10<^> is <^>7<^>.`.

Your app can now take a number, then find and display a prime number. Next, you'll add a **Like** button.

### Adding a Like Button

Currently, your app can produce different views based on each number `N` submitted. Apart from updating text, the content of those views is likely to stay the same. The **Like** button you'll add in this section will provide a way to update the content of a view. This button demonstrates the need for invalidating a cached view when its contents change, which will be beneficial when caching rendered views later in the tutorial.

With a **Like** button, the app needs somewhere to store the like data. While persistent storage is ideal, you will store likes in memory because implementing a database is beyond the scope of this tutorial. As such, the data will be ephemeral, which means all data will be lost when the server stops.

Open `server.js` to add the following variable:

```js
[label server.js]
...

app.set('view engine', 'ejs');

<^>/**<^>
<^> * Key is `n`<^>
<^> * Value is the number of 'likes' for `n`<^>
<^> */<^>
<^>const likesMap = {};<^>

...
```

The `likesMap` object is used as a map to store likes for all requested numbers. The key is `n`, and its values are the number of likes for `n`.

Likes for a number need to be initialized when a number is submitted. Still in the `server.js`, add the highlighted lines to initialize likes for `N`:

```js
[label server.js]
...

  const prime = findPrime(n);

  <^>// Initialize likes for this number when necessary<^>
  <^>if (!likesMap[n]) likesMap[n] = 0;<^>

  const locals = { n, prime };
  res.render('index', locals);

...
```

This `if` statement checks if likes for the current number exist. If no likes are present, then the `likesMaps` number initializes to `0`.

Next, add likes as a local variable for the view:

```js
[label server.js]
...

  const prime = findPrime(n);

  // Initialize likes for this number when necessary
  if (!likesMap[n]) likesMap[n] = 0;

  const locals = { n, prime<^>, likes: likesMap[n]<^> };
  res.render('index', locals);

...
```

Save the file.

Now that the view has data for likes, you can display its value and add a **Like** button.

In `views/index.ejs`, add the **Like** button markup:

```ejs
[label views/index.ejs]
...

<% if (locals.n && locals.prime) { %>
  <p>
    The largest prime number less than or equal to <%= n %> is <strong><%= prime %></strong>.
  </p>

  <^><form action="/like" method="get"><^>
    <^><input type="hidden" name="n" value="<%= n %>"><^>
    <^><input type="submit" value="Like"> <%= likes %><^>
  <^></form><^>
<% } %>
...
```

Your completed file should now match the following:

```ejs
[label views/index.ejs]
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Find the largest prime number</title>
  </head>
  <body>
    <h1>Find the largest prime number</h1>

    <p>
      For any number N, find the largest prime number less than or equal to N.
    </p>

    <form action="/" method="get">
      <label>
        N
        <input type="number" name="n" placeholder="e.g. 10" required>
      </label>
      <button>Find Prime</button>
    </form>

    <% if (locals.n && locals.prime) { %>
      <p>
        The largest prime number less than or equal to <%= n %> is <strong><%= prime %></strong>.
      </p>
      <form action="/like" method="get">
        <input type="hidden" name="n" value="<%= n %>">
        <input type="submit" value="Like"> <%= likes %>
      </form>
    <% } %>
  </body>
</html>
```

Save the file.

Restart the server, then submit a number. A **Like** button will appear after the prime number result with a like count of `0`.

![A screencapture of the page with a box around the newly added Like button](https://deved-images.nyc3.digitaloceanspaces.com/CART-68717/likebutton.png)

Clicking the **Like** button sends a `GET` request to `/like`, with the current value of `N` as a query parameter via a hidden input. For now, you'll receive a 404 error with **Cannot GET /like**, because your app does not yet have a corresponding route.

You'll now add the route to handle the request.

Back in `server.js`, add the route:

```js
[label server.js]
...

app.get('/', (req, res) => {
  ...
});

<^>app.get('/like', (req, res) => {<^>
  <^>const n = req.query.n;<^>

  <^>if (!n) {<^>
    <^>res.redirect('/');<^>
    <^>return;<^>
  <^>}<^>

  <^>likesMap[n]++;<^>

  <^>res.redirect(`/?n=${n}`);<^>
<^>});<^>

...
```

This new route checks if `n` exists. If not, it redirects home. Otherwise, it increments likes for this number. Finally, it redirects to the view where the **Like** button was clicked.

Your completed file should now match the following:

```js
[label server.js]
const express = require('express');
const findPrime = require('./utils/findPrime');

const app = express();

app.set('view engine', 'ejs');

/**
 * Key is `n`
 * Value is the number of 'likes' for `n`
 */
const likesMap = {};

app.get('/', (req, res) => {
  const n = req.query.n;
  
  if (!n) {
    res.render('index');
    return;
  }
  
  const prime = findPrime(n);

  // Initialize likes for this number when necessary
  if (!likesMap[n]) likesMap[n] = 0;

  const locals = { n, prime, likes: likesMap[n] };
  res.render('index', locals);
});

app.get('/like', (req, res) => {
  const n = req.query.n;

  if (!n) {
    res.redirect('/');
    return;
  }

  likesMap[n]++;

  res.redirect(`/?n=${n}`);
});

const port = process.env.PORT || 3000;
app.listen(port, () =>
  console.log(`Example app is listening on port ${port}.`)
);

```

Save the file.

Restart the app and test the **Like** button again. The likes count will increment for each click.

<$>[note]
**Note:** You could also use the `POST` method instead of `GET` for this route. It would be more [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) because an update is made to a resource. This tutorial uses `GET` rather than introducing form `POST` request body handling so that you can work with the now familiar request query parameters.
<$>

Your app is now complete with fully functioning features, so you can prepare to deploy it to App Platform. In the next step, you'll commit the app's code with `git` and push that code to GitHub.

## Step 3 — Creating Your Code Repository

In this step, you will create a code repository to hold all the files for your deployment. First, you will commit your code to git, and then you will push it to a GitHub repository. You will use this repository to deploy with App Platform.

### Committing Your Code to Git

In this section, you'll commit your code to git, so it's ready to push to GitHub.

<$>[note]
**Note:** If you have not configured your settings with your username, be sure to [set up Git](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-20-04#setting-up-git) and authenticate your GitHub account with SSH.
<$>

First, initialize a `git` repository:

```command
git init
```

Next, tell Git to exclude your app's dependencies. Create a new file called `.gitignore` and add the following:

```text
[label .gitignore]
node_modules

# macOS file
.DS_Store
```
<$>[note]
**Note:** The `.DS_Store` line is specific to macOS and does not need to be present for other operating systems.
<$>

Save and close the file.

Now, add all files to git:

```command
git add .
```

Finally, commit those changes with the following command:

```command
git commit -m "<^>Initial commit<^>"
```

The `-m` option is used to specify the commit message, which you can update with whatever message you wish.

After committing your code, you'll receive an output like so:

```
[secondary_label Output]
[main (root-commit) deab84e] Initial commit
 6 files changed, 1259 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 package-lock.json
 create mode 100644 package.json
 create mode 100644 server.js
 create mode 100644 utils/findPrime.js
 create mode 100644 views/index.ejs
```

You have committed your code to git. Next, you'll push it to GitHub.

### Pushing Your Code to a GitHub Repository

Now that your app's code is committed to git, you're ready to push it to GitHub. You can then connect the code with DigitalOcean App Platform and deploy it.

First, in your browser, log in to GitHub and [create a new repository](https://github.com/new) called `express-memcache`. Create an empty repository without `README`, `.gitignore`, or license files. You can make the repository either private or public. You can also review [GitHub's documentation on creating a new repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository).

Back in your terminal, add your newly created repository as a remote origin, updating your username:

```command
git remote add origin https://github.com/<^>your_username<^>/express-memcache.git
```

This command tells Git where to push your code.

Next, rename the default branch `main`:

```command
git branch -M main
```

Finally, push the code to your repository:

```command
git push -u origin main
```

Enter your credentials if prompted.

You'll receive output similar to the following:

```
[secondary_label Output]
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 8 threads
Compressing objects: 100% (7/7), done.
Writing objects: 100% (10/10), 9.50 KiB | 9.50 MiB/s, done.
Total 10 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/<^>your_username<^>/express-memcache.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

Your app's code is now on GitHub, ready to be deployed by App Platform.

## Step 4 — Deploying on App Platform

In this step, you'll deploy your Express app to [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform). You'll create an App Platform app, permit it to access your GitHub repository, and then deploy it.

You'll start by updating the environment settings so that your configuration can be read from the `PORT` environment label.

### Updating Your App's Environment Settings

In this section, you'll expand your Express server to allow the app's port configuration to be read from an environment variable. Because the configuration will likely change between deploys, this update will enable your app to read the port from its App Platform environment.

Open the file `server.js` in your editor. Then, at the bottom of the file, update the highlighted code to replace the existing `app.listen` line and add a new `const port` line:

```js
[label server.js]
...

<^>const port = process.env.PORT || 3000;<^>
app.listen(<^>port<^>, () =>
  <^>console.log(`Example app is listening on port ${port}.`)<^>
<^>);<^>
```

This code indicates to use a `PORT` environment variable if it exists or default to port `3000` otherwise.

Your app will now be able to read the port from the App Platform environment to which you will now deploy it.

### Creating and Deploying Your App on App Platform

You can now set up your app with App Platform.

<$>[info]
You will incur charges for running this app on App Platform, with web services billed by the second (starting at a minimum of one minute). Pricing is displayed on the **Review** screen. See [App Platform Pricing](https://docs.digitalocean.com/products/app-platform/details/pricing/) for details.
<$>

First, log in to your DigitalOcean account. From the [Apps](https://cloud.digitalocean.com/apps/) dashboard, click **Create**, then **Apps**. You can also follow our [product documentation on How to Create Apps in App Platform](https://docs.digitalocean.com/products/app-platform/how-to/create-apps/).

On the **Create Resource From Source Code** screen, select **GitHub** as the **Service Provider**. Then, give DigitalOcean permission to access your repository. The best practice is to select only the repository that you want deployed. If you haven't done so, you'll be prompted to install the DigitalOcean GitHub app. Select your repository from the list and click **Next**.

On the **Resources** screen, click **Edit Plan** to select your plan size. This tutorial will use the **Basic Plan** with the smallest size **Web Services** (**512 MB RAM | 1 vCPU**) for the **express-memcache** resource. The Basic Plan and smallest web service offer enough resources for this sample Express app. Once you have set your plan, click **Back**.

Next, click the **Info** tab on the left navigation bar and note the region your app is in. You'll need this in the next step when you add a DigitalOcean Marketplace Add-On for [MemCachier](https://marketplace.digitalocean.com/add-ons/memcachier).

Finally, click on the **Review** tab, then click the **Create Resources** button to build and deploy your app. It will take a little while for the build to run. When it is finished, you will receive a success message with a link to your deployed app.

So far, you have created an Express app that finds a prime number and has a **Like** button. You committed the app's code to Git and pushed it to GitHub, and then you deployed the app on App Platform.

To make your Express app faster and more scalable, you will implement three object caching strategies. You need a cache, which you'll create in the next step.

## Step 5 — Configuring an Object Cache with MemCachier

In this step, you'll create and configure an object cache. Any [memcached](https://memcached.org/)-compatible cache will work for this tutorial. You will provision one with the [MemCachier Add-On](https://marketplace.digitalocean.com/add-ons/memcachier) from the DigitalOcean Marketplace. A MemCachier cache is an in-memory key-value store.

First, you'll add the MemCachier Add-On from the DigitalOcean Marketplace. Visit the [MemCachier Add-On page](https://marketplace.digitalocean.com/add-ons/memcachier) and click **Add MemCachier**. On the next screen, select the region your App Platform app is in, which you noted earlier. Your app and cache should be in the same region so that latency is as low as possible. You can view your App Platform app's settings if you need to find the region again. You can optionally select a plan. Then, click **Add MemCachier** to provision your cache.

<$>[info]
To figure out region name-to-slug mappings, see DigitalOcean's [Available Datacenters](https://docs.digitalocean.com/products/platform/availability-matrix/#available-datacenters). For example, the region **San Francisco** maps to **sfo3**.
<$>

Next, you'll configure your Express app to use the cache. Visit the [Add-Ons dashboard](https://cloud.digitalocean.com/add-ons/), then click the name of your MemCachier Add-On to open its dashboard. On the MemCachier Add-On dashboard, click the **Show** button for **Configuration Variables** to load a display with the values for `MEMCACHIER_USERNAME`, `MEMCACHIER_PASSWORD`, and `MEMCACHIER_SERVERS`. Take note of these values because you will need them next.

![Screencapture of redacted values for configuration variables in the Add-Ons dashboard](https://deved-images.nyc3.digitaloceanspaces.com/CART-68717/shown.png)

You'll now save your MemCachier configuration variables as environment variables for your app. Go back to your App Platform app's dashboard and click **Settings**. Then, under **Components**, click **express-memc...**. Scroll to the **Environment Variables** section, click **Edit**, and then add your MemCachier configuration variables with the three keys (`MEMCACHIER_USERNAME`, `MEMCACHIER_PASSWORD` and `MEMCACHIER_SERVERS`) and the corresponding values you got from the MemCachier dashboard. For `MEMCACHIER_PASSWORD`, check **Encrypt** because the value is a password. Click **Save** to update the app.

![Screencapture of App Platform configuration window for environment variables](https://deved-images.nyc3.digitaloceanspaces.com/CART-68717/envar.png)

Now, you'll configure a memcache client in your Express app, using the environment variables you just saved so that the app can communicate with your cache.

In your terminal, install the [`memjs`](https://github.com/memcachier/memjs) library:

```command
npm install memjs
```

Next, create a `services` directory. Then, create the file `services/memcache.js` and open it in your editor. At the top of the file, import `memjs` and configure a cache client:

```js
[label services/memcache.js]
const { Client } = require('memjs');

module.exports = Client.create(process.env.MEMCACHIER_SERVERS, {
  failover: true,
  timeout: 1,
  keepAlive: true,
});
```

Save the file.

This code creates a MemCachier cache client. As for the options, `failover` is set to `true` to use MemCachier's high-availability clusters. If a server fails, commands for all keys stored on that server will automatically be made to the next available server. A `timeout` of `1` second is better for a deployed app than the default of `0.5` seconds. `keepAlive: true` keeps connections to your cache open even when idle, which is desirable because making connections is slow, and caches must be fast to be effective.

You provisioned a cache using the MemCachier Add-On from the DigitalOcean Marketplace in this step. You then added your cache's configuration settings as App Platform environment variables, enabling you to configure a client, using `memjs`, so your Express app can communicate with the cache.

Everything is ready to start implementing caching in Express, which you'll do next.

## Step 6 — Implementing Caching in Express with MemCachier

With your Express app deployed and your MemCachier Add-On provisioned, you can now use your object cache. In this step, you will implement three object caching techniques. You will begin by caching resource-intensive computation to improve usage speeds and efficiency. Then, you will implement techniques to cache rendered views after user input to improve request handling and to cache short-lived sessions in anticipation of scaling your app beyond this tutorial.

### Caching High-Resource Computations

In this section, you'll cache resource-intensive computations to speed up your app, which results in more efficient CPU use. The `findPrime` function is a resource-intensive computation, when a large enough number is submitted. You'll cache its result and serve that cached value when available instead of repeating the calculation.

First, open `server.js` to add the memcache client:

```js
[label server.js]
const express = require('express');
const findPrime = require('./utils/findPrime');
<^>const memcache = require('./services/memcache');<^>

...
```

Then, store a calculated prime number in the cache:

```js
[label server.js]
...

  const prime = findPrime(n);

  <^>const key = 'prime_' + n;<^>

  <^>memcache.set(key, prime.toString(), { expires: 0 }, (err) => {<^>
    <^>if (err) console.log(err);<^>
  <^>});<^>

...
```

Save the file.

The `set` method takes a key as its first parameter and a value of a string as its second, so you convert the `prime` number to a string. The third `options` argument ensures the stored item never expires. The fourth and final parameter is an optional callback, where an error is thrown if present.

<$>[note]
**Note:** As a best practice, cache errors should be handled gracefully. A cache is an enhancement and should generally not crash an app on failure. An app can work perfectly fine, albeit slower, without its cache.
<$>

<$>[note]
**Note:** At this point, your app will continue to work locally but without caching. An error will be output when `memcache.set` is called, because it will not be able to find a cache server:

```
[secondary_label Output]
MemJS: Server <localhost:11211> failed after (2) retries with error - connect ECONNREFUSED 127.0.0.1:11211
Error: No servers available
...
```

For the rest of this tutorial, you don't need local caching. If you want it to work, you could run memcached at `localhost:11211`, which is the `memjs` default.
<$>

Next, stage and commit your changes:

```command
git add . && git commit -m "<^>Add memjs client and cache prime number<^>"
```

Then, push these changes to GitHub, which should automatically deploy to App Platform:

```command
git push
```

Your App Platform dashboard will shift from the **Deployed** message to one that indicates your app is building. When the build is complete, open the app in your browser and submit a number to find its biggest prime.

<$>[note]
**Note:** Your dashboard may display a `Waiting for service` message. That message will typically resolve by itself. If it lingers, try refreshing your app to check if the build has deployed.
<$>

Next, return to the [Add-Ons dashboard](https://cloud.digitalocean.com/add-ons/), then click the **View MemCachier** option for your named service to view your cache's analytics dashboard.

![The MemCachier analytics dashboard](https://deved-images.nyc3.digitaloceanspaces.com/CART-68717/KhcUKJG.png)

On this dashboard, the **Set Cmds** option on the **All Time Stats** board and the **Items** stats on the **Storage** board have both increased by `1`. Each time you submit a number, **Set Cmds** and **Items** will both increase. You must press the **Refresh** button to load any new stats.

<$>[note]
**Note:** Checking your app's logs on App Platform can be valuable for debugging. From your app's dashboard, click **Runtime Logs** to view them.
<$>

With items stored in the cache, you can make use of them. You'll now check if an item is cached, and if so, you'll serve it from the cache; otherwise, you'll find the prime number as before.

Back in `server.js`, update your file with the highlighted lines. You will both modify existing lines and add new lines for the cache:

```js
[label server.js]
...

app.get('/', (req, res) => {
  const n = req.query.n;

  if (!n) {
    res.render('index');
    return;
  }

  <^>let prime;<^>

  const key = 'prime_' + n;

  <^>memcache.get(key, (err, val) => {<^>
    <^>if (err) console.log(err);<^>

    <^>if (val !== null) {<^>
      <^>// Use the value from the cache<^>
      <^>// Convert Buffer string before converting to number<^>
      <^>prime = parseInt(val.toString());<^>
    <^>} else {<^>
      <^>// No cached value available, find it<^>
      <^>prime = findPrime(n);<^>

      memcache.set(key, prime.toString(), { expires: 0 }, (err) => {
        if (err) console.log(err);
      });
    <^>}<^>

    // Initialize likes for this number when necessary
    if (!likesMap[n]) likesMap[n] = 0;

    const locals = { n, prime, likes: likesMap[n] };
    res.render('index', locals);
  <^>});<^>
});

...
```

Save the file.

This code initializes `prime` without a value, using the `let` keyword, as its value is now reassigned. Then `memcache.get` attempts to retrieve the cached prime number. Most of the controller's code now lives in the `memcache.get` callback because its result is required to determine how to handle the request. If a cached value is available, use it. Otherwise, do the computation to find the prime number and store the result in the cache as before.

The value returned in the `memcache.get` callback is a [`Buffer`](https://nodejs.org/api/buffer.html), so you convert it to a string before converting `prime` back into a number.

Commit your changes and push them to GitHub to deploy:

```command
git add . && git commit -m "<^>Check cache for prime number<^>" && git push
```

When you submit a number not yet cached to your app, the **Set Cmds**, **Items**, and **get misses** stats on your MemCachier dashboard will increase by `1`. The miss occurs because you try to get the item from the cache before setting it. The item is not in the cache, resulting in a miss, after which the item gets stored. When you submit a cached number, **get hits** will increment.

You are now caching resource-intensive computations. Next, you'll cache your app's rendered views.

### Caching Rendered Views

In this section, you'll cache the views rendered by your Express app with middleware. Earlier, you set up `ejs` as a template engine and created a template to render views for each number `N` submitted. Rendered views can be resource-intensive to create, so caching them can speed up request handling and use fewer resources.

To begin, create a `middleware` directory. Then, create the file `middleware/cacheView.js` and open it in your editor. In `cacheView.js`, add these lines for the middleware function:

```js
[label middleware/cacheView.js]
const memcache = require('../services/memcache');

/**
 * Express middleware to cache views and serve cached views
 */
module.exports = function (req, res, next) {
  const key = `view_${req.url}`;

  memcache.get(key, (err, val) => {
    if (err) console.log(err);

    if (val !== null) {
      // Convert Buffer string to send as the response body
      res.send(val.toString());
      return;
    }
  });
};
```

You first import the `memcache` client. Then, you declare a key, such as `view_/?<^>n=100<^>`. Next, you check if a view for that key is in the cache with `memcache.get`. If there is no error and a value exists for that key, there's nothing more to do, so the request finishes by sending the view back to the client.

Next, if a view is not cached, you want to cache it. To do this, override the `res.send` method by adding the highlighted lines:

```js
[label middleware/cacheView.js]
...

module.exports = function (req, res, next) {
  const key = `view_${req.url}`;

  memcache.get(key, (err, val) => {
    if (err) console.log(err);

    if (val !== null) {
      // Convert Buffer to UTF-8 string to send as the response body
      res.send(val.toString());
      return;
    }

    <^>const originalSend = res.send;<^>
    <^>res.send = function (body) {<^>
      <^>memcache.set(key, body, { expires: 0 }, (err) => {<^>
        <^>if (err) console.log(err);<^>
      <^>});<^>

      <^>originalSend.call(this, body);<^>
    <^>};<^>
  });
};
```

You override the `res.send` method with a function that stores the view in the cache before calling the original `send` function as usual. You invoke the original `send` function with `call`, which sets its `this` context to what it would have been if not overridden. Make sure to use an [anonymous function expression](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function#parameters) (not an [arrow function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions)), so the correct `this` value will be specified.

Then, pass control to the next middleware by adding the highlighted line:

```js
[label middleware/cacheView.js]
...

/**
 * Express middleware to cache views and serve cached views
 */
module.exports = function (req, res, next) {
  const key = `view_${req.url}`;

  memcache.get(key, (err, val) => {
    if (err) console.log(err);

    if (val !== null) {
      // Convert Buffer to UTF-8 string to send as the response body
      res.send(val.toString());
      return;
    }

    const originalSend = res.send;
    res.send = function (body) {
      memcache.set(key, body, { expires: 0 }, (err) => {
        if (err) console.log(err);
      });

      originalSend.call(this, body);
    };

    <^>next();<^>
  });
};

...
```

Calling `next` invokes the next middleware function in the app. In your case, there is no other middleware, so the controller is called. The `res.render` method for Express renders a view, then calls `res.send` internally with that rendered view. So now, in the controller for the home route, your override function is called when `res.render` is called, storing the view in the cache before finally calling the original `send` function to complete the response.

Save the file.

<$>[note]
**Note:** You can also pass a callback to the [`render`](https://expressjs.com/en/api.html#res.render) method in the controller, but you will have to duplicate the view caching code in the controller for each route being cached.
<$>

Now import the view caching middleware into `server.js`:

```js
[label server.js]
const express = require('express');
const findPrime = require('./utils/findPrime');
const memcache = require('./services/memcache');
<^>const cacheView = require('./middleware/cacheView');<^>

...
```

Add the highlighted code to use it with the `GET /` home route:

```js
[label server.js]
...

app.get('/'<^>, cacheView<^>, (req, res) => {
  ...
});

...
```

Save the file.

Then commit your changes and push them to GitHub to deploy:

```command
git add . && git commit -m "<^>Add view caching<^>" && git push
```

Everything should work as usual when you submit a number in your app. If you submit a new number, the MemCachier dashboard stats for **Set Cmds**, **Items**, and **get misses** all increase by two: once for the prime number calculation and once for the view. If you refresh the app with the same number, you'll see a single **get hit** added to the MemCachier dashboard. The view is retrieved successfully from the cache, so there is no need to fetch the prime number result.

<$>[note]
**Note:** The Express application setting `view cache` is enabled by default in production. This view cache does not cache the contents of the template’s output, only the underlying template itself. The view is re-rendered with every request, even when the cache is on. As such, it's different but complementary to the rendered view caching you implemented.
<$>

Now that you are caching views, you may notice that the **Like** button no longer works. If you were to log the `likes` value, the value will indeed change. However, the cached view still needs to be updated when the number of likes changes. A cached view needs to be invalidated when the view changes.

Next, when `likes` changes, you'll invalidate the cached view by deleting it from the cache. Back in `server.js`, update the `redirect` function and add the highlighted lines:

```js
[label server.js]
...

app.get('/like', (req, res) => {
  const n = req.query.n;

  if (!n) {
    res.redirect('/');
    return;
  }

  likesMap[n]++;

  <^>// The URL of the page being 'liked'<^>
  <^>const url = `/?n=${n}`;<^>

  res.redirect(<^>url<^>);
});

...
```

The likes count for this view has changed, so the cached version will be invalid. Add the highlighted lines to delete the likes count from the cache when `likes` change:

```js
[label server.js]
...
  const url = `/?n=${n}`;

  <^>// The view for this URL has changed, so the cached version is no longer valid, delete it from the cache.<^>
  <^>const key = `view_${url}`;<^>
  <^>memcache.delete(key, (err) => {<^>
    <^>if (err) console.log(err);<^>
  <^>});<^>

  res.redirect(url);
...
```

Your `server.js` file should now match the following:

```js
[label server.js]
const express = require('express');
const findPrime = require('./utils/findPrime');
const memcache = require('./services/memcache');
const cacheView = require('./middleware/cacheView');

const app = express();

app.set('view engine', 'ejs');

/**
 * Key is `n`
 * Value is the number of 'likes' for `n`
 */
const likesMap = {};

app.get('/', cacheView, (req, res) => {
  const n = req.query.n;

  if (!n) {
    res.render('index');
    return;
  }

  let prime;

  const key = 'prime_' + n;

  memcache.get(key, (err, val) => {
    if (err) console.log(err);

    if (val !== null) {
      // Use the value from the cache
      // Convert Buffer string before converting to number
      prime = parseInt(val.toString());
    } else {
      // No cached value available, find it
      prime = findPrime(n);

      memcache.set(key, prime.toString(), { expires: 0 }, (err) => {
        if (err) console.log(err);
      });
    }

    // Initialize likes for this number when necessary
    if (!likesMap[n]) likesMap[n] = 0;

    const locals = { n, prime, likes: likesMap[n] };
    res.render('index', locals);
  });
});

app.get('/like', (req, res) => {
  const n = req.query.n;

  if (!n) {
    res.redirect('/');
    return;
  }

  likesMap[n]++;

  // The URL of the page being 'liked'
  const url = `/?n=${n}`;

  // The view for this URL has changed, so the cached version is no longer valid, delete it from the cache.
  const key = `view_${url}`;
  memcache.delete(key, (err) => {
    if (err) console.log(err);
  });

  res.redirect(url);
});

const port = process.env.PORT || 3000;
app.listen(port, () =>
  console.log(`Example app is listening on port ${port}.`)
);
```

Save the file.

Commit and push changes to deploy:

```command
git add . && git commit -m "<^>Delete invalid cached view<^>" && git push
```

The **Like** button on your app will now work. The following stats will change on your MemCachier dashboard when a view is liked:

- **delete hits** increments as the view is deleted.
- **get misses** increases because the view was deleted and is not in the cache.
- **get hits** increments because the prime number was found in the cache.
- **Set Cmds** increases because the updated view is added to the cache.
- **Items** stays the same as the view is deleted and re-added.

You have implemented rendered view caching and invalidated cached views when they change. The final strategy you will implement is session caching.

### Caching Sessions

In this section, you'll add and cache sessions in your Express app, making your cache the session store. A common use case for sessions is user logins, so you can consider this section on caching sessions as a preliminary step for implementing a user login system in the future (though the user login system is beyond the scope of this tutorial). Storing short-lived sessions in a cache can be faster and more scalable than storing in many databases.

<$>[note]
**Note:** A cache is ideal for storing short-lived sessions that time out. However, caches are not persistent; long-lived sessions are better suited to permanent storage solutions like databases.
<$>

Install the [`express-session`](https://github.com/expressjs/session) tool to add sessions to your Express app and [`connect-memjs`](https://github.com/liamdon/connect-memjs) to enable the use of your MemCachier cache as the session store:

```command
npm install express-session connect-memjs
```

In `server.js`, import `express-session` and `connect-memjs`:

```js
[label server.js]
const express = require('express');
const findPrime = require('./utils/findPrime');
const memcache = require('./services/memcache');
const cacheView = require('./middleware/cacheView');
<^>const session = require('express-session');<^>
<^>const MemcacheStore = require('connect-memjs')(session);<^>

...
```

Save the file.

The session middleware is passed to the `connect` memcached module, allowing it to inherit from `express.session.Store`.

Still in `server.js`, configure the session middleware to use your cache as its store. Add the highlighted lines:

```js
[label server.js]
...

app.set('view engine', 'ejs');

<^>app.use(<^>
  <^>session({<^>
    <^>secret: 'your-session-secret',<^>
    <^>resave: false,<^>
    <^>saveUninitialized: true,<^>
    <^>store: new MemcacheStore({<^>
      <^>servers: [process.env.MEMCACHIER_SERVERS],<^>
      <^>prefix: 'session_',<^>
    <^>}),<^>
  <^>})<^>
<^>);<^>

...
```

The `secret` is used to sign the session cookie. Be sure to update `<^>your-session-secret<^>` with a unique string.

<$>[note]
**Note:** You should use an environment variable to set your secret for production setups. To do that, you can set the secret with `secret: process.env.SESSION_SECRET || '<^>your-session-secret<^>'`, though you would also need to set the environment variable in your App Platform dashboard.
<$>

`resave` forces the session to resave if unmodified during a request. You don't want to store the item in the cache again unnecessarily, so you set it to `false`.

`saveUninitialized: false` is useful when you only want to save modified sessions, as is often the case with login sessions where a user property might be added to the session after authentication. In this case, you will store all sessions indiscriminately, so you set it to `true`.

Finally, set `store` to your cache, setting the prefix for session cache keys to `session_`. That means the key for a session item in the cache will look like `session_<session ID>`.

Next, add some app-level debugging middleware with the highlighted lines, which will help identify the cached sessions in action:

```js
[label server.js]
...

app.use(
  session({
    ...
  })
);

<^>/**<^>
 <^>* Session sanity check middleware<^>
 <^>*/<^>
<^>app.use(function (req, res, next) {<^>
  <^>console.log('Session ID:', req.session.id);<^>

  <^>// Get the item from the cache<^>
  <^>memcache.get(`session_${req.session.id}`, (err, val) => {<^>
    <^>if (err) console.log(err);<^>

    <^>if (val !== null) {<^>
      <^>console.log('Session from cache:', val.toString());<^>
    <^>}<^>
  <^>});<^>

  <^>next();<^>
<^>});<^>

...
```

That middleware will log the session ID for each request. It then gets the session for that ID from the cache and logs its contents. This approach demonstrates that sessions are working and being cached.

Save the file, then commit and push your changes to deployment.

```command
git add . && git commit -m "<^>Add session cachin<^>" && git push
```

In your app, submit a number and then check the **Runtime Logs** in your App Platform dashboard to access your debugging messages. You will find the session ID and value that you logged, demonstrating that sessions are working and being cached.

On your MemCachier dashboard, once a view and session are cached, you'll see `3` **get hits** for every page refresh: `1` for the view, `1` for the session, and `1` for getting the session in the debugging middleware.

You have now implemented session caching. You can stop here, or you can clean up your app in the optional final step.

## (Optional) Step 7 — Cleaning Up Your Resources

The app you have deployed in this tutorial will incur charges, so you can optionally destroy the app and the MemCachier Add-On when you have finished working with them.

From the app's dashboard, click **Actions**, then **Destroy App**. 

To clean up your MemCachier Add-On, click **Add-Ons**, then the name of your MemCachier Add-On. Next, click on **Settings** and **Destroy**. A free MemCachier cache will be deactivated after 30 days of inactivity, but it is a good practice to clean up your tools.

## Conclusion

In this tutorial, you created an Express app to find a prime number with a **Like** button. You then pushed that app to GitHub and deployed it on DigitalOcean App Platform. Finally, you made the Express app faster and more scalable by implementing three object caching techniques with the MemCachier Add-On for caching resource-intensive computations, rendered views, and sessions. You can [review all the files for this tutorial in the DigitalOcean Community repository](https://github.com/do-community/express-memcache).

In each caching strategy you implemented, keys had a prefix: `prime_`, `view_` and `session_`. In addition to the namespace advantage, the prefix offers the additional benefit of allowing you to profile cache performance. You used the MemCachier developer plan in this tutorial, but you can also [try a fully managed plan](https://marketplace.digitalocean.com/add-ons/memcachier#plans) that comes with the Introspection feature set, enabling you to track the performance of individual prefixes. For example, you could monitor any prefix's hit rate or hit ratio, providing detailed insight into your cache's performance. To continue working with MemCachier, you can [review their documentation](https://www.memcachier.com/documentation/getting-started).

To keep building with DigitalOcean App Platform, try our [App Platform How-To guides](https://docs.digitalocean.com/products/app-platform/how-to/) and read further in our [App Platform documentation](https://docs.digitalocean.com/products/app-platform/).
