import threading
import Queue
import array
import logging
from logging.handlers import TimedRotatingFileHandler

class PackageHandlerThread (threading.Thread):

	FIXED_BYTES_PART_1 = ['H', 'D', 'L', 'M', 'I', 'R', 'A', 'C', 'L', 'E']
	FIXED_BYTES_PART_2 = [-86, -86] # = 0xAA
	BYTE_POSITION_OPERATION_CODE_BYTE_1 = 21
	BYTE_POSITION_OPERATION_CODE_BYTE_2 = 22
	LOG_TYPE_FILE_HUMAN_READABLE = 1
	OPERATION_CODES = {
		0x0031: "Single channel control",
		0x0032: "Response single channel control",
		0x1647: "Broadcast sensors status",
		0x1948: "Read temperature",
		0x1949: "Response read temperature",
		0x1C5C: "Control floor heating status",
		0x1C5D: "Response control floor heating status",
		0xE3E5: "Broadcast temperature",
		0xDA44: "Broadcast date and time (every minute)"
	}

	def __init__(self, messageQueue):
		threading.Thread.__init__(self)
		self.messageQueue = messageQueue
		logHandler = TimedRotatingFileHandler("network.log", when="midnight", backupCount=7)
		#logHandler.suffix = '%Y-%m-%d.log'
		logging.basicConfig(format='%(asctime)s %(message)s')
		self.log = logging.getLogger()
		self.log.setLevel(logging.DEBUG)
		self.log.addHandler(logHandler)


	def run(self):
		print "Starting package handler thread..."
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
			#print "rawMessageStr: ", rawMessageStr
			#print rawBytes
			#print map(hex, rawBytes)
			#print rawBytes[self.BYTE_POSITION_OPERATION_CODE_BYTE_1].__class__.__name__
			operationCodeInt = (((rawBytes[self.BYTE_POSITION_OPERATION_CODE_BYTE_1] & 0xFF) << 8) + (rawBytes[self.BYTE_POSITION_OPERATION_CODE_BYTE_2] & 0xFF))
			operationCode =  "0x" + ("%X" % operationCodeInt).zfill(4)
			#print "Operation code: ", map(hex, operationCode)
			self.log.info("Op: %s" % operationCode + " (" + self.getOperationName(operationCodeInt) + ")")
			#print "Operation code: ", operationCode


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


	def getOperationName(self, operationCodeInt):
		if(operationCodeInt in self.OPERATION_CODES):
			name = self.OPERATION_CODES[operationCodeInt]
		else:
			name = "Unknown operation"
		return '{0:<30.30}'.format(name)

