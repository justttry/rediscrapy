# encoding:UTF-8

"""
author：justry
function: 处理网页模板
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import unittest

progPath = r"C:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe"

########################################################################
class ProcessPageTemplate(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, url):
        """Constructor"""
        self.url = url
        self.driver = webdriver.PhantomJS(executable_path=progPath)
        
    #----------------------------------------------------------------------
    def getUrl(self):
        """"""
        try:
            self.driver.get(self.url)
            ret = True
        except:
            ret = False
        return ret
        
    #----------------------------------------------------------------------
    def getSubPages(self):
        """"""
        raise NotImplementedError
    
    
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