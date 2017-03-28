#encoding:UTF-8

"""
author：justry
function: 处理主页www.tianyancha.com
"""
from bs4 import BeautifulSoup
from urllib2 import Request
from selenium import webdriver
from processPageTemplate import ProcessPageTemplate
import unittest

url = 'http://www.tianyancha.com'
xpath = "//a[@class='f13 c3 block overflow-width ng-binding ng-scope']"

########################################################################
class ProcessMainPage(ProcessPageTemplate):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, url):
        """Constructor"""
        super(ProcessMainPage, self).__init__(url)
    
    #----------------------------------------------------------------------
    def getSubPages(self):
        """
        获取子网页
        Parameter:
        None
        Return:
        ret:子网页列表
        >>> p = ProcessMainPage(url)
        >>> print p.getSubPages()
        ......
        城市：宣城, 	网址:http://xuancheng.tianyancha.com/search
        城市：沧州, 	网址:http://cangzhou.tianyancha.com/search
        城市：怀化, 	网址:http://huaihua.tianyancha.com/search
        城市：南京, 	网址:http://nanjing.tianyancha.com/search
        城市：信阳, 	网址:http://xinyang.tianyancha.com/search
        城市：舟山, 	网址:http://zhoushan.tianyancha.com/search
        城市：青岛, 	网址:http://qingdao.tianyancha.com/search
        城市：北海, 	网址:http://beihai.tianyancha.com/search
        城市：宜春, 	网址:http://ych.tianyancha.com/search
        城市：平凉, 	网址:http://pingliang.tianyancha.com/search
        城市：宁德, 	网址:http://ningde.tianyancha.com/search
        城市：怒江傈僳族自治州, 	网址:http://njlsz.tianyancha.com/search
        城市：包头, 	网址:http://baotou.tianyancha.com/search
        城市：黔东南州, 	网址:http://qdnz.tianyancha.com/search
        城市：广元, 	网址:http://guangyuan.tianyancha.com/search
        城市：汕尾, 	网址:http://shanwei.tianyancha.com/search
        城市：平顶山, 	网址:http://pds.tianyancha.com/search
        """
        ret = {}
        data = self.driver.find_elements_by_xpath(xpath)
        for i in data:
            ret[i.text[2:]] = i.get_attribute('href')
        self.closeDriver()
        return ret
    
########################################################################
class ProcessMainPageTest(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_getsubpages(self):
        p = ProcessMainPage(url)
        if p.getUrl():
            subpages = p.getSubPages()
        else:
            subpages = {}
        for i, j in subpages.items():
            print u'城市：%s, \t网址:%s' %(i, j)
        

#----------------------------------------------------------------------
def suite():
    """"""
    suite = unittest.TestSuite()
    suite.addTest(ProcessMainPageTest('test_getsubpages'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')

        
    
    