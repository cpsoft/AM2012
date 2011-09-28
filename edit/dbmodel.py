#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from dbview import *
from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy.orm import *
from db import *

class DbModel(gtk.GenericTreeModel):

	def __init__(self, database):
		self.database = database
		try:
			self.table = Table(self.tablename, database.metadata, autoload = True)
		except exc.NoSuchTableError:
			self.createTable()

		self.session = create_session()
		gtk.GenericTreeModel.__init__(self)
		return

	def get_column_names(self):
		return self.column_names[:]

	def get_column_types(self):
		return self.column_types[:]

	def on_get_flags(self):
		return gtk.TREE_MODEL_LIST_ONLY | gtk.TREE_MODEL_ITERS_PERSIST

	def on_get_n_columns(self):
		return len(self.column_types)

	def on_get_column_type(self, n):
		return self.column_types[n]

	def on_get_iter(self, path):
		if path[0] >= len(self.datas):
			return None
		return self.datas[path[0]]

	def on_get_path(self, rowref):
		return self.datas.index(rowref)

	def on_iter_next(self, rowref):
		try:
			i = self.datas.index(rowref) + 1
			return self.datas[i]
		except IndexError:
			return None

	def on_iter_children(self, rowref):
		if rowref:
			return None
		return self.datas[0]

	def on_iter_has_child(self, rowref):
		return False

	def on_iter_n_children(self, rowref):
		if rowref:
			return 0
		return len(self.datas)

	def on_iter_nth_child(self, rowref, n):
		if rowref:
			return None
		try:
			return self.datas[n]
		except IndexError:
			return None

	def on_iter_parent(self, child):
		return None

	def remove(self, iter):
		path = self.get_path(iter)
		data = self.datas[path[0]]
		self.datas.remove(data)
		self.row_deleted(path)
		self.session.delete(data)
		self.session.flush()

	def append(self, data):
		self.session.add(data)
		self.session.flush()
		self.datas.append(data)
		path = (self.datas.index(data), )
		iter = self.get_iter(path)
		self.row_inserted(path, iter)

	def get_data(self, iter):
		path = self.get_path(iter)
		return self.datas[path[0]]
	
		
	def modified(self, data):
		self.session.flush()
		path = (self.datas.index(data), )
		iter = self.get_iter(path)
		self.row_changed(path, iter)
