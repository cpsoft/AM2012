from sqlalchemy import *

class DataBase:
	def __init__(self):
		self.db = create_engine("sqlite:///am.db")
		self.metadata=MetaData(self.db)
		return
