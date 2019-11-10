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
from imdb import IMDb
import sheets
import log_maker
import Bot_Notifier
ia = IMDb()



def imdb_link_get_by_url(imdb_id):
    try:
        movie_name = ia.get_movie(imdb_id)                                    #using imdbpy api and given imdb_id extracts movie_name and
        movie_year = movie_name['year']                                       #release year
    except:
        log_maker.print2("Couldn't extract info from imdb")
        movie_name = "Couldn't extract info from imdb"
        movie_year = "Couldn't extract info from imdb"
    imdb_link = "http://www.imdb.com/title/tt"+imdb_id+"/"                 #imdb link
    #log_maker.print2(movie_name,movie_year,imdb_link)    
    return(movie_name,movie_year,imdb_link)   

def WordSearch1(event_name):
    if '"' in event_name:
        words = event_name.split('"')[1]                                                #This function extracts whatever words are in between "" in the event_name
        if "(" and ")" in event_name:                                                   #Tries to extract movie year from event name
            text = event_name.split('(')[1]  
            text_left = text.split(')')[0]
            if len(text_left) == 4:
                words = str(words) + " "+ str(text_left)
    elif "'" in event_name:
        words = event_name.split("'")[1]                                                #This function extracts whatever words are in between "" in the event_name
        if "(" and ")" in event_name:                                                   #Tries to extract movie year from event name
            text = event_name.split('(')[1]  
            text_left = text.split(')')[0]
            words = str(words) + str(text_left)
            if len(text_left) == 4:
                words = str(words) + " "+ str(text_left)
    else :
        words = 0   
    return (words)

def WordSearch2(event_name):
    if ':' in event_name:
        words = event_name.split(':')[1]                                                #This function extracts whatever words are in between : in the event_name
        if "," in words:
            words = words.split(',')[0]
    else :
        words = 0
    return (words)

def WordSearch3(event_name):                                                                                                            
    if 'προβαλει' in event_name:
        words = event_name.split('προβαλει')[1]             #This function extracts whatever words after various προβαλλει alterations in the event_name
    elif 'προβάλλει' in event_name:
        words = event_name.split('προβάλλει')[1]
    elif 'προβαλλει' in event_name:
        words = event_name.split('προβαλλει')[1]
    elif 'προβάλει' in event_name:
        words = event_name.split('προβάλει')[1]
    elif 'presents' in event_name:
        words = event_name.split('presents')[1]
    elif 'present' in event_name:
        words = event_name.split('present')[1]
    #CAPS
    elif 'Προβαλει' in event_name:
        words = event_name.split('Προβάλλει')[1]
    elif 'Προβάλλει' in event_name:
        words = event_name.split('Προβάλλει')[1]
    elif 'Προβαλλει' in event_name:
        words = event_name.split('Προβαλλει')[1]
    elif 'Προβάλει' in event_name:
        words = event_name.split('Προβάλει')[1]
    elif 'Presents' in event_name:
        words = event_name.split('Presents')[1]
    elif 'Present' in event_name:
        words = event_name.split('Present')[1]
    elif '-' in event_name:
        words = event_name.split('-')[1]    
    else :
       words = 0
    return (words)

def imdb_link_get_by_event_name(movie_name):
    if movie_name == 0:                                                     #Queue imdb search, if no result found from given movie_name return 0
        return (0,0)
    if movie_name == "" :                                                 #checks if movie name is none
        log_maker.print2("Couldn't extract usable movie name")
        return (0,0)
    s_result = ia.search_movie(str(movie_name), results=1)
    if not s_result:                                                      #checks if imdbpy didn't find any results with the name given
        log_maker.print2("Couldn't find a match in imdb using the given movie name: "+ movie_name)
        return (0,0)
    else:
        for item in s_result:
            [imdb_name,imdb_id] = (item['long imdb canonical title'],item.movieID) 
    return(imdb_name,imdb_id)


