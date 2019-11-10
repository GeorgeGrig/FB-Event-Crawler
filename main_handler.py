import os,time,sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import sheets, fb_event_handler
import log_maker

TIMES_TO_SCROLL_DOWN = 15

def Events(events_url):
    #Navigates to target events page, scrolls down a given number of times and extracts event_id for every visible event found
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options,executable_path=os.path.abspath(os.path.dirname(sys.argv[0]))+"\\" + "geckodriver.exe")    
    #navigates to url
    driver.get(events_url)
    i = TIMES_TO_SCROLL_DOWN #how many times to scroll down
    while i > 0:
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i -= 1
    test = driver.find_elements_by_xpath("//div[@class='_4dmk']//a[contains(@href,'')]")
    event_ids = []
    for item in test:
        event_id = str(item.get_attribute("href")).split("www.facebook.com/events/", 1)[1]
        event_id = event_id.split("/", 1)[0]
        event_ids.append(event_id)
    #log_maker.print2 (len(event_ids))
    driver.close()
    return event_ids


def main():
    EMPTY_LOG_FINDER = "test"                                      #finds empty log cell(if it's empty end function because there are no more teams left to check)
    i=2
    while  EMPTY_LOG_FINDER != "": 
        [team_name,events_url,last_id,team_name_next,number_of_strikes,team_email]=sheets.SheetDataFetcher(i)                        #Fetches from sheets team name etc.
        log_maker.print2 ("Doing "+ team_name)                                                 ######################
        event_ids = Events(events_url)
        new_strikes = 0
        for event_id in event_ids: #adds new strikes to a team if they didn't add an imdb link to their event
            if event_id != last_id:
                strikes = fb_event_handler.per_event_handler(event_id,team_name,team_email)
                new_strikes = int(new_strikes) + int(strikes)
            else:
                strikes = int(number_of_strikes) + int(new_strikes)
                sheets.LastEvent(i,event_ids[0],strikes)
                break
        i += 1
        EMPTY_LOG_FINDER = team_name_next                                                #Repeats stuffs for each "team"


def Cleaner():   
    #Just some housekeeping to keep the logs file in a managable size
    with open("logs", "w",encoding='utf-8') as f: #About every month in flushes the logs
        f.write("#####################################\n#####################################\n")
    log_maker.print2("Flushed logs")
    with open("cleaner", "w",encoding='utf-8') as f:
        f.write("value=")
        f.write(str(0))
    main()
    return

def Handler():
    with open("logs", "a",encoding='utf-8') as f:
        f.write("#####################################\n#####################################\n")
        f.close()
    file = open("cleaner", "r",encoding='utf-8')
    k = str(file.read(10))
    k = k.split('=')[1]
    k = int(k)
    file.close()
    main()
    k=k+1
    if k>30 :
        Cleaner()
    with open("cleaner", "w",encoding='utf-8') as f:
        f.write("value=")
        f.write(str(k))
        f.close()
    log_maker.print2("Done,waiting 24h to start next circle")




Handler()
