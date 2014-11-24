'''
Created on Nov 23, 2014
@author: Etienne
'''
from threading import Thread
from Queue import Queue
from ProxyManager import *
import requests, socket
from requests.exceptions import RequestException

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
    

def parseCaptchaLink(data):
    data = data.split("https:\/\/www.facebook.com\/captcha\/")[1]
    data = data.split("\\\" alt=")[0]
    link = "https://www.facebook.com/captcha/"+data
    return link
    


def mineFriend(ID, PM, CS):
    recoveryLink0 = "https://www.facebook.com/ajax/login/help/identify.php?ctx=recover&__a=1&email="
    s = requests.Session()
    ProxyManager.proxyUp(s)
    try:
        recoveryLink1 = s.get(recoveryLink0+ID, timeout = 5).text
        if "Security Check" in recoveryLink1:
            captchaLink = parseCaptchaLink(recoveryLink1)
            solution = CS.solveCaptcha(ID, captchaLink )
    except RequestException, socket.error:
        pass
    
    
    
    
def mineFriendList(friendList, friendQueue, ProxyManager, CaptchaSolver):
    for ID in friendList:
        friendQueue.put(ID)
    friendQueue.join()

def checkIP(PM):
    s = requests.Session()
    PM.proxyUp(s)
    print s.get("http://httpbin.org/ip").text
def proxyUp(session):
    pass

def recoverMail():
    pass


# PM = ProxyManager()
# PM.loadProxies(fromFile = True, checkProxies=False)

# friendIDs = parseFriends(None)
# print friendIDs
# checkIP(PM)

# mineFriendList(friendIDs, PM)
# f = open("securityCheck.txt","r")
# data = f.read()
# f.close()
# parseCaptchaLink(data)