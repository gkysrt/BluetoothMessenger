from PySide2 import QtCore
from models import ListModel


class ModelFilter(ListModel.ListModel):
	def __init__(self, adapter = None, parent = None):
		super().__init__(adapter=adapter, parent=parent)

	# def rowCount(self, index):
	# 	return 0
	#
	# def index(self, row, column, parent = QtCore.QModelIndex()):
	# 	return QtCore.QModelIndex()
	#
	# def flags(self, index):
	# 	return super().flags()

	def setFilter(self, func):
		pass
