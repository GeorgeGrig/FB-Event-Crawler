import os,time,sys, random
import smtplib, ssl
import log_maker
EMAIL = "YOUR-GMAIL@gmail.com" #you need to enable less secure app on your gmail account
PASS = "YOUR-PASS"
SENDSTRIKE = False
SENDCONFLICT = True

def Strike_notifier(event_url,team_name,team_email):
    if SENDSTRIKE:
        #sends the emails and stuff
        info = "MAIL BODY\n"
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        subject = 'Subject'
        message = 'Subject:{}\n\n'.format(subject) +  info + event_url 
        log_maker.print2 ("Found strike " + team_name + " sending email to " + team_email)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(EMAIL, PASS)
            if team_email != "":
                server.sendmail(EMAIL, team_email, message.encode("utf8"))         
                server.close()
            else:
                message = message + "\nERROR MESSAGE?"
                server.sendmail(EMAIL, "YOUR EMAIL@gmail.com", message.encode("utf8"))          
                server.close()


def Conflict_notifier(event_url,conflict_url,team_name,team_email):
    if SENDCONFLICT:
        #sends the emails and stuff
        info = "MAIL BODY\n"
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        subject = 'Subject'
        message = 'Subject:{}\n\n'.format(subject) +  info + event_url + "\nΜε αυτο:\n" + conflict_url
        log_maker.print2 ("Found conflict " + team_name + " sending email to " + team_email)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(EMAIL, PASS)
            if team_email != "":
                server.sendmail(EMAIL, team_email, message.encode("utf8"))  
                server.sendmail(EMAIL, "YOUR EMAIL@gmail.com", message.encode("utf8"))          
                server.close()
            else:
                message = message + "\nERROR MESSAGE?"
                server.sendmail(EMAIL, "YOUR EMAIL@gmail.com", message.encode("utf8"))          
                server.close()
