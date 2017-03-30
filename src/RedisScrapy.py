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
from insertData import InsertData
from webNode import WebNode, WebNodeFF
from simHash import simhash
from eventEngine import EventEngine, Event
from eventType import *
import jieba
import unittest

progPath = r"C:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe"
        

########################################################################
class RedisScrapy(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, k=50):
        """Constructor"""
        self.url = 'http://www.tianyancha.com'
        self.eventEngine = EventEngine()
        self.insertData = InsertData()
        self.hashs = [long(i) for i in self.getHashs()]
        self.k = k
        
    #----------------------------------------------------------------------
    def start(self, cond=None):
        """
        开启抓取任务
        """
        ret = self.getSubpages()
        self.eventEngine.start()
        for web, region in ret.items():
            if cond is None:
                event = Event(EVENT_SUBWEB)
                event.dict_['data'] = WebNode(region, web)
                self.eventEngine.put(event)
                print u'推送--%s--%s--到处理器' %(region, web)
            elif region == cond:
                event = Event(EVENT_SUBWEB)
                event.dict_['data'] = WebNode(region, web)
                self.eventEngine.put(event)
                print u'推送--%s--%s--到处理器' %(region, web)
            
        
    #----------------------------------------------------------------------
    def getSubpages(self):
        """
        从主页上获取子网页列表
        Parameter:
        None
        Return:
        ret:{子网页网址:地区}
        """
        p = ProcessMainPage(self.url)
        if p.getUrl():
            subpages = p.getSubPages()
        #注册任务
        self.register(EVENT_SUBWEB, self.processSubwebs)
        print u'注册子网页处理业务'
        self.register(EVENT_SUBWEB_RETRY, self.processSubwebs_retry)
        print u'注册子网页处理重试业务'
        self.register(EVENT_COMINFO, self.processCompInfo)
        print u'注册公司信息处理业务'
        self.register(EVENT_COMINFO_FF, self.processCompInfoRefresh)
        #将地区信息存入redis
        self.insertData.insertRegions(subpages.keys())
        ret = {}
        #for i, j in subpages.items():
            #for k in range(1, 51):
                #ret[j + '/p%d'%k] = i
        ret = {j+'/p%d'%k:i for k in range(1, self.k+1) for i, j in subpages.items()}
        return ret
    
    #----------------------------------------------------------------------
    def processSubwebs(self, event):
        """子网页处理任务"""
        webnode = event.dict_['data']
        region, web = webnode.name, webnode.url
        #获取子网页中的公司-网址信息
        datas = self.getCompanies(region, web)
        for company, url in datas.items():
            if self.insertData.insertCompanies(company):
                event = Event(EVENT_COMINFO)
                event.dict_['data'] = WebNode(company, url)
                self.eventEngine.put(event)
                print u'\t推送--%s--%s--到处理器' %(company, url)
    
    #----------------------------------------------------------------------
    def processSubwebs_retry(self, event):
        """子网页处理任务"""
        webnode = event.dict_['data']
        region, web = webnode.name, webnode.url
        cnt = webnode.retry
        #大于三次取消重试
        if cnt >= 3:
            print '!!!!web---retry cnt greater than 3'
            return
        #获取子网页中的公司-网址信息
        datas = self.getCompanies_retry(region, web, cnt)
        for company, url in datas.items():
            if self.insertData.insertCompanies(company):
                event = Event(EVENT_COMINFO)
                event.dict_['data'] = WebNode(company, url)
                self.eventEngine.put(event)
                print u'\t推送--%s--%s--到处理器' %(company, url)
    
    #----------------------------------------------------------------------
    def getCompanies_retry(self, region, url, cnt):
        """
        从子网页上获取公司列表
        Return:
        datas:{公司：网址}
        """
        p = ProcessSubPages(url)
        if p.getUrl():
            datas = p.getSubPages()
        else:
            datas = {}
        #将地区-公司信息存入redis
        self.insertData.insertRegionCompanies(region, datas.keys())
        if len(datas.keys()) == 0:
            print u'#########insertRegionCompanies retry %d failed at %s#########' \
                  %(cnt, url)
            #加入重试队列
            event = Event(EVENT_SUBWEB_RETRY)
            webnode = WebNode(region, web)
            webnode.retry = cnt + 1
            event.dict_['data'] = webnode
            self.eventEngine.put(event)
            print u'!!!推送--%s--%s--到重试队列' %(region, web)
        return datas
    
    #----------------------------------------------------------------------
    def getCompanies(self, region, url):
        """
        从子网页上获取公司列表
        Return:
        datas:{公司：网址}
        """
        p = ProcessSubPages(url)
        if p.getUrl():
            datas = p.getSubPages()
        else:
            datas = {}
        #将地区-公司信息存入redis
        self.insertData.insertRegionCompanies(region, datas.keys())
        if len(datas.keys()) == 0:
            print u'\t\t#########insertRegionCompanies failed at %s#########' %url
            #加入重试队列
            event = Event(EVENT_SUBWEB_RETRY)
            event.dict_['data'] = WebNode(region, url)
            self.eventEngine.put(event)
            print u'!!!推送--%s--%s--到重试队列' %(region, url)
        return datas
    
    #----------------------------------------------------------------------
    def processCompInfo(self, event):
        """"""
        webnode = event.dict_['data']
        company, url = webnode.name, webnode.url
        self.getCompInfo(company, url)
        
    #----------------------------------------------------------------------
    def processCompInfoRefresh(self, event):
        """"""
        webnode = event.dict_['data']
        company, url, keys = webnode.name, webnode.url, webnode.keys
        print u'\t\t####重新处理队列:', company
        print u'\t\t####重新更新数据:', ' '.join(keys)
        self.getCompInfoRefresh(company, url, keys)
    
    #----------------------------------------------------------------------
    def getCompInfo(self, company, url):
        """
        获取公司信息
        """
        print u'\t\t处理--%s--' %company
        #计算hash值
        p = ProcessCompanyPage(self.eventEngine, 
                               self.insertData, 
                               company, 
                               url)
        hold_pages, invest_pages = p.getSubPages()
        cominfo = p.getComInfo()
        hash_ = simhash(cominfo.values())
        if cominfo.has_key(u'工商注册号') and cominfo[u'工商注册号'] != u'未公开':
            #将新的哈希值存入列表
            self.hashs.append(hash_.hash)
            #将新的哈希值入栈
            self.insertData.insertHashs(hash_.hash)
            #将公司信息入栈
            self.insertData.insertCompanyHash(company, cominfo[u'工商注册号'])
            self.insertData.insertHashCompanyInfo(cominfo[u'工商注册号'], cominfo)
            #self.refreshDump(company, url, cominfo)
        elif cominfo.has_key(u'登记机关'):
            self.insertData.deleteCompanies(company)
            event = Event(EVENT_COMINFO)
            event.dict_['data'] = WebNode(company, url)
            self.eventEngine.put(event)
            print u'\t\t没有工商注册号,重新推送--%s--%s--到处理器' %(company, url) 
        else:
            print u'\t\t自然人,不推送--%s--%s--到处理器' %(company, url) 
        return hold_pages, invest_pages
    
    #----------------------------------------------------------------------
    def getCompInfoRefresh(self, company, url, keys):
        """
        获取公司信息
        """
        print u'\t\t####处理更新--%s--' %company
        #计算hash值
        p = ProcessCompanyPage(self.eventEngine, 
                               self.insertData, 
                               company, 
                               url)
        hold_pages, invest_pages = p.getSubPages()
        cominfo = p.getComInfo()
        if cominfo.has_key(u'工商注册号') and cominfo[u'工商注册号'] != u'未公开':
            #将公司信息入栈
            print u'\t\t####更新键值:', ' '.join(keys)
            newcominfo = self.insertData.getHashCompanyInfo(cominfo[u'工商注册号'])
            for key in keys:
                newcominfo[key] = cominfo[key]
            self.insertData.insertHashCompanyInfo(cominfo[u'工商注册号'], newcominfo)
            #self.refreshDump(company, url, newcominfo)
    
    ##----------------------------------------------------------------------
    #def refreshDump(self, company, url, cominfo):
        #""""""
        #keys = []
        #for key, value in cominfo.items():
            #if value == u'未公开':
                #keys.append(key)
        #if keys:
            #print u'\t\t!!出现未公开数据:', company, u'重新导入队列'
            #print u'\t\t!!未公开数据:', ' '.join(keys)
            #webnode = WebNodeFF(company, url, keys)
            #event = Event(EVENT_COMINFO_FF)
            #event.dict_['data'] = webnode
            #self.eventEngine.put(event)
            
    #----------------------------------------------------------------------
    def compareHashes(self, hash_, delta=1):
        """"""
        for i in self.hashs:
            if hash_.hamming_distance(i) < delta:
                return False
        return True
            
    #----------------------------------------------------------------------
    def getHashs(self):
        """
        获取数据库中的哈希值列表
        """
        return self.insertData.getHashs()
    
    #----------------------------------------------------------------------
    def clearDb(self):
        """"""
        self.insertData.clearDb()
        
    #----------------------------------------------------------------------
    def register(self, type_, handler):
        """"""
        self.eventEngine.register(type_, handler)
        
        
