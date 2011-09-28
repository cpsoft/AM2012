
from dbview import *
from airplane import AirPlane
import string

class AirPlaneDialog:
	def __init__(self, data):
		if data == None:
			return
		self.data = data
		self.dialog = gtk.Dialog(title = "airplane",
						flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
						buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK,
								gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
		self.dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)

		frame = gtk.Frame("airplane")
		table = gtk.Table(6, 2, False)

		label = gtk.Label("name:")
		table.attach(label, 0, 1, 0, 1)
		self.entry = gtk.Entry()
		table.attach(self.entry, 1, 2, 0, 1)
		if data.name != None:
			self.entry.set_text(data.name)

		label = gtk.Label("image:")
		table.attach(label, 0, 1, 1, 2)
		self.fileChooserButton = gtk.FileChooserButton("image")
		table.attach(self.fileChooserButton, 1, 2, 1, 2)
		image = gtk.Image()
		table.attach(image, 1, 2, 2, 3)
		self.fileChooserButton.connect("file-set", self.fileSet, image)
		
		if data.image != None:
			self.fileChooserButton.set_filename(data.image)
			image.set_from_file(data.image)

		label = gtk.Label("start:")
		table.attach(label, 0, 1, 3, 4)
		self.start = gtk.Calendar()
		table.attach(self.start, 1, 2, 3, 4)
		if data.start != None:
			date = data.start.split('-')
			self.start.select_month(string.atoi(date[1]), string.atoi(date[0]))
			self.start.select_day(string.atoi(date[2]))
		
		label = gtk.Label("end:")
		table.attach(label, 0, 1, 4, 5)
		self.end = gtk.Calendar()
		table.attach(self.end, 1, 2, 4, 5)
		if data.end != None:
			date = data.end.split('-')
			self.end.select_month(string.atoi(date[1]), string.atoi(date[0]))
			self.end.select_day(string.atoi(date[2]))

		frame.add(table)
		self.dialog.vbox.pack_start(frame)

		self.dialog.show_all()
		return

	def fileSet(self, widget, data=None):
		filename = widget.get_filename()
		data.set_from_file(filename)

	def run(self):
		ret = self.dialog.run()
		if gtk.RESPONSE_OK == ret:
			self.data.name = self.entry.get_text()
			self.data.image = self.fileChooserButton.get_filename()
			self.data.start = "%d-%d-%d" % self.start.get_date()
			self.data.end = "%d-%d-%d" % self.end.get_date()
		self.dialog.destroy()
		return ret


class AirPlaneView(DbView):
	def __init__(self, model):
		DbView.__init__(self, model)
		self.treeview.connect("select-cursor-row", self.select)
	
	def select(self, widget, start_editing, data=None):
		(model, iter) = self.selection.get_selected()
		airPlane = model.get_data(iter)
		dialog = AirPlaneDialog(airPlane)
		if dialog.run() == gtk.RESPONSE_OK:
			model.modified(airPlane)

	def add(self, widget, data=None):
		airPlane = AirPlane()
		dialog = AirPlaneDialog(airPlane)
		if dialog.run() == gtk.RESPONSE_OK:
			self.model.append(airPlane)
