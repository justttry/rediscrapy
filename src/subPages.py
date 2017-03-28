# encoding:UTF-8

"""
author：justry
function: 处理子网页, 例如 bj.tianyancha.com/search/p14
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from processPageTemplate import ProcessPageTemplate
import unittest

url = 'http://bj.tianyancha.com/search/p14'
xpath = "//a[@class='query_name search-new-color']"

########################################################################
class ProcessSubPages(ProcessPageTemplate):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, url):
        """Constructor"""
        super(ProcessSubPages, self).__init__(url)
        
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
        公司：银建投资公司, 	网址:http://www.tianyancha.com/company/5309154
        公司：富力城房地产开发有限公司, 	网址:http://www.tianyancha.com/company/2902988
        公司：市有色金属工业总公司, 	网址:http://www.tianyancha.com/company/395385
        公司：京铁实业开发总公司, 	网址:http://www.tianyancha.com/company/1760522
        公司：华信电子企业集团, 	网址:http://www.tianyancha.com/company/607987
        公司：金通资产经营管理公司, 	网址:http://www.tianyancha.com/company/1136032
        公司：市食品公司, 	网址:http://www.tianyancha.com/company/4038095
        公司：中化股份有限公司, 	网址:http://www.tianyancha.com/company/7623655
        公司：中邮资产管理有限公司, 	网址:http://www.tianyancha.com/company/25952946
        公司：鹏润投资有限公司, 	网址:http://www.tianyancha.com/company/2954997
        公司：中化集团公司, 	网址:http://www.tianyancha.com/company/14733566
        公司：盛世恒兴格力国际贸易有限公司, 	网址:http://www.tianyancha.com/company/1213946
        公司：外轮理货总公司, 	网址:http://www.tianyancha.com/company/6950903
        公司：新兴（集团）总公司, 	网址:http://www.tianyancha.com/company/19261871
        公司：标志基汇投资有限公司, 	网址:http://www.tianyancha.com/company/22297653
        公司：中民资产管理有限公司, 	网址:http://www.tianyancha.com/company/2353358769
        公司：电力股份公司, 	网址:http://www.tianyancha.com/company/2450873725
        公司：风险投资有限公司, 	网址:http://www.tianyancha.com/company/1458533
        公司：资本投资管理集团有限公司, 	网址:http://www.tianyancha.com/company/2353037428
        公司：检验认证（集团）有限公司, 	网址:http://www.tianyancha.com/company/4248724
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