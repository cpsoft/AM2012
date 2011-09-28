#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from dbview import *
from sqlalchemy import *
from sqlalchemy.orm import *
from db import *
from dbmodel import DbModel


class AirCompany(object):
	def __repr__(self):
		return ("<Airpalne('%s', '%s', '%s', '%s')>" % 
					(self.name, self.image, self.start, self.end))


class AirCompanyModel(DbModel):
	column_types = (long, str, str, str, str)
	column_names = ['id', 'name', 'image']
	tablename = 'aircompany'

	def __init__(self, database):
		DbModel.__init__(self, database)
		mapper(AirCompany, self.table)
		self.datas = self.session.query(AirCompany).all()

	def createTable(self):
		self.table = Table(self.tablename, self.database.metadata,
					Column(self.column_names[0], Integer, primary_key=True),
					Column(self.column_names[1], String(40)),
					Column(self.column_names[2], String(256)),
					keep_existing = True
					)
		self.table.create()
		return

	def on_get_value(self, rowref, column):
		if column is 0:
			return rowref.id
		elif column is 1:
			return rowref.name
		elif column is 2:
			return rowref.image
		return None
