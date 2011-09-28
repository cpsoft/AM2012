#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from sqlalchemy import *
from db import *
from aircompanyview import *
from aircompany import AirCompanyModel
from airplaneview import *
from airplane import AirPlaneModel


class App:
	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Air Manager 2012 editor")
		window.set_size_request(800, 600)
		window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		window.connect("destroy", gtk.main_quit)

		notebook = gtk.Notebook()
		window.add(notebook)
		db = DataBase()

		airPlaneModel = AirPlaneModel(db)
		airPlaneView = AirPlaneView(airPlaneModel)
		label = gtk.Label("Airplane")
		notebook.append_page(airPlaneView.widget, label)

		airCompanyModel = AirCompanyModel(db)
		airCompanyView = AirCompanyView(airCompanyModel)
		label = gtk.Label("Company")
		notebook.append_page(airCompanyView.widget, label)

		window.show_all()

	def run(self):
		gtk.main()

if __name__ == "__main__":
	app = App()
	app.run()
