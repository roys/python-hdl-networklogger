import threading
import Queue

class PackageHandlerThread (threading.Thread):

	def __init__(self, messageQueue):
		threading.Thread.__init__(self)
		self.messageQueue = messageQueue

	def run(self):
		print "Starting " + self.__class__.__name__ + "..."
		self.running = True
		while self.running:
			data = self.messageQueue.get()
			if data is None:
				break
			print "data: ", data
		print "Stopping " + self.__class__.__name__ + "..."

	def stop(self):
		self.running = False # This will stop the thread even though we have a lot of work left
		self.messageQueue.put(None) # This will stop the thread even though the thread is blocking
