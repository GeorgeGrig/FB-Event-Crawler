# FB-Event-Crawler
Grabs movie info from a Facebook event using imdbpy.

Facebook API is not used because the restrictions added after the cambridge analytic scandal made it much harder to get access to various API functions

## Prerequisites
In order to run the script you need to have the following:
```
gspread ---> https://github.com/burnash/gspread/
oauth2client
selenium (A windows 64bit version of gecko driver is already provided in the package)
imdbpy ---> https://imdbpy.sourceforge.io/
```
## Getting started
* Put a working client_secret.json for Google sheets access inside the script folder (how-To: https://developers.google.com/sheets/api/quickstart/python)

* Create a google sheet named "EventCrawler" with a layout like this: https://imgur.com/a/DTgdDaC and another one named however you like but remember to change the value in the 
script and give access to your developer account.

## Also...
I probably won't maintain this at all
