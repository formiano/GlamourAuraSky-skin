# GlamourExtra converter (Python 3)
# Modded and recoded by MCelliotG for use in Glamour skins or standalone
# Updated by OPENDROID_TEAM to use getCPUInfoString() from Components/About.py

from Components.About import getCPUInfoString
from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached
from enigma import eConsoleAppContainer


class GlamourExtra(Poll, Converter):
	TEMPERATURE = 0
	HDDTEMP = 1
	CPULOAD = 2
	CPUSPEED = 3
	FANINFO = 4
	UPTIME = 5

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.container = eConsoleAppContainer()
		self.type = self.getType(type)
		self.hddtemp = "Waiting for HDD Temp Data..."

		if self.type == self.HDDTEMP:
			self.container.appClosed.append(self.runFinished)
			self.container.dataAvail.append(self.dataAvail)
			self.container.execute("hddtemp -n -q /dev/sda")
			self.poll_interval = 500
		elif self.type == self.UPTIME:
			self.poll_interval = 1000
		else:
			self.poll_interval = 7000

		self.poll_enabled = True

	def getType(self, type):
		mapping = {
			"CPULoad": self.CPULOAD,
			"CPUSpeed": self.CPUSPEED,
			"Temperature": self.TEMPERATURE,
			"Uptime": self.UPTIME,
			"HDDTemp": self.HDDTEMP,
			"FanInfo": self.FANINFO
		}
		return mapping.get(type.split(",")[0], None)

	def dataAvail(self, strData):
		self.hddtemp = strData.decode("utf-8", "ignore").strip()

	def runFinished(self, retval):
		if "No such file or directory" in self.hddtemp or "not found" in self.hddtemp:
			self.hddtemp = "HDD Temp: N/A"
		elif self.hddtemp.isdigit():
			temp_value = int(self.hddtemp)
			self.hddtemp = f"HDD Temp: {temp_value}°C" if temp_value > 0 else "HDD idle or N/A"
		else:
			self.hddtemp = "HDD idle or N/A"

	@cached
	def getText(self):
		if self.type in (self.CPULOAD, self.CPUSPEED, self.TEMPERATURE, self.FANINFO):
			processor, speed, cores, temperature = getCPUInfoString()
			if self.type == self.CPULOAD:
				return self.getCpuLoad()
			elif self.type == self.CPUSPEED:
				return f"CPU Speed: {speed}"
			elif self.type == self.TEMPERATURE:
				return f"Temperature: {temperature}" if temperature else "Temperature: N/A"
			elif self.type == self.FANINFO:
				return f"{processor} - {cores}"
		elif self.type == self.HDDTEMP:
			return self.hddtemp
		elif self.type == self.UPTIME:
			return self.getUptime()
		return "N/A"

	def getCpuLoad(self):
		try:
			with open("/proc/loadavg") as f:
				return f"CPU Load: {f.readline().split()[0]}"
		except:
			return "CPU Load: N/A"

	def getUptime(self):
		try:
			with open("/proc/uptime") as f:
				total_seconds = int(float(f.readline().split()[0]))
		except:
			return "Uptime: N/A"

		days, remainder = divmod(total_seconds, 86400)
		hours, remainder = divmod(remainder, 3600)
		minutes, seconds = divmod(remainder, 60)
		return f"Uptime: {days}d {hours}h {minutes}m {seconds}s"

	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
