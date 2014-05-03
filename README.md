## Introduction

The [Wall Street Journal](http://wsj.com) is an excellent financial newspaper, but its RSS feeds are a hot mess. They're an embarassment to the newspaper.

There's too many of them, if you don't subscribe to many you'll miss articles, but if you subscribe to many you'll see a whole mess of duplicated articles.

This fixes that. Put a bunch of feeds in feedlist.txt, run wsjfixer.py every 10 minutes or so, and you'll have a constantly updated feed of Wall Street Journal articles, from just the sources that you want, with no duplicates.

I uploaded it to a [DigitalOcean $5 a month server](https://www.digitalocean.com/?refcode=1524b0f92fa4)*, installed Apache, and had wsjfixer output the RSS file to the web root directory so Apache could serve it. Then I just scheduled it to run via cron every 30 minutes.

So far it's working perfectly in various feed readers I use. 

It's still a quick and dirty hack, but I'm having fun with it and finding it useful.

* Note. That's a referral link. Go straight to [https://www.digitalocean.com/](https://www.digitalocean.com/) if you want to avoid the referral.