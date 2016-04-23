import select
import socket
import sys
import exceptions
import Queue
import packagehandler


def write_report(contents):
	millis = str(int(round(time.time() * 1000)))
	filename = 'networklogger_report-' + millis + '.txt'
	file = open(filename, 'w')
	file.write(contents)
	file.close()
	print('Wrote report to file [%s].' % (filename))


def send_report(contents):
	try:
		mail = email.mime.text.MIMEText(contents, 'plain', 'UTF-8')
		mail['Subject'] = 'HDL network logger status'
		mail['From'] = cfg.EMAIL_ADDRESS_FROM
		mail['To'] = cfg.EMAIL_ADDRESS_TO
		smtp = smtplib.SMTP(cfg.SMTP_HOST, cfg.SMTP_PORT)
		smtplib.SMTP.starttls(smtp)
		smtp.login(cfg.SMTP_USERNAME, cfg.SMTP_PASSWORD)
		smtp.sendmail(cfg.EMAIL_ADDRESS_FROM, [cfg.EMAIL_ADDRESS_TO], mail.as_string())
		smtp.quit()
	except socket.error as e:
		print e
		print 'Got socket error while trying to send mail. Will write report to file.'
		write_report(contents)
	except:
		print "Got unexpected error while trying to send mail. Will write report to file.", sys.exc_info()[0]
		write_report(contents)

def getConfig():
	try:
		cfg = __import__("hdlconfig")
	except ImportError:
		print '\033[93m' + "\nWARNING: Did not find a configuration file called hdlconfig.py. Will use default config. You can use the file hdlconfig-example.py as inspiration.\n" + '\033[0m'
		class Config(object):
			pass
		cfg = Config()
		cfg.HDL_PORT = 6000
	return cfg

def main():
	print 'Starting network logger...'

	cfg = getConfig()
	bufferSize = 95
	numOfExceptions = 0
	messageQueue = Queue.Queue()
	packageHandlerThread = packagehandler.PackageHandlerThread(messageQueue)
	packageHandlerThread.start()

	while numOfExceptions < 3:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.bind(('', cfg.HDL_PORT))
			#s.setblocking(0)
			print('Listening on port [%s]...' % (cfg.HDL_PORT))
			#numOfExceptions = 0
			while True:
				data, addr = s.recvfrom(bufferSize)
				messageQueue.put(data)
				#result = select.select([s],[],[])
				#msg = result[0][0].recv(bufferSize)
		except exceptions.KeyboardInterrupt:
			break
		except:
			numOfExceptions += 1
			print "Got unexpected error while logging network traffic.", sys.exc_info()[0]
			raise
	packageHandlerThread.stop()
	print 'Exiting application.'


if __name__ == '__main__':
	main()
