
from dbview import *
from aircompany import AirCompany
import string

class AirCompanyDialog:
	def __init__(self, data):
		if data == None:
			return
		self.data = data
		self.dialog = gtk.Dialog(title = "air company",
						flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
						buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK,
								gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
		self.dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)

		frame = gtk.Frame("air company")
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
		self.dialog.destroy()
		return ret


class AirCompanyView(DbView):
	def __init__(self, model):
		DbView.__init__(self, model)
		self.treeview.connect("select-cursor-row", self.select)
	
	def select(self, widget, start_editing, data=None):
		(model, iter) = self.selection.get_selected()
		airCompany = model.get_aircompany(iter)
		dialog = AirCompanyDialog(airCompany)
		if dialog.run() == gtk.RESPONSE_OK:
			model.modified(airCompany)

	def add(self, widget, data=None):
		airCompany = AirCompany()
		dialog = AirCompanyDialog(airCompany)
		if dialog.run() == gtk.RESPONSE_OK:
			self.model.append(airCompany)
