# encoding:UTF-8

"""
author：justry
function: 处理子网页, 例如 bj.tianyancha.com/search/p14
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import unittest

url = 'http://bj.tianyancha.com/search/p14'
progPath = r"C:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe"

########################################################################
class ProcessSubPages(object):
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
            self.driver.get(url)
            ret = True
        except:
            ret = False
        return ret
        
    #----------------------------------------------------------------------
    def getSubPages(self):
        """
        获取公司子网页
        Parameter:
        None
        Return:
        ret:公司子网页列表
        >>> data = {}
        >>> p = ProcessSubPages(url)
        >>> if p.getUrl():
        >>>     data = p.getSubPages()
        >>> for i, j in data.items():
        >>>     print u'公司：%s, \t网址:%s' %(i, j)
        """
        ret = {}
        data = self.driver.find_elements_by_xpath(xpath)
        for i in data:
            ret[i.text[2:]] = i.get_attribute('href')
        return ret
    
    
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