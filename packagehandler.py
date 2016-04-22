import threading
import Queue
import array

class PackageHandlerThread (threading.Thread):

	FIXED_BYTES_PART_1 = ['H', 'D', 'L', 'M', 'I', 'R', 'A', 'C', 'L', 'E']
	FIXED_BYTES_PART_2 = [-86, -86] # = 0xAA
	BYTE_POSITION_OPERATION_CODE_BYTE_1 = 21
	BYTE_POSITION_OPERATION_CODE_BYTE_2 = 22

	def __init__(self, messageQueue):
		threading.Thread.__init__(self)
		self.messageQueue = messageQueue

	def run(self):
		print "Starting " + self.__class__.__name__ + "..."
		self.running = True
		while self.running:
			message = self.messageQueue.get()
			if message is None:
				break
			self.processMessage(message)
		print "Stopping " + self.__class__.__name__ + "..."

	def stop(self):
		self.running = False # This will stop the thread even though we have a lot of work left
		self.messageQueue.put(None) # This will stop the thread even though the thread is blocking

	def processMessage(self, rawMessageStr):
		rawBytes = array.array("b", rawMessageStr)
		if(self.isMessageValid(rawBytes)):
			print "rawMessageStr: ", rawMessageStr
			#print rawBytes
			#print map(hex, rawBytes)
			print rawBytes[self.BYTE_POSITION_OPERATION_CODE_BYTE_1].__class__.__name__
			operationCode = (rawBytes[self.BYTE_POSITION_OPERATION_CODE_BYTE_1] & 0xFF, rawBytes[self.BYTE_POSITION_OPERATION_CODE_BYTE_2] & 0xFF)
			print "Operation code: ", map(hex, operationCode)


	def isMessageValid(self, bytes):
		if(bytes is not None and len(bytes) >= 23):
			for i in range(0, len(self.FIXED_BYTES_PART_1)):
				if(ord(self.FIXED_BYTES_PART_1[i]) is not bytes[i + 4]):
					return False
			for i in range(0, len(self.FIXED_BYTES_PART_2)):
				if(self.FIXED_BYTES_PART_2[i] != bytes[i + 14]):
					return False
			# TODO: Verify CRC
			return True
		return False
