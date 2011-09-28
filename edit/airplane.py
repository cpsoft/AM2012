#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from dbview import *
from sqlalchemy import *
from sqlalchemy.orm import *
from db import *
from dbmodel import DbModel

class AirPlane(object):
	def __repr__(self):
		return ("<Airpalne('%s', '%s', '%s', '%s')>" % 
					(self.name, self.image, self.company, self.start, self.end))


class AirPlaneModel(DbModel):
	column_types = (long, str, str, str, 
					long, long, long,
					str, str)
	column_names = ['id', 'name', 'image', 'company', 
					'travle', 'consume', 'Maintain',
					'start', 'end']
	tablename = 'airplane'

	def __init__(self, database):
		DbModel.__init__(self, database)
		mapper(AirPlane, self.table)
		self.datas = self.session.query(AirPlane).all()
		return

	def createTable(self):
		self.table = Table(self.tablename, self.database.metadata,
					Column(self.column_names[0], Integer, primary_key=True),
					Column(self.column_names[1], String(40)),
					Column(self.column_names[2], String(256)),
					Column(self.column_names[3], String(256)),
					Column(self.column_names[4], Integer),
					Column(self.column_names[5], Integer),
					Column(self.column_names[6], Integer),
					Column(self.column_names[7], String(20)),
					Column(self.column_names[8], String(20)),
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
		elif column is 3:
			return rowref.company
		elif column is 4:
			return rowref.start
		elif column is 5:
			return rowref.end
		return None
