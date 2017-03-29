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