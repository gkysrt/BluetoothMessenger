# A custom stack that has extra features
class Stack(list):
	def __init__(self):
		super().__init__()
		self.__limit = -1
		self.__limitEnabled = False
		self.__pointer = -1  # Points an index on the stack, this point can be used for various operations.

	# Define a element limit. Stack forgets least recent element if limit is overrun.
	def setLimit(self, limit):
		self.__limit = limit

	# Return limit
	def limit(self):
		return self.__limit

	def setLimitEnabled(self, enabled):
		self.__limitEnabled = enabled

	def limitEnabled(self):
		return self.__limitEnabled

	def append(self, _object):
		if self.limitEnabled() and self.limit() > 0:
			elementCount = len(self)
			if elementCount + 1 > self.limit():
				self.pop(0)

		super().append(_object)
		self.resetPointer()

	def push(self, _object):
		self.append(_object)

	def pop(self, index):
		super().pop(index)
		self.resetPointer()

	# Get pointer index
	def pointer(self):
		return self.__pointer

	# Set pointer index
	def setPointer(self, index):
		self.__pointer = index

	# Reset pointer
	def resetPointer(self):
		self.__pointer = len(self)

	# Increment pointer by 1 or more
	def incrementPointer(self, steps=1):
		if self.__pointer + steps <= len(self) - 1:
			self.__pointer += steps

	# Decrement pointer by 1 or more
	def decrementPointer(self, steps=1):
		if self.__pointer - steps >= 0:
			self.__pointer -= steps

	# softPop() returns the item that pointer shows and does not pop it,
	# decrements pointer and behaves like standart pop operation
	def softPop(self, index=None):
		if self.__pointer < 0 or self.__pointer > len(self):
			return None

		if index:
			item = self[index]
			self.__pointer = index
			return item

		if self.pointer() - 1 < 0:
			return None

		self.decrementPointer()
		item = self[self.pointer()]
		return item

	# reverseSoftPop() returns the item that pointer shows and does not pop it,
	# increments pointer and behaves like reverse pop operation
	def reverseSoftPop(self, index=None):
		if self.__pointer < 0 or self.__pointer > len(self):
			return None

		if index:
			item = self[index]
			self.__pointer = index
			return item

		if self.pointer() + 1 > len(self) - 1:
			self.resetPointer()
			return None

		self.incrementPointer()
		item = self[self.pointer()]
		return item
