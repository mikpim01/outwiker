#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с поиском
"""

import os.path

from core.tree import WikiPage
from core.search import AllTagsSearchStrategy, AnyTagSearchStrategy, TagsList

from SearchPanel import SearchPanel
import core.system
from core.application import Application
from core.factory import PageFactory
from core.exceptions import ReadonlyException

paramsSection = u"Search"

class SearchWikiPage (WikiPage):
	"""
	Класс HTML-страниц
	"""
	def __init__ (self, path, title, parent, readonly = False):
		WikiPage.__init__ (self, path, title, parent, readonly)

		# Искомая фраза
		self._phrase = self._getPhrase()

		# Теги, по которым осуществляется поиск (не путать с тегами, установленными для данной страницы)
		self._searchTags = self._getSearchTags()

		# Стратегия для поиска
		self._strategy = self._getStrategy()


	@staticmethod
	def getTypeString ():
		return u"search"

	
	def _getPhrase (self):
		"""
		Возвращает искомую фразу
		"""
		phrase = u""
		try:
			phrase = self.getParameter (paramsSection, u"phrase")
		except:
			pass

		return phrase

	
	@property
	def phrase (self):
		return self._phrase


	@phrase.setter
	def phrase (self, phrase):
		"""
		Устанавливает искомую фразу
		"""
		self._phrase = phrase

		try:
			self.setParameter (paramsSection, u"phrase", phrase)
		except ReadonlyException:
			# Ничего страшного, если поисковая фраза не сохранится
			pass

		Application.onPageUpdate (self)
	

	def _getSearchTags (self):
		"""
		Загрузить список тегов из настроек страницы
		"""
		tags_str = u""

		try:
			tags_str = self.getParameter (paramsSection, "tags")
		except:
			pass

		tags = TagsList.parseTagsList (tags_str)
		return tags


	@property
	def searchTags (self):
		return self._searchTags


	@searchTags.setter
	def searchTags (self, tags):
		"""
		Выбрать теги для поиска
		"""
		self._searchTags = tags
		tags_str = TagsList.getTagsString (tags)

		try:
			self.setParameter (paramsSection, u"tags", tags_str)
		except:
			# Ну не сохранятся искомые теги, ничего страшного
			pass

		Application.onPageUpdate (self)
	

	def _getStrategy (self):
		strategy = 0
		try:
			strategy = int (self.getParameter (paramsSection, u"strategy"))
		except:
			pass

		return self._strategyByCode(strategy)
	

	def _strategyByCode (self, code):
		if code == 0:
			return AnyTagSearchStrategy
		else:
			return AllTagsSearchStrategy
	

	@property
	def strategy (self):
		return self._strategy
	

	@strategy.setter
	def strategy (self, strategy):
		if strategy == AllTagsSearchStrategy:
			strategyCode = 1
		else:
			strategyCode = 0

		self._strategy = strategy

		try:
			self.setParameter (paramsSection, u"strategy", strategyCode)
		except ReadonlyException:
			# Ничего страшного
			pass

		Application.onPageUpdate (self)


class SearchPageFactory (PageFactory):
	@staticmethod
	def getPageType():
		return SearchWikiPage

	@staticmethod
	def getTypeString ():
		return SearchPageFactory.getPageType().getTypeString()

	# Название страницы, показываемое пользователю
	title = _(u"Search Page")

	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		"""
		Создать страницу. Вызывать этот метод вместо конструктора
		"""
		return PageFactory.createPage (SearchPageFactory.getPageType(), parent, title, tags)


	@staticmethod
	def getPageView (page, parent):
		"""
		Вернуть контрол, который будет отображать и редактировать страницу
		"""
		panel = SearchPanel (parent)
		panel.page = page

		return panel


	@staticmethod
	def getPrefPanels (parent):
		return []


class GlobalSearch (object):
	pageTitle = _(u"# Search")

	@staticmethod
	def create (root, phrase = u"", tags = [], strategy = AllTagsSearchStrategy):
		"""
		Создать страницу с поиском. Если страница существует, то сделать ее активной
		"""
		title = GlobalSearch.pageTitle
		number = 1
		page = None

		imagesDir = core.system.getImagesDir()

		while page == None:
			page = root[title]
			if page == None:
				page = SearchPageFactory.create (root, title, [])
				page.icon = os.path.join (imagesDir, "global_search.png")
			elif page.getTypeString() != SearchPageFactory.getTypeString():
				number += 1
				title = u"%s %d" % (GlobalSearch.pageTitle, number)
				page = None
		
		page.phrase = phrase
		page.searchTags = [tag for tag in tags]
		page.strategy = strategy
		page.root.selectedPage = page

		return page

