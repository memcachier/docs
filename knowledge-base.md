# How do you guarantee locality of MemCachier servers with my Heroku Dynos?
Sadly we can't. We make sure that we are in the same amazon data center as your Heroku dynos. So right now for Heroku that is either EU or US-East.

However, Amazon data centers also have availability zones (AZ), which are marketed as physically isolated sub-data-centers providing fault tolerance (separate power, networks... etc). Going from one AZ to another is more expensive than going between two machines in the same AZ. Latency in same AZ is pretty stable and around 0.3ms. Latency across AZ is higher, around 0.5 - 1.5ms and much more variability (outliers can be 100's of ms).

Heroku spins up your dynos in multiple AZ and chooses them randomly. So there is no way for us to be in the same AZ as all your dyno's.

This is generally fine as cross AZ is fast enough but the outliers in the network latency do cause some problems as its often the case that when a customers sees time outs on rare occasions in their logs they are caused by this fundamental issue and not something we can address. These occurrences are rare though so overall cause no issue, just annoying log messages.

# I noticed that one particular Dyno couldn't connect to MemCachier. What is best practices for handling this?
Yes, sadly this seems to be an issue in the underlying Amazon network. Occasionally as you saw, customers report just one certain dyno not being able to connect.

In general we recommend restarting that particular dyno, although usually this is done by hand. As you wisely say, doing this automatically would cause your app to not function is MemCachier went down.

Our suggestion would be that your app ideally should function as well as possible with MemCachier being 'down'. This applies for all services you are using. Now, that said it makes sense to have an automated way to detect when any service is down. It then makes sense to try just restarting the dyno a few times automatically, but only a few times, not infinitely.

This is similar to how upstart or systemd works if you are familiar with running services using these Linux frameworks. They have an ability to restart a service if they detect it has crashed but will only do so up to some limit (i.e., 5 times) before killing the process completely.

So in summary, our best practice suggestion is:
* Design your app to function as well as possible with any service being down.
* Have an automated way to detect a service being 'down' to any particular dyno.
* Have an automated way to restart that dyno but with a limit on how many times in a short space of time this can occur.
* When the limit is hit, the dyno should be started again so it can run as well as possible without access to the service.
* In this final case, a notification should be sent to a team member to be resolved by a human.

Now having all of this would be awesome and make your app quite fault tolerant and one of the best designed on Heroku I would think :) It's also a reasonable amount of work, so the easiest solution may just be an automated notification system that brings a human in when needed to either restart one particular dyno or take other actions.

