﻿#  GlamAudioIcon renderer
#  Modded and recoded by MCelliotG for use in Glamour skins or standalone
#  If you use this Renderer for other skins and rename it, please keep the first and second line adding your credits below

from os.path import exists, join

from Components.Renderer.Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import SCOPE_GUISKIN, resolveFilename


class GlamAudioIcon(Renderer):
	searchPaths = (resolveFilename(SCOPE_GUISKIN), "/usr/share/enigma2/skin_default/")

	def __init__(self):
		Renderer.__init__(self)
		self.size = None
		self.nameAudioCache = {}
		self.pngname = ""
		self.path = ""

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = join(value, "")
			else:
				attribs.append((attrib, value))
			if attrib == "size":
				value = value.split(",")
				if len(value) == 2:
					self.size = f"{value[0]}x{value[1]}"
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				sname = self.source.text
				print(f"DEBUG: Received audio name = {sname}")  # Debug output
				pngname = self.nameAudioCache.get(sname, "")
				if pngname == "":
					pngname = self.findAudioIcon(sname)
					if pngname != "":
						self.nameAudioCache[sname] = pngname
			if pngname == "":
				print("DEBUG: Hiding icon")  # Debug output
				self.instance.hide()
			else:
				print(f"DEBUG: Showing icon {pngname}")  # Debug output
				self.instance.show()
			if pngname != "" and self.pngname != pngname:
				self.instance.setPixmapFromFile(pngname)
				self.pngname = pngname

	def findAudioIcon(self, audioName):
		if self.path.startswith("/"):
			pngname = f"{self.path}{audioName}.png"
			if exists(pngname):
				return pngname
		for path in self.searchPaths:
			pngname = f"{path}{self.path}{audioName}.png"
			if exists(pngname):
				return pngname
		return ""
