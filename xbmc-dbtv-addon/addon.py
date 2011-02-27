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
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import urllib
import re
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from BeautifulSoup import BeautifulSoup
from Item import Item

__settings__ = xbmcaddon.Addon(id="plugin.video.dbtv")
__language__ = __settings__.getLocalizedString


def createMainMenu(baseUrl, handle):
	"""
	Reads channels from dagbladet.no. When done sends them to Xbmc
	This is the plugin main menu
	"""
	soup = BeautifulSoup(urllib.urlopen('http://www.dagbladet.no/tv/'))
	# Finds the <div> tag containing all the channels
	channels = soup.find('div', attrs={'id':re.compile('kanaler2')})
	# Feed it back to BeautifulSoup to get the actual channels
	soup = BeautifulSoup(str(channels))
	# Each channel name is it's own link (<a></a>)
	channels = soup.findAll('a')

	listing = []
	for channel in channels:
		url = channel['href']
		url_split = url.rsplit('=', 1)
		# The channel "Huset" doesn't have a category ID, which means it will not be added.
		# TODO: Huset
		if len(url_split) > 1:
			cat_id = url_split[1]
			listing.append(Item(title=channel.contents[0], url=baseUrl+"?sub=" + str(cat_id) + "=0"))
	sendToXbmc(handle, listing)

def createSubMenu(baseUrl, handle, cat_id, offset="0"):
	url = 'http://www.dagbladet.no/api/kommentar/gallery/?op=VideosByCategory&catid=%s&offset=%s' % (cat_id, offset)
	soup = BeautifulSoup(urllib.urlopen(url))
	objs = soup.findAll('obj')

	listing = []
	for obj in objs:
		obj_soup = BeautifulSoup(str(obj))
		progid = obj_soup.find('mm_id').contents[0]
		title =  obj_soup.find('caption').contents[0]
		duration =  obj_soup.find('duration').contents[0]
		viewed =   obj_soup.find('viewedtimes').contents[0]
		date =  obj_soup.find('uploadedtime').contents[0]
		rating =  obj_soup.find('rating').contents[0]
		votes =  obj_soup.find('votes').contents[0]
		category =  obj_soup.find('category').contents[0]
		thumb = 'http://front.xstream.dk/dagbladet/GetThumbnail.php?ClipId=%s' % (progid)
		stream_url = 'http://front.xstream.dk/dagbladet/xmlgenerator.php?id=%s' % (progid)
		stream_soup = BeautifulSoup(urllib.urlopen(stream_url))
		stream_url = stream_soup.find('flv', attrs={'id':re.compile(progid)})['flv8']

		listing.append(Item(progid=progid, title=title, duration=duration,
			viewed=viewed, date=date, rating=rating, votes=votes, thumb=thumb,
			category=category, url=stream_url, isPlayable=True))

	new_offset = int(offset) + 12
	listing.append(Item(title=__language__(30000), category=cat_id, url=baseUrl+"?sub=" + str(cat_id) + "=" + str(new_offset)))
	sendToXbmc(handle, listing)

def sendToXbmc(handle, listing):
	"""
	Sends a listing to XBMC for display as a directory listing
	Plugins always result in a listing
	@param list listing
	@retur n void
	"""
	# send each item to xbmc
	for item in listing:
		listItem = xbmcgui.ListItem(item.title, thumbnailImage=item.thumb)
		listItem.setInfo(type="Video", infoLabels={"title": item.title, "plot":item.description,
		"duration":item.duration, "rating":int(item.rating), "playcount":int(item.viewed),
		"date":item.date, "votes":item.votes})
		xbmcplugin.addDirectoryItem(handle, item.url, listItem, not item.isPlayable)

	# tell xbmc we have finished creating the directory listing
	xbmcplugin.endOfDirectory(handle)

if ( __name__ == "__main__" ):
	xbmcplugin.setContent(int(sys.argv[1]), "episodes")
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

	# Probaly not the "correct way...
	# sys.argv[2]: ?sub=<category id>=<offset>
	# Offset is used to paginate the movies within a category
	arg = sys.argv[2].split('=')

	if (arg[0] == "?sub"):
		createSubMenu(sys.argv[0], int(sys.argv[1]), arg[1], arg[2])
	else:
		createMainMenu(sys.argv[0], int(sys.argv[1]))

