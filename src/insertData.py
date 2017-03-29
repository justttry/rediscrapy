#encoding:UTF-8

"""
author:justry
function:向数据库插入数据
"""

import redis
from selenium import webdriver
from mainPage import ProcessMainPage
from subPages import ProcessSubPages
from compPage import ProcessCompanyPage
from webNode import WebNode
from simHash import simhash
from eventEngine import EventEngine, Event
from eventType import *
import jieba
import unittest

progPath = r"C:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe"


########################################################################
class InsertData(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, r='regions', c='company', h='hashes'):
        """Constructor"""
        self.r = redis.StrictRedis()
        self.region = r
        self.company = c
        self.hashes = h
        
    #----------------------------------------------------------------------
    def insertRegions(self, regions):
        """插入region-地区"""
        return self.r.sadd(self.region, *regions)
        
    #----------------------------------------------------------------------
    def insertCompanies(self, comps):
        """插入company-公司"""
        if type(comps) == 'list':
            return self.r.sadd(self.company, *comps)
        else:
            return self.r.sadd(self.company, comps)
        
    #----------------------------------------------------------------------
    def deleteCompanies(self, company):
        """"""
        try:
            cnt = self.r.srem(self.company, company)
        except:
            cnt = 0
        return cnt
        
    #----------------------------------------------------------------------
    def insertHoldCompanies(self, company, hold_comps):
        """"""
        if hold_comps:
            return self.r.sadd('holdcompany:'+company, *hold_comps)
        else:
            return 0
        
    #----------------------------------------------------------------------
    def insertInvestCompanies(self, company, invest_comps):
        """"""
        if invest_comps:
            return self.r.sadd('investcompany:'+company, *invest_comps)
        else:
            return 0
    
    #----------------------------------------------------------------------
    def insertHashs(self, hash_):
        """"""
        return self.r.sadd('hash:' + str(self.hashes), hash_)
    
    #----------------------------------------------------------------------
    def insertRegionCompanies(self, region, companies):
        """插入地区-公司集合"""
        try:
            cnt = self.r.sadd('region:' + region, *companies)
        except:
            print '\t\t#########insertRegionCompanies failed at %s#########' %region
            cnt = 0
        return cnt
    
    #----------------------------------------------------------------------
    def insertCompanyHash(self, company, hash_):
        """插入公司-哈希集合"""
        return self.r.sadd('company:' + company, hash_)
    
    #----------------------------------------------------------------------
    def insertHashCompanyInfo(self, hash_, cominfo):
        """插入哈希-公司信息"""
        try:
            cnt = self.r.hmset('companyInfo:' + str(hash_), cominfo)
        except:
            cnt = 0
        return cnt
    
    #----------------------------------------------------------------------
    def getHashCompanyInfo(self, key):
        """"""
        return self.r.hgetall('companyInfo:' + str(key))
    
    #----------------------------------------------------------------------
    def getHashs(self):
        """"""
        return self.r.smembers(self.hashes)
    
    #----------------------------------------------------------------------
    def clearDb(self):
        """"""
        self.r.flushdb()
    
    
########################################################################
class InsertDataTest(unittest.TestCase):
    """"""
    
    #----------------------------------------------------------------------
    def setUp(self):
        """"""
        self.r = InsertData('test')
        try:
            self.r.r.flushdb()
        except:
            pass
        self.regions = [u'北京', u'上海', u'广州', u'深圳', u'武汉']
        self.companies = [u'国家认证认可监督管理委员机关服务中心',
                          u'国际检验检疫标准与技术法规研究中心',
                          u'浙江检验检疫科学技术研究院',
                          u'宁波出入境检验检疫局机关服务中心',
                          u'上海检验检疫局工业品与原材料检测技术中心',
                          u'山东出入境检验检疫局机关服务中心',
                          u'国家质量监督检验检疫总局机关服务中心',
                          u'中国进出口商品检验研究所',
                          u'中国检验认证集团浙江有限公司',
                          u'北京安利隆生态农业有限责任公司',
                          u'中国检验认证集团天津有限公司',
                          u'中国检验认证集团陕西有限公司',
                          u'中国检验认证集团北京有限公司',
                          u'中国检验认证集团江西有限公司',
                          u'中国检验认证集团检验有限公司',
                          u'中国检验认证集团上海有限公司',
                          u'中国检验认证集团广西有限公司',
                          u'中检集团汽车检测股份有限公司',
                          u'中国检验认证集团广东有限公司',
                          u'中国检验认证集团河南有限公司']

    #----------------------------------------------------------------------
    def test_insertregion(self):
        cnt = self.r.insertRegions(self.regions)
        self.assertEqual(cnt, 5)
        print 'test_insertregion done'
        print '-' * 70
    
    #----------------------------------------------------------------------
    def test_insertcompanies(self):
        """"""
        cnt = self.r.insertCompanies(self.companies)
        self.assertEqual(cnt, 20)
        print 'test_insertcompanies done'
        print '-' * 70
    
    #----------------------------------------------------------------------
    def test_insertregioncompany(self):
        """"""
        region = u'北京'
        cnt = self.r.insertRegionCompanies(region, self.companies)
        print 'test_insertregioncompany done'
        print '-' * 70
        
    #----------------------------------------------------------------------
    def test_insertcompanyhash(self):
        """"""
        company = u'中国检验认证集团广东有限公司'
        cuts = jieba.cut(company)
        hash_ = simhash(cuts)
        cnt = self.r.insertCompanyHash(company, hash_.hash)
        self.assertAlmostEqual(cnt, 1)
        print 'test_insertcompanyhash done'
        print '-' * 70
        
    #----------------------------------------------------------------------
    def test_inserthashcompinfo(self):
        """"""
        company = u'中国检验认证集团广东有限公司'
        cuts = jieba.cut(company)
        hash_ = simhash(cuts)
        cominfo = {u'公司信息网址': 'http://www.tianyancha.com/company/4248724',
                   u'登记机关': u'深圳市市场监督管理局',
                   u'工商注册号': 440301108548379,
                   u'统一信用代码': '91440300085948158H',
                   u'组织机构代码': '085948158',
                   u'营业期限': '2013-12-20至2043-12-20',
                   u'核准日期': '2015-12-18',
                   u'行业': u'商务服务业',
                   u'企业类型': u'有限责任公司(自然人独资)'}
        cnt = self.r.insertHashCompanyInfo(hash_.hash, cominfo)
        self.assertEqual(cnt, 1)
        print 'test_inserthashcompinfo done'
        print '-' * 70
        
    #----------------------------------------------------------------------
    def test_insertgethashes(self):
        """"""
        self.r.insertHashs(0)
        self.r.insertHashs(1)
        self.r.insertHashs(2)
        self.r.insertHashs(3)
        self.r.insertHashs(4)
        ret = self.r.getHashs()
        self.assertListEqual(sorted(list(ret)), sorted(map(str, range(5))))
        

#----------------------------------------------------------------------
def suite():
    """"""
    suite = unittest.TestSuite()
    #suite.addTest(InsertDataTest('test_insertregion'))
    #suite.addTest(InsertDataTest('test_insertcompanies'))
    #suite.addTest(InsertDataTest('test_insertregioncompany'))
    #suite.addTest(InsertDataTest('test_insertcompanyhash'))
    #suite.addTest(InsertDataTest('test_inserthashcompinfo'))
    #suite.addTest(InsertDataTest('test_insertgethashes'))
    return suite
    
if __name__ == '__main__':
    unittest.main(defaultTest='suite')