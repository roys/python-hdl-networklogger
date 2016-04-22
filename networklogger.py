import hdlconfig as cfg
import select
import socket
import sys
import exceptions


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


def main():
	print 'Starting network logger...'

	bufferSize = 95

	numOfExceptions = 0

	while numOfExceptions < 3:
		print numOfExceptions
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.bind(('', 6000))
			#s.setblocking(0)
			print('Listening on port [%s]...' % (cfg.HDL_PORT))
			#numOfExceptions = 0
			while True:
				data, addr = s.recvfrom(bufferSize)
				print "received message:", data
				#result = select.select([s],[],[])
				#msg = result[0][0].recv(bufferSize)
		except exceptions.KeyboardInterrupt:
			break
		except:
			numOfExceptions += 1
			print "Got unexpected error while logging network traffic.", sys.exc_info()[0]
			raise
	print 'Exiting application.'


if __name__ == '__main__':
	main()
