# Rank Finder 

## What is it for?
This app is for a quick check on anyone's rank at Rocket League.

The app works for Xbox, PSN and Steam.


### How does it work?

This app is powered (indirectly) by [Tracker Network](https://tracker.gg/) from where I get the data via web-scrapping (sorry Tracker don't hate me)
I'm eager to see their full API for their Rocket League data, but thus far, it's still in development, so I only had this option.


### Set up
You will need [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/), and [Python3](https://www.python.org/downloads/)

With pip you may install the rest of the dependencies:

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Python Requests](https://requests.readthedocs.io/en/master/)


## How to use it
You can download the code and execute it in your own machine using Flask, as I'm doing myself.

I'm looking into some options to host this **and make it a full-online-accessible API** (if Tracker gives me the OK 😜)

For my Twitch stream, I hooked it with the [Streamlabs Chatbot](https://streamlabs.com/chatbot?l=es-ES), 
so when a command is called, the bot makes a request to the program retrieving the info.

At the moment, there are only 2 endpoints exposed:

- The root, which automatically searches for my own rank info
- /finder , which will get two parameters, the platform and the username

Maybe I should make a swagger just for the memes 😆