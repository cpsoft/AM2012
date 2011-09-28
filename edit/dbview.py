#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class DbView:
	def __init__(self, model):
		self.model = model
		self.widget = gtk.VBox()
		self.createTreeView()
		self.scrolledwindow = gtk.ScrolledWindow()
		self.scrolledwindow.add(self.treeview)
		self.widget.pack_start(self.scrolledwindow, padding = 10)
		self.createButtonBox()
		self.widget.pack_start(self.buttonbox, False, False, padding = 10)
		return

	def createTreeView(self):
		self.treeview = gtk.TreeView(self.model)
		column_names = self.model.get_column_names()
		column_types = self.model.get_column_types()
		self.tvcolumn = [None] * len(column_names)
		for i in range(len(column_names)):
			if column_types is gtk.gdk.Pixbuf:
				cell = gtk.CellRendererPixbuf()
			else:
				cell = gtk.CellRendererText()
			self.tvcolumn[i] = gtk.TreeViewColumn(column_names[i], cell, text = i)
			self.treeview.append_column(self.tvcolumn[i])
		self.treeview.set_search_column(0)
		self.treeview.set_reorderable(True)
		self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		self.treeview.set_enable_tree_lines(True)
		self.selection = self.treeview.get_selection()
		self.selection.set_mode(gtk.SELECTION_SINGLE)

	def createButtonBox(self):
		self.buttonbox = gtk.HButtonBox()
		self.buttonbox.set_layout(gtk.BUTTONBOX_END)
		self.button = gtk.Button(stock = gtk.STOCK_ADD)
		self.button.connect("clicked", self.add)
		self.buttonbox.pack_start(self.button)

		self.button = gtk.Button(stock = gtk.STOCK_DELETE)
		self.button.connect("clicked", self.delete)
		self.buttonbox.pack_start(self.button)

	def delete(self, widget, data = None):
		(model, iter) = self.selection.get_selected()
		self.model.remove(iter)
