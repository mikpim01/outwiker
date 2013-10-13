#!/usr/bin/python
# -*- coding: UTF-8 -*-

from fontsizebase import WikiFontSizeBaseAction


class WikiFontSizeSmallAction (WikiFontSizeBaseAction):
    """
    Действие для выделения текста мелким шрифтом
    """
    stringId = u"WikiSmallFont"

    @property
    def title (self):
        return _(u"Small font")


    @property
    def description (self):
        return _(u"Small font for wiki pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        self.selectFontSize (3)