def imdb_alternative(event_name,event_date,event_url,team_name):
    movie_name1 = WordSearch1(event_name)                                                 #Handles things when no imdb link was found in the event desc, circles through the different WordSearch methods
    [imdb_name,imdb_id] = imdb_link_get_by_event_name(movie_name1)                        #search IMDB API for the first movie and get imdb_name1 or no result
    if imdb_name != 0 :
        log_maker.print2("Found movie name "+imdb_name+" in event name using WordSearch1")                                     ###############
        [movie_name,movie_year,imdb_link] = imdb_link_get_by_url(imdb_id)
        sheets.WordSearchSheetAdd(movie_name,movie_year,team_name,event_date,imdb_link,event_url)
    elif imdb_name == 0:
        movie_name2 = WordSearch2(event_name)
        [imdb_name,imdb_id] = imdb_link_get_by_event_name(movie_name2)
        if imdb_name != 0 :
            log_maker.print2("Found movie name "+imdb_name+" in event name using WordSearch2")                                  ###############
            [movie_name,movie_year,imdb_link] = imdb_link_get_by_url(imdb_id)
            sheets.WordSearchSheetAdd(movie_name,movie_year,team_name,event_date,imdb_link,event_url)
        elif imdb_name == 0 :
            movie_name3 = WordSearch3(event_name)
            [imdb_name,imdb_id] = imdb_link_get_by_event_name(movie_name3)
            if imdb_name != 0 :
                log_maker.print2("Found movie name "+imdb_name+" in event name using WordSearch3")                          ###############
                [movie_name,movie_year,imdb_link] = imdb_link_get_by_url(imdb_id)
                sheets.WordSearchSheetAdd(movie_name,movie_year,team_name,event_date,imdb_link,event_url)
            elif imdb_name == 0:
                [movie_name,movie_year,imdb_link]= ["Couldn't extract movie name","UKNOWN_YEAR","UKNOWN"]
                sheets.WordSearchSheetAdd(movie_name,movie_year,team_name,event_date,imdb_link,event_url)
                log_maker.print2("Couldn't find movie.Sad MAYDAY MAYDAY MAYDAY")    


def per_event_handler(event_id,team_name,team_email):
    #selenium browser initialization stuffs
    options = Options() 
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options,executable_path=os.path.abspath(os.path.dirname(sys.argv[0]))+"\\" + "geckodriver.exe")    
    #navigates to url
    event_url = "https://www.facebook.com/events/"+str(event_id)
    driver.get(event_url)
    #Gets info from the given event
    date = driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[4]/div/div/div[2]/div/ul/li[1]/div/table/tbody/tr/td[2]/div/div/div[2]/div/div[1]')[0].text
    date = date.split('at')[0]
    description = driver.find_elements_by_css_selector('._63ew > span:nth-child(1)')[0].get_attribute('textContent')
    name = driver.find_elements_by_xpath('//*[@id="seo_h1_tag"]')[0].text
    imdb_ids = []
    driver.close()
    while True: #checks if there are more than one imdb links and for each extracts an imdb id
        if "imdb.com/title/" in description:
            description = description.split("imdb.com/title/tt", 1)[1]
            imdb_id = description.split("/", 1)[0]
            imdb_ids.append(imdb_id)
            #log_maker.print2 (description)
            #log_maker.print2 (imdb_ids)
        else:
            break
    if len(imdb_ids) != 0 :
        for i in imdb_ids:
            movie_name,movie_year,imdb_link = imdb_link_get_by_url(i)
            ##
            lenght = len(imdb_ids)
            sheets.SheetsNewEntry(movie_name,movie_year,team_name,date,imdb_link,event_url,lenght)
            new_strikes = "0"
    else:#if no imdb links where found calls the imdb_alternative
        imdb_alternative(name,date,event_url,team_name)
        new_strikes = "1"
        Bot_Notifier.Strike_notifier(event_url,team_name,team_email) #sends an email to someone from the target team
    return new_strikes
