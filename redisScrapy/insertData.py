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