########################################################################
class RedisScrapyTest(unittest.TestCase):
    """"""
    
    #----------------------------------------------------------------------
    def setUp(self):
        """"""
        self.r = RedisScrapy()
        self.r.clearDb()

    #----------------------------------------------------------------------
    def test_getsubpages(self):
        subpages = self.r.getSubpages()
        for i, j in subpages.items():
            print i, j
        print len(subpages)
        print 'test_getsubpages done'
        print '-' * 70
        
    #----------------------------------------------------------------------
    def test_getCompanies(self):
        """"""
        url = 'http://guyuan.tianyancha.com/search/p8'
        region = u'北京'
        datas = self.r.getCompanies(region, url)
        for i, j in datas.items():
            print u'公司：%s, \t网址:%s' %(i, j)
        print 'test_getCompanies done'
        print '-' * 70
    
    #----------------------------------------------------------------------
    def test_insertgethashes(self):
        """"""
        self.r.insertData.insertHashs(0)
        self.r.insertData.insertHashs(3)
        self.r.insertData.insertHashs(5)
        self.r.insertData.insertHashs(7)
        self.r.insertData.insertHashs(9)
        ret = self.r.getHashs()
        self.assertListEqual(sorted(list(ret)), 
                             sorted(map(str, [0, 3, 5, 7, 9])))
        print 'test_insertgethashes done'
        print '-' * 70
        
    #----------------------------------------------------------------------
    def test_getcompanyinfo(self):
        """"""
        url = 'http://guyuan.tianyancha.com/search/p8'
        region = u'北京'
        com_webs = self.r.getCompanies(region, url)
        for i, j in com_webs.items():
            self.r.getCompInfo(i, j)
        print 'test_getcompanyinfo done'
        print '-' * 70
        
    #----------------------------------------------------------------------
    def test_all(self):
        """"""
        r = RedisScrapy()
        r.start()
        print 'test_all done'
        print '-' * 70
        

#----------------------------------------------------------------------
def main():
    """"""
    r = RedisScrapy(1)
    r.start()
    

#----------------------------------------------------------------------
def suite():
    """"""
    suite = unittest.TestSuite()
    #suite.addTest(RedisScrapyTest('test_getsubpages'))
    #suite.addTest(RedisScrapyTest('test_getCompanies'))
    #suite.addTest(RedisScrapyTest('test_insertgethashes'))
    #suite.addTest(RedisScrapyTest('test_getcompanyinfo'))
    suite.addTest(RedisScrapyTest('test_all'))
    return suite
    
if __name__ == '__main__':
    #unittest.main(defaultTest='suite')
    main()