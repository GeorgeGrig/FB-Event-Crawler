# FB-Event-Crawler
Grabs movie info from a Facebook event (from a given list of Fb pages) using imdbpy.

Facebook API is not used because the restrictions added after the cambridge analytica scandal made it much harder to get access to various API functions

## Getting started  
* In order to run the script you need to install all the required prerequisites.  
* A version of geckodriver.exe in the directory.  
* [imdbpy](https://imdbpy.sourceforge.io/).  
* Put a [working](https://developers.google.com/sheets/api/quickstart/python) client_secret.json for Google sheets access inside the script folder.  
* Create a google sheet named "EventCrawler" with a layout like [this](https://imgur.com/a/DTgdDaC) and another one named however you like but remember to change the value in the script and give access to your developer account.  
