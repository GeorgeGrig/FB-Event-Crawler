import gspread
from oauth2client.service_account import ServiceAccountCredentials
import log_maker
from date_normalizer import normalize
from datetime import date
import Bot_Notifier
###some initialization stuff###
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
oauth_access_token = ""
###

DAYSAFTERLASTSCREENING = 545

def SheetsNewEntry(movie_name,movie_year,team_name,event_date,imdb_link,event_url,lenght):
    if lenght > 1:  ##checks if event description has more than one imdb links 
        event_url = event_url + movie_name ##this is done to avoid conflicts on the following checks
    try:
        ##checks if movie was screened recently
        sheet = client.open("Auth Movies").sheet1
        movies_list = sheet.col_values(1)
        movie_name = str(movie_name)+ " ("+str(movie_year)+")"
        if movie_name in movies_list:
            i = movies_list.index(movie_name)
            i = i + 1  
            month1,year1 = normalize(str(event_date))   
            month2,year2 = normalize (str(sheet.cell(i,3).value))   
            event_date_norm = str(month1) + str(year1)
            found_event_date = str(month2) + str(year2)
            print (found_event_date,event_date_norm)
            if event_date_norm != found_event_date:
                d0 = date(int(year2), int(month2), 1)
                d1 = date(int(year1), int(month1), 1)
                delta = d1 - d0
                print(delta.days)
                if delta.days < DAYSAFTERLASTSCREENING :
                    conflict_url = str(sheet.cell(i,5).value)
                    sheet1 = client.open("EventCrawler").sheet1
                    teams_names = sheet1.col_values(1)
                    i = teams_names.index(team_name)
                    i = i + 1  
                    team_email = sheet1.cell(i, 5).value
                    Bot_Notifier.Conflict_notifier(event_url,conflict_url,team_name,team_email)
        event_list = sheet.col_values(5)                                                 #Reads the whole fb event column
        if event_url in event_list: #checks if event already exists in the spreadsheet
            i = event_list.index(event_url)
            i = i + 1                                                                    #gets row number
            team_name_old = sheet.cell(i, 2).value 
            if team_name in team_name_old:
                log_maker.print2 ("Turns out it was just a duplicate,either there were no new events or something might have gone wrong")
            else :
                log_maker.print2 ("Turns out it's a collaboration between "+str(team_name_old)+" & "+str(team_name))
                sheet.update_cell(i, 2, str(team_name_old)+" & "+str(team_name))         #adds collab if team's name doesn't already exist in said row
            return 
        else:
            log_maker.print2("Successfully added new entry to sheets:"+" " +str(movie_name)+" "+str(movie_year)+" "+str(team_name)+" "+str(event_date))          ################
            values = [movie_name,team_name,event_date,imdb_link,event_url]
            sheet.insert_row(values, index=3, value_input_option='RAW')
    except:
        log_maker.print2("Couldn't access Google sheets")


def WordSearchSheetAdd(movie_name,movie_year,team_name,event_date,imdb_link,event_url):
   SheetsNewEntry("(D) " + str(movie_name),movie_year,team_name,event_date,imdb_link,event_url,1) #this is just done to add the (D) marker before the movie name

def SheetDataFetcher(i) :
    sheet = client.open("EventCrawler").sheet1                                      #Gets all the info needed from the second spreadsheet on the i line
    team_name = sheet.cell(i, 1).value                                              
    events_url = sheet.cell(i, 2).value
    last_id = sheet.cell(i, 3).value
    j = i + 1
    team_name_next = sheet.cell(j, 1).value
    number_of_strikes = sheet.cell(i, 4).value
    team_email = sheet.cell(i, 5).value
    return [team_name,events_url,last_id,team_name_next,number_of_strikes,team_email]

def LastEvent(i,last_id,strikes):
    sheet = client.open("EventCrawler").sheet1                                           #updates the event url which was the latest as of program end
    sheet.update_cell(i, 3, str(last_id))
    sheet.update_cell(i, 4, str(strikes))
    log_maker.print2("Successfully updated last event name in sheets: "+last_id) 
