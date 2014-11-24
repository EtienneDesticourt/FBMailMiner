'''
Created on Nov 24, 2014
@author: Etienne
'''

import time
from Queue import Queue


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
        