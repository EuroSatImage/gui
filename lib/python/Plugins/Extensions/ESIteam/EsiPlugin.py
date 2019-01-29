﻿from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Components.ActionMap import ActionMap
from Components.config import config, ConfigText, configfile
from Components.Sources.List import List
from Components.Label import Label
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_SKIN_IMAGE, fileExists, pathExists, createDir
from Tools.LoadPixmap import LoadPixmap
from Components.PluginList import *
from Plugins.Plugin import PluginDescriptor
from Components.PluginComponent import plugins
from Components.Console import Console
from os import popen, system, listdir, chdir, getcwd, remove as os_remove
from enigma import iServiceInformation, eTimer, eDVBDB, eDVBCI_UI, eListboxPythonStringContent, eListboxPythonConfigContent, gFont, loadPNG, eListboxPythonMultiContent, iServiceInformation

import os
import sys

config.misc.fast_plugin_button = ConfigText(default="")

class ESIPluginPanel(Screen):
	skin = """
<screen name="ESIPluginPanel" position="center,center" size="1150,650">
<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ESIteam/images/menu/fondo.png" alphatest="blend" transparent="1" />
<widget source="global.CurrentTime" render="Label" position="35,10" size="500,24" font="Regular;22" foregroundColor="#FFFFFF" halign="left" transparent="1" zPosition="5">
		<convert type="ClockToText">>Format%H:%M:%S</convert>
</widget>
	<eLabel text="OpenESI Plugins Panel" position="45,40" size="800,38" font="Regular;32" halign="left" foregroundColor="#004c74" backgroundColor="transpBlack" transparent="1"/>
			<widget source="list" render="Listbox" position="55,105" zPosition="1" size="590,450" scrollbarMode="showOnDemand"  transparent="1">
			 <convert type="TemplatedMultiContent">
				 {"template": [
				 MultiContentEntryText(pos = (125, 0), size = (550, 24), font=0, text = 0),
				 MultiContentEntryText(pos = (125, 24), size = (550, 24), font=1, text = 1),
				 MultiContentEntryPixmapAlphaTest(pos = (6, 5), size = (100, 40), png = 2),
				 ],
				 "fonts": [gFont("Regular", 24),gFont("Regular", 20)],
				 "itemHeight": 50
				 }
			</convert>
			</widget>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ESIteam/images/buttons/red150x30.png" position="30,590" size="150,30" alphatest="on"/>
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ESIteam/images/buttons/green150x30.png" position="200,590" size="150,30" alphatest="on"/>
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ESIteam/images/buttons/yellow150x30.png" position="370,590" size="150,30" alphatest="on"/>
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ESIteam/images/buttons/blue150x30.png" position="543,590" size="150,30" alphatest="on"/>
			<widget name="key_red" position="30,594" zPosition="2" size="150,25" font="Regular; 18" halign="center" valign="center" backgroundColor="red" transparent="1" />
			<widget name="key_green" position="200,594" zPosition="1" size="150,25" font="Regular; 18" halign="center" valign="center" backgroundColor="green" transparent="1" />
			<widget name="key_yellow" position="370,594" zPosition="1" size="150,25" font="Regular; 18" halign="center" valign="center" backgroundColor="yellow" transparent="1" />
			<widget name="key_blue" position="543,594" zPosition="1" size="150,25" font="Regular; 18" halign="center" valign="center" backgroundColor="blue" transparent="1" />

</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)

		self["key_green"] = Label(_("Addons"))
		self["key_red"] = Label(_("Update"))
		self["key_yellow"] = Label(_("Scripts"))
		self["key_blue"] = Label(_("Tools"))

		self.list = []
		self["list"] = List(self.list)
		self.updateList()

		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.runPlug,
			"back": self.close,
			"red": self.keyRed,
			"green": self.keyGreen,
			"yellow": self.keyYellow,
			"blue": self.keyBlue
		}, -1)

	def runPlug(self):
		mysel = self["list"].getCurrent()
		if mysel:
			plugin = mysel[3]
			plugin(session=self.session)

	def updateList(self):
		self.list = [ ]
		self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
		for plugin in self.pluginlist:
			if plugin.icon is None:
				png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/icons/plugin.png"))
			else:
				png = plugin.icon
			res = (plugin.name, plugin.description, png, plugin)
			self.list.append(res)

		self["list"].list = self.list

	def keyYellow(self):
		from Plugins.Extensions.ESIteam.EsiScripts import ESIScripts
		self.session.open(ESIScripts)

	def keyRed(self):
		from Plugins.SystemPlugins.SoftwareManager.plugin import UpdatePluginMenu
		self.session.open(UpdatePluginMenu)

	def keyGreen(self):
		from Screens.PluginBrowser import PluginDownloadBrowser
		self.session.open(PluginDownloadBrowser)

	def keyBlue(self):
		from Plugins.Extensions.ESIteam.EsiUtil import ESIUtiles
		self.session.open(ESIUtiles)

class ESIPl:
	def __init__(self):
		self["ESIPl"] = ActionMap( [ "InfobarSubserviceSelectionActions" ],
			{
				"ESIPlshow": (self.showESIPl),
			})

	def showESIPl(self):
		self.session.openWithCallback(self.callNabAction, ESIPluginPanel)

	def callNabAction(self, *args):
		if len(args):
			(actionmap, context, action) = args
			actionmap.action(context, action)
