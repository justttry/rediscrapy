# encoding:UTF-8

"""
author: justry
function: 处理公司页面, 例如 http://www.tianyancha.com/company/5309154
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from processPageTemplate import ProcessPageTemplate
from time import sleep
import unittest

progPath = r"C:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe"
#xpath = "//a[@class='query_name search-new-color']"
hold_xpath = "//div[@class='ng-scope'][2]//tr[@class='ng-scope']/td[1]/a"
invest_xpath = "//div[@class='ng-scope'][3]//tr[@class='ng-scope']/td[1]/a"
cominfo_xpath = "//td/div[@class='c8']"

########################################################################
class ProcessCompanyPage(ProcessPageTemplate):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, url):
        super(ProcessCompanyPage, self).__init__(url)
        self.comInfo = {}
        
    #----------------------------------------------------------------------
    def getSubPages(self):
        """
        获取公司持股/投资信息
        Parameter:
        None
        Return:
        hold_ret:持股公司信息列表
        invest_ret:投资公司信息列表
        """
        self.getUrl()
        hold_data = self.driver.find_elements_by_xpath(hold_xpath)
        invest_data = self.driver.find_elements_by_xpath(invest_xpath)
        cominfo_data = self.driver.find_elements_by_xpath(cominfo_xpath)
        hold_ret = {i.text: i.get_attribute('href') for i in hold_data}
        invest_ret = {j.text: j.get_attribute('href') for j in invest_data}
        cominfo_data = [i.text.replace(u'\uff1a', ' ').split() for\
                        i in cominfo_data]
        self.comInfo = {i[0]: i[1] for i in cominfo_data}
        self.closeDriver()
        return hold_ret, invest_ret
    
    #----------------------------------------------------------------------
    def getComInfo(self):
        """
        获取公司信息
        Parameter:
        None
        Return:
        comInfo:公司相关信息
        """
        self.comInfo[u'公司信息网址'] = self.url
        return self.comInfo
    
    
########################################################################
class ProcessCompanyPageTest(unittest.TestCase):
    """"""
    
    #----------------------------------------------------------------------
    def setUp(self):
        """"""
        self.url = "http://www.tianyancha.com/company/4248724"

    #----------------------------------------------------------------------
    def test_getsubpage(self):
        p = ProcessCompanyPage(self.url)
        holddatas, investdatas = p.getSubPages()
        cominfo = p.getComInfo()
        for i, j in holddatas.items():
            print u'持股公司：%s, \t网址:%s' %(i, j)
        i, j = None, None
        for i, j in investdatas.items():
            print u'投资公司：%s, \t网址:%s' %(i, j)
        i, j = None, None
        for i, j in cominfo.items():
            print u'%s: %s' %(i, j)

    #----------------------------------------------------------------------
    def test_getcominfo(self):
        p = ProcessCompanyPage(self.url)
        p.getSubPages()
        cominfo = p.getComInfo()
        for i, j in cominfo.items():
            print u'%s: %s' %(i, j)
            

#----------------------------------------------------------------------
def suite():
    """"""
    suite = unittest.TestSuite()
    suite.addTest(ProcessCompanyPageTest('test_getsubpage'))
    suite.addTest(ProcessCompanyPageTest('test_getcominfo'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')