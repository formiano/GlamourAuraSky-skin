#  GlamCI renderer
#  Modded and recoded by MCelliotG for use in Glamour skins or standalone, added Python3 support
#  If you use this Renderer for other skins and rename it, please keep the first and second line adding your credits below

from Components.Renderer.Renderer import Renderer
from Components.VariableText import VariableText
from enigma import eDVBCI_UI, eDVBCIInterfaces, eLabel, iPlayableService


class GlamCI(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.eDVBCIUIInstance = eDVBCI_UI.getInstance()
		self.eDVBCIUIInstance and self.eDVBCIUIInstance.ciStateChanged.get().append(self.ciModuleStateChanged)
		self.NUM_CI = eDVBCIInterfaces.getInstance() and eDVBCIInterfaces.getInstance().getNumOfSlots()
		self.text = ""
		self.allVisible = False

	GUI_WIDGET = eLabel

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for (attrib, value) in self.skinAttributes:
			if attrib == "allVisible":
				self.allVisible = value == "1"
				attribs.remove((attrib,value))
				break
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def ciModuleStateChanged(self, slot):
		self.changed(True)

	def changed(self, what):
		if what == True or (what[0] == self.CHANGED_SPECIFIC and what[1] == iPlayableService.evStart):
			string = ""
			if self.NUM_CI and self.NUM_CI > 0:
				if self.eDVBCIUIInstance:
					for slot in list(range(self.NUM_CI)):
						add_num = True
						if string:
							string += " "
						state = self.eDVBCIUIInstance.getState(slot)
						if state != -1:
							if state == 0:
								if not self.allVisible:
									string += ""
									add_num = False
								else:
									string += r"\c007?7?7?"
							elif state == 1:
								string += r"\c00????00"
							elif state == 2:
								string += r"\c0000??00"
						else:
							if not self.allVisible:
								string += ""
								add_num = False
							else:
								string += r"\c00??2525"
						if add_num:
							string += "%d" % (slot + 1)
					if string:
						string = _("CI slot: ") + string
			self.text = string
