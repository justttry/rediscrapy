# encoding:UTF-8

"""
author：justry
function: 处理网页模板
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import unittest

progPath = r"D:\Anaconda2\Tools\phantomjs-2.1.1-windows\bin\phantomjs.exe"

########################################################################
class ProcessPageTemplate(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, url):
        """Constructor"""
        self.url = url
        
    #----------------------------------------------------------------------
    def getUrl(self, sleeptime=1):
        """"""
        try:
            dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
            service_args = ['--load-images=false', '--proxy-type=None']
            self.driver = webdriver.PhantomJS(executable_path=progPath, service_args=service_args, desired_capabilities=dcap)            
            #self.driver = webdriver.PhantomJS(executable_path=progPath)
            self.driver.get(self.url)
            sleep(sleeptime)
            ret = True
        except:
            ret = False
        return ret
        
    #----------------------------------------------------------------------
    def getSubPages(self):
        """"""
        raise NotImplementedError
    
    #----------------------------------------------------------------------
    def closeDriver(self):
        """"""
        self.driver.close()
        self.driver.quit()
    
    
########################################################################
class ProcessSubPagesTest(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_getsubpages(self):
        p = ProcessSubPages(url)
        if p.getUrl():
            datas = p.getSubPages()
        for i, j in datas.items():
            print u'公司：%s, \t网址:%s' %(i, j)
            
#----------------------------------------------------------------------
def suite():
    """"""
    suite = unittest.TestSuite()
    suite.addTest(ProcessSubPagesTest('test_getsubpages'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')