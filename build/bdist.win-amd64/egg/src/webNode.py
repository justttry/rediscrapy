#encoding:UTF-8

########################################################################
class WebNode(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, name, url):
        """Constructor"""
        self.name = name
        self.url = url
        self.retry = 0
        
########################################################################
class WebNodeFF(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, name, url, keys):
        """Constructor"""
        self.name = name
        self.url = url
        self.keys = keys
        
    
    