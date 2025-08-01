﻿#  GlamPicon renderer
#  Modded and recoded by MCelliotG for use in Glamour skins or standalone, added Python3 support
#  If you use this Renderer for other skins and rename it, please keep the first and second line adding your credits below

import os.path
import re
import unicodedata

import six
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap
from ServiceReference import ServiceReference


class GlamPicon(Renderer):
	searchPaths = ("/media/usb/%s/", "/media/usb2/%s/", "/%s/", "/%sx/", "/usr/share/enigma2/%s/", "/usr/%s/", "/media/hdd/%s/", "/media/usb/XPicons/%s/", "/usr/share/enigma2/XPicons/%s/", "/media/hdd/XPicons/%s/", "/media/ba/%s/", "/media/cf/%s/")
	def __init__(self):
		Renderer.__init__(self)
		self.path = "picon"
		self.nameCache = {}
		self.pngname = ""

	def applySkin(self, desktop, parent):
		attribs = []
		for attrib, value in self.skinAttributes:
			if attrib == "path":
				self.path = value
			else:
				attribs.append((attrib, value))

		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				self.instance.show()
				sname = self.source.text.upper()
				pos = sname.rfind(":")
				if pos != -1:
					sname = sname[:pos].rstrip(":").replace(":", "_")
					sname = sname.split("_HTTP")[0]
				pngname = self.nameCache.get(sname, "")
				if pngname == "":
					pngname = self.findPicon(sname)
					if pngname == "":
						fields = sname.split("_", 3)
						if len(fields) > 2 and fields[2] != "2":
							fields[2] = "1"
						if fields[0] == "4097" or fields[0] == "5002":
							fields[0] = "1"
						pngname = self.findPicon("_".join(fields))
					if not pngname:
						name = ServiceReference(self.source.text).getServiceName()
						if six.PY3:
							name = six.ensure_str(unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore'))
						else:
							name = unicodedata.normalize('NFKD', unicode(name, 'utf_8', errors='ignore')).encode('ASCII', 'ignore')
						name = re.sub('[^a-z0-9]', '', name.replace('&', 'and').replace('+', 'plus').replace('*', 'star').lower())
						if len(name) > 0:
							pngname = self.findPicon(name)
							if not pngname and len(name) > 2 and name.endswith("hd"):
								pngname = self.findPicon(name[:-2])
					if pngname != "":
						self.nameCache[sname] = pngname
				if pngname == "":
					self.pngname = ""
					self.instance.hide()
					#pngname = self.nameCache.get("default", "")
					#if pngname == "":
						#pngname = self.findPicon("picon_default")
						#if pngname == "":
							#tmp = resolveFilename(SCOPE_CURRENT_SKIN, "picon_default.png")
							#if os.path.exists(tmp):
								#pngname = tmp
							#else:
								#pngname = resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/picon_default.png")
						#self.nameCache["default"] = pngname
				if self.pngname != pngname:
					self.instance.setScale(1)
					self.instance.setPixmapFromFile(pngname)
					self.pngname = pngname
			else:
				self.pngname = ""
				self.instance.hide()

	def findPicon(self, serviceName):
		for path in self.searchPaths:
			pngname = path % self.path + serviceName + ".png"
			if os.path.exists(pngname):
				return pngname

		return ""
