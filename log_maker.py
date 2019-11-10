import time,os,sys

def print2(text):
    text = str(text)
    print (time.ctime(),":",text)
    with open("logs", "a",encoding='utf-8') as f:
        f.write(time.ctime()+":"+text+"\n")
        f.close()
