'''
Created on Nov 24, 2014
@author: Etienne
'''

import time, requests, shutil
from PIL import Image
from Queue import Queue
from threading import Thread


class CaptchaSolver:
    def __init__(self):
        self.solvedCaptchas = {}
        self.captchaQueue = Queue(1000)
    def solveCaptcha(self, ID, captchaLink):
        self.solvedCaptchas[ID] = None
        self.captchaQueue.put((ID,captchaLink))
        while self.solvedCaptchas[ID] == None:
            time.sleep(1)
        return self.solvedCaptchas[ID]
    def showCaptchas(self, PM):               
        while True:
            ID, captchaLink = self.captchaQueue.get()
            img = requests.get(captchaLink, stream=True, proxies=PM.getProxy()) 
            f = open("temp.jpg", 'wb')
            shutil.copyfileobj(img.raw, f)
            f.close()
            img = Image.open("temp.jpg")
            img.show()
            solution = raw_input("Solution:")
            self.solvedCaptchas[ID] = solution
            self.captchaQueue.task_done()
    def startThread(self, PM):
        t = Thread(target=self.showCaptchas, args=[PM])
        t.daemon = True
        t.start()
            