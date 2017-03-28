# encoding:UTF-8

"""
# Author: justry
#         
# Instruments: 事件驱动模块
"""

from Queue import Queue, Empty
from threading import Thread
from time import sleep

from eventType import *
import unittest

########################################################################
class EventEngine(object):
    """事件驱动模块"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.__queue = Queue()
        
        self.__active = False
        
        self.__thread = Thread(target=self.__run)
        
        self.__timer = Thread(target=self.__runTimer)
        self.__timerActive = False
        self.__timerSleep = 1
        
        self.__handlers = {}
        
    #----------------------------------------------------------------------
    def __run(self):
        """引擎运行"""
        while self.__active:
            try:
                event = self.__queue.get(block=True, timeout=1)
                self.__process(event)
            except Empty:
                pass
    
    #----------------------------------------------------------------------
    def __process(self, event):
        """处理数据"""
        if event.type_ in self.__handlers:
            [handler(event) for handler in self.__handlers[event.type_]]
            
    #----------------------------------------------------------------------
    def __runTimer(self):
        """向事件队列存入计时器事件"""
        while self.__timerActive:
            event = Event(type_=EVENT_TIMER)
            
            self.put(event)
            
            sleep(self.__timerSleep)
        
    #----------------------------------------------------------------------
    def start(self):
        """引擎启动"""
        self.__active = True
        self.__thread.start()
        self.__timerActive = True
        self.__timer.start()
        
    #----------------------------------------------------------------------
    def stop(self):
        """引擎停止"""
        self.__active = False
        self.__timerActive = False
        self.__timer.join()
        self.__thread.join()
        
    #----------------------------------------------------------------------
    def register(self, type_, handler):
        """注册事件处理函数"""
        try:
            handlerList = self.__handlers[type_]
        except KeyError:
            handlerList = []
            self.__handlers[type_] = handlerList
            
        if handler not in handlerList:
            handlerList.append(handler)
            
    #----------------------------------------------------------------------
    def unregister(self, type_, handler):
        """注销事件处理监听"""
        try:
            handlerList = self.__handlers[type_]
            
            if handler in handlerList:
                handlerList.remove(handler)
                
            if not handlerList:
                del self.__handlers[type_]
        
        except KeyError:
            pass
        
    #----------------------------------------------------------------------
    def put(self, event):
        """向事件队列中存入事件"""
        self.__queue.put(event)
        
        
########################################################################
class Event(object):
    """事件对象"""

    #----------------------------------------------------------------------
    def __init__(self, type_=None):
        """Constructor"""
        self.type_ = type_
        self.dict_ = {}
    

########################################################################
class EventEngineTest(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_0(self):
        import sys
        from datetime import datetime
        from PyQt4.QtCore import QCoreApplication
        
        def simpletest(event):
            print u'处理每秒触发的计时器事件:%s' % str(datetime.now())
            
        app = QCoreApplication(sys.argv)
        
        ee = EventEngine()
        ee.register(EVENT_TIMER, simpletest)
        ee.start()
        
        app.exec_()
        
#----------------------------------------------------------------------
def suite():
    """"""
    suite = unittest.TestSuite()
    suite.addTest(EventEngineTest('test_0'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')