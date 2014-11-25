'''
Created on Nov 23, 2014
@author: Etienne
'''
from threading import Thread
from Queue import Queue
from ProxyManager import *
from FriendMiner import  FriendMiner
import requests, socket
from requests.exceptions import RequestException
from CaptchaSolver import CaptchaSolver

#TODO:
#get captcha
#create captcha solver
#save emails
#check emails


        
def parseFriends(path):
    f = open("allfriends.html","r") #Gotta be generated html not just page source
    data  = f.read()
    f.close()
    
    #Parse profile divs
    profileBoxes = []
    data = data.split("<li class=\"_698\">")
    for li in data:
        profileBoxes.append(li.split("</li>")[0])
    #Parse id links
    profileIDs = []
    for box in profileBoxes:
        profileIDs.append(box.split("https://www.facebook.com/")[1].split("?fref=pb")[0])
    #Clean up
    for ID in profileIDs:
        if "profile.php?id=" in ID or "?ref=logo\"" in ID:
            profileIDs.remove(ID)
    return profileIDs
    


    
def postCaptcha(link, solution):
    pass



    
    
    
    


def checkIP(PM):
    s = requests.Session()
    PM.proxyUp(s)
    print s.get("http://httpbin.org/ip").text


def recoverMail():
    pass


PM = ProxyManager()
PM.loadProxies(fromFile = True, checkProxies=False)
CS = CaptchaSolver()
CS.startThread(PM)
friendIDs = parseFriends(None)
 
 
FM = FriendMiner()
FM.mineFriends(friendIDs, PM, CS)


