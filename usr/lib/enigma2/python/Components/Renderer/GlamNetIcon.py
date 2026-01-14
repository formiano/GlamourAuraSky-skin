# GlamBaseIcons - common base renderer for SVG/PNG icons
# Used by GlamNetIcon, GlamAudioIcon, and any future Glam-* icon renderers
# Coded by MCelliotG for use in Glamour skins or standalone
# If you use this Renderer for other skins and rename it, please keep the lines above adding your credits below

from os.path import exists, join
from enigma import ePixmap
from Components.Renderer.Renderer import Renderer
from Tools.Directories import SCOPE_GUISKIN, resolveFilename

class GlamNetIcon(Renderer):
	searchPaths = (
		resolveFilename(SCOPE_GUISKIN),
		"/usr/share/enigma2/skin_default/"
	)

	GUI_WIDGET = ePixmap

	def __init__(self):
		Renderer.__init__(self)
		self.size = None
		self.cache = {}
		self.currentIcon = ""
		self.path = ""
		print("[GlamNetIcon] Base icon renderer initialized")

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = join(value, "")
				print(f"[GlamNetIcon] applySkin: path='{self.path}'")
			elif attrib == "size":
				parts = value.split(",")
				if len(parts) == 2:
					self.size = (int(parts[0]), int(parts[1]))
					print(f"[GlamNetIcon] applySkin: size={self.size}")
				attribs.append((attrib, value))
			else:
				attribs.append((attrib, value))

		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def _tryIcon(self, base, name, ext):
		full = f"{base}{self.path}{name}.{ext}"
		print(f"[GlamNetIcon] Trying {ext.upper()}: {full}")
		return full if exists(full) else ""

	def findIcon(self, name):
		if not name:
			return ""

		lname = name.lower()
		if lname == "unknown":
			return ""

		if self.path.startswith("/"):
			svg = f"{self.path}{name}.svg"
			if exists(svg):
				return svg

			png = f"{self.path}{name}.png"
			if exists(png):
				return png

		for base in self.searchPaths:
			svg = self._tryIcon(base, name, "svg")
			if svg:
				return svg

			png = self._tryIcon(base, name, "png")
			if png:
				return png

		return ""

	def _loadPixmap(self, path):
		try:
			self.instance.setPixmapFromFile(path)
		except Exception as e:
			print("[GlamNetIcon] ERROR loading icon:", e)

	def changed(self, what):
		if not self.instance:
			return

		if what[0] == self.CHANGED_CLEAR:
			self.instance.hide()
			return

		value = (self.source.text or "").strip()
		lname = value.lower()
		if lname in ("on", "true", "1", "yes", "vpn_on"):
			value = "vpn_on"
		elif lname in ("off", "false", "0", "no", "vpn_off"):
			value = "vpn_off"

		iconPath = self.cache.get(value, "")
		if not iconPath:
			iconPath = self.findIcon(value)
			if iconPath:
				self.cache[value] = iconPath

		if iconPath:

			if iconPath != self.currentIcon:
				self._loadPixmap(iconPath)
				self.currentIcon = iconPath
			self.instance.show()
		else:
			self.instance.hide()
