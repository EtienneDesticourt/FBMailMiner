'''
Created on Nov 24, 2014

@author: Etienne
'''

from Queue import Queue
from threading import Thread
import requests, socket
from requests.exceptions import RequestException



class ProxyManager:
    "Manages everything proxy related from fetching/loading to applying."
    def __init__(self, savePath="proxyList.txt", concurrent=100):
        self.proxies = []
        self.currentProxy = 1
        self.path = savePath
        self.concurrent = concurrent
    def getProxy(self):
        proxy = {"http":"http://"+self.proxies[self.currentProxy]}
        self.currentProxy += 1
        if self.currentProxy >= len(self.proxies): self.currentProxy = 0
        return proxy
    def proxyUp(self, Session):
        "Change proxy of the passed request Session."
        if len(self.proxies) == 0: raise ValueError("No proxies loaded.")
        Session.proxies = self.getProxy()
    def checkProxy(self, url):
        "Checks to see if a proxy is still functionnal."
        s = requests.Session()
        s.proxies = {"http":"http://"+url}
        try:
            r = s.get("http://httpbin.org/ip", timeout = 15)
            if r.status_code == 200:
                return True
        except RequestException, socket.error: #Covers Connection, timeout, err 10054 exceptions and any other that should arise because of bad proxy
            pass
        return False
    def checkProxiesThread(self, q, workingProxies):
        "Check all proxies and stores the working ones."
        while True:
            url = q.get()
            if self.checkProxy(url):
                print "Working:", url
                workingProxies.append(url)
            q.task_done()            
    def startQueue(self, concurrent, workingProxies):
        "Creates a queue to store proxies and starts the threads to check them."
        q = Queue(concurrent * 2)
        for i in xrange(concurrent):
            t = Thread(target=self.checkProxiesThread, args=[q, workingProxies])
            t.daemon = True
            t.start()
        return q
    def checkProxies(self, concurrent):
        "Check all proxies stored in the file at the path location and stores them in self.proxies"
        workingProxies = []
        q = self.startQueue(concurrent, workingProxies)
        for proxy in self.proxies:
            q.put(proxy)
        q.join() #Waits for all q.get to have been followed by task done.
        print len(workingProxies), "working proxies found."
        return workingProxies    
    def fetchProxies(self):
        "Gets a proxy list from an online website."
        url = "http://www.us-proxy.org/"
        s = requests.Session()
        page = s.get(url).text
        #Single out table
        page = page.split("<tbody><tr>")[1]
        table = page.split("</td></tr></tbody>")[0]
        #Clean up ip rows
        rows = table.split("<")
        cleanRows = []
        for row in rows:
            try:
                cleanRows.append(row.split(">")[1])
            except IndexError:
                pass
        #Add proxies
        proxies = []
        for i in xrange(200):
            proxies.append( cleanRows[i*18]+":"+cleanRows[i*18+2] )
        return proxies
    def loadProxies(self, fromFile = True, checkProxies = True):
        "Loads proxy list from file or from the web and checks them by default."
        #Load
        if fromFile:            
            f = open(self.path,"r")
            self.proxies = f.read().split("\n")
            f.close()
        else:
            self.proxies = self.fetchProxies()
        #Check
        if checkProxies:
            self.proxies = self.checkProxies(self.concurrent)            
    def saveProxies(self):
        "Saves proxies to a file."
        f = open(self.path,"w")
        data = "\n".join(self.proxies)
        f.write(data)
        f.close()
            
            