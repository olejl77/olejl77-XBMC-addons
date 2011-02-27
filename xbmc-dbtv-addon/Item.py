# -*- coding: utf-8 -*-
'''
Dagbladet TV plugin for XBMC
Copyright (C) 2011 olejl77@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

class Item:
    def __init__(self, title="", description="", date="", author="", 
	category="", thumb="", thumbBig="", url="", progid="", duration="", 
	rating="0", votes="0", viewed="0", isPlayable=False):
        self._title = title
        self._description = description
        self._date = date
        self._author = author
        self._category = category
        self._thumb = thumb
        self._thumbBig = thumbBig
        self._url = url
	self._progid = progid
	self._duration = duration
	self._rating = rating
	self._votes = votes
	self._viewed = viewed
        self._isPlayable = isPlayable
    
    @property
    def isPlayable(self):
        return self._isPlayable
    
    @property
    def title(self):
        return self._title
    
    @property
    def description(self):
        return self._description
    
    @property
    def date(self):
        return self._date
    
    @property
    def author(self):
        return self._author
    
    @property
    def category(self):
        return self._category
    
    @property
    def thumb(self):
        return self._thumb
    
    @property
    def thumbBig(self):
        return self._thumbBig
    
    @property
    def url(self):
        return self._url

    @property
    def progid(self):
        return self._progid

    @property
    def duration(self):
        return self._duration

    @property
    def rating(self):
        return self._rating

    @property
    def votes(self):
        return self._votes

    @property
    def viewed(self):
        return self._viewed
