import threading
import Queue
import array
import logging
from logging.handlers import TimedRotatingFileHandler

class PackageHandlerThread (threading.Thread):

	OPERATION_CODES = {
		0x0031: "Single channel control",
		0x0032: "Response single channel control",
		0x15D0: "Read dry contact status",
		0x15D1: "Response read dry contact status",
		0x1647: "Broadcast sensors status",
		0x1948: "Read temperature",
		0x1949: "Response read temperature",
		0x1C00: "Read temperature",
		0x1C01: "Response read temperature",
		0x1C5C: "Control floor heating status",
		0x1C5D: "Response control floor heating status",
		0xE3E5: "Broadcast temperature",
		0xDA44: "Broadcast date and time (every minute)"
	}
	COMPONENT_TYPES = {
		0x0138: "Ceiling Mount PIR Sensor"
	}
	FIXED_BYTES_PART_1 = ['H', 'D', 'L', 'M', 'I', 'R', 'A', 'C', 'L', 'E']
	FIXED_BYTES_PART_2 = [0xAA, 0xAA] # = 0xAA
	BYTE_POSITION_LENGTH = 16
	BYTE_POSITION_SOURCE_SUBNET_ID = 17
	BYTE_POSITION_SOURCE_DEVICE_ID = 18
	BYTE_POSITION_DEVICE_TYPE_BYTE_1 = 19
	BYTE_POSITION_DEVICE_TYPE_BYTE_2 = 20
	BYTE_POSITION_OPERATION_CODE_BYTE_1 = 21
	BYTE_POSITION_OPERATION_CODE_BYTE_2 = 22
	BYTE_POSITION_TARGET_SUBNET_ID = 23
	BYTE_POSITION_TARGET_DEVICE_ID = 24
	BYTE_POSITION_CONTENT = 25
	LOG_TYPE_FILE_HUMAN_READABLE = 1

	def __init__(self, messageQueue):
		threading.Thread.__init__(self)
		self.messageQueue = messageQueue
		logHandler = TimedRotatingFileHandler("network.log", when="midnight", backupCount=7)
		logHandler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
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
		rawBytes = array.array("B", rawMessageStr)
		if(self.isMessageValid(rawBytes)):
			operationCodeInt = (((rawBytes[self.BYTE_POSITION_OPERATION_CODE_BYTE_1] & 0xFF) << 8) + (rawBytes[self.BYTE_POSITION_OPERATION_CODE_BYTE_2] & 0xFF))
			operationCode =  "0x" + ("%X" % operationCodeInt).zfill(4)
			sourceTypeInt = (((rawBytes[self.BYTE_POSITION_DEVICE_TYPE_BYTE_1] & 0xFF) << 8) + (rawBytes[self.BYTE_POSITION_DEVICE_TYPE_BYTE_2] & 0xFF))
			sourceType = "0x" + ("%X" % sourceTypeInt).zfill(4)
			sourceSubnetAndDeviceId = '{0:<5}'.format(str(rawBytes[self.BYTE_POSITION_SOURCE_SUBNET_ID] & 0xFF) + "/" + str(rawBytes[self.BYTE_POSITION_SOURCE_DEVICE_ID] & 0xFF))
			destinationSubnetAndDeviceId = '{0:<7}'.format(str(rawBytes[self.BYTE_POSITION_TARGET_SUBNET_ID] & 0xFF) + "/" + str(rawBytes[self.BYTE_POSITION_TARGET_DEVICE_ID] & 0xFF))
			contentLength = rawBytes[self.BYTE_POSITION_LENGTH] & 0xFF
			if(contentLength > 78 or contentLength < 11):
				self.log.warn("WARNING: Unexpected contents length [" + contentLength + "] of package:")
			contentLength = min(contentLength, 78)
			if(contentLength > 11):
				contentBytes = rawBytes[self.BYTE_POSITION_CONTENT:self.BYTE_POSITION_CONTENT + contentLength - 11]
				contents = "contents: " + "[" + self.getContentsAsText(contentBytes) + "]/[" + self.getContentsAsInts(contentBytes) + "]"
			else:
				contents = "no contents"

			self.log.info("Op: %s" % operationCode + " (" + self.getOperationName(operationCodeInt) + "), src: " + sourceSubnetAndDeviceId + " (" + sourceType + "/" + self.getTypeName(sourceTypeInt) + "), dst: " + destinationSubnetAndDeviceId + ", \n                        " + contents + "\n")


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

	def getTypeName(self, type):
		if(type in self.COMPONENT_TYPES):
			name = self.COMPONENT_TYPES[type]
		else:
			name = "Unknown component"
		return '{0:<30.30}'.format(name)


	def getContentsAsText(self, contentBytes):
		# TODO: How can we convert this unsigned char array to ISO-8859-1?
		return contentBytes.tostring().replace("\r\n", "").replace("\n", "").replace("\r", "")


	def getContentsAsInts(self, contentBytes):
		return ' '.join(str(c).rjust(3) for c in contentBytes)